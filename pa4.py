#!/usr/bin/env python3

# Author: Edgaras Fiodorovas
# Date:   12-13-2018

import pickle
import copy
import re
import logging
import math
import itertools
from collections import OrderedDict

from pathlib import Path
from antlr4.error.ErrorListener import ErrorListener
from grammar.SQL457Lexer import SQL457Lexer
from grammar.SQL457Visitor import SQL457Visitor
from grammar.SQL457Listener import SQL457Listener
from grammar.SQL457Parser import *

# Setups logger, change level to logging.DEBUG to view debug messages
logging.basicConfig(format='%(message)s', level=logging.INFO, stream=sys.stdout) 

# =====================================================================================================================
# Helper Functions: 

# Extracts raw string from parse tree
def getCtxString(ctx):
    return ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop)

# Prepares expression parser and executes it
def resolveExpression(expr, columns=None, rows=None):
    walker = ParseTreeWalker()
    exprResListener = SQL457ExprResListener(columns, rows)
    walker.walk(exprResListener, expr)
    return expr

# =====================================================================================================================
# Custom Exceptions:

class DBMSDatabaseMissing(Exception):
    pass
class DBMSTableMissing(Exception):
    pass
class DBMSTableLocked(Exception):
    pass
class DBMSTransactionAbort(Exception):
    pass

class DBMSDuplicateColumn(Exception):
    pass
class DBMSTypeMismatch(Exception):
    pass
class DBMSValueTooBig(Exception):
    pass
class DBMSUnknownColumn(Exception):
    pass
class DBMSUnknownTable(Exception):
    pass
class DBMSIncompatibleTypes(Exception):
    pass

# =====================================================================================================================
# Resolves epxression parse trees with given table structures and rows (one of each per table)
class SQL457ExprResListener(SQL457Listener):
    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows

    #   '(' expr ')'
    def exitParanthesis(self, ctx):
        ctx.val = ctx.expr().val
        ctx.type = ctx.expr().type
        ctx.size = ctx.expr().size
        ctx.id = ctx.expr().id
        ctx.tbl = ctx.expr().tbl

    #   literalValue
    def exitValue(self, ctx):
        ctx.val = ctx.literalValue().val
        ctx.type = ctx.literalValue().type
        ctx.size = ctx.literalValue().size
        ctx.id = None
        ctx.tbl = None

    #   tbl '.' column
    #   column
    def exitColumn(self, ctx):
        ctx.val = None
        ctx.type = None
        ctx.size = None
        ctx.id = None
        ctx.tbl = None

        # Resolve columns if there's data
        if self.rows:
            tableName = None
            columnName = ctx.column.id
            columnSchema = None
            
            # Find schema for column
            if ctx.table and not self.rows.get(ctx.table.id) is None:
                tableName = ctx.table.id
                tableSchema = self.columns.get(tableName)
                if not tableSchema:
                    raise DBMSUnknownTable(tableName)
                columnSchema = dict(self.columns[tableName]).get(columnName)
            else:
                for tblName, tblSchema in self.columns.items():
                    if not self.rows.get(tblName):
                        continue

                    tmp = dict(tblSchema).get(columnName)
                    if tmp:
                        tableName = tblName
                        columnSchema = tmp
                        break
            
            if columnSchema:
                # Update node values
                ctx.val = self.rows[tableName][columnName]
                ctx.type = columnSchema["type"]
                if ctx.type == "varchar":
                    ctx.type = "char"

                if columnSchema["size"]:
                    len(ctx.val)
            else:
                ctx.val = None
                ctx.type = "null"

        # Don't resolve columns if there's no data
        else:
            if ctx.table:
                ctx.val = ctx.table.id + '.' + ctx.column.id
                ctx.tbl = ctx.table.id
            else:
                ctx.val = ctx.column.id
            ctx.id = ctx.column.id
            ctx.type = "id"

    # NOT expr
    def exitInverse(self, ctx):
        ctx.type = "int"
        ctx.size = None
        ctx.id = None
        ctx.tbl = None
        ctx.val = 0
        
        val1Type = ctx.expr().type
        if (val1Type == "int" or val1Type == "float"):
            ctx.val = ctx.expr().val and 0 or 1
        elif val1Type == "null":
            ctx.type = "null"
            ctx.val = None

    # -expr
    def exitNegative(self, ctx):
        ctx.type = "int"
        ctx.size = None
        ctx.id = None
        ctx.tbl = None
        ctx.val = 0

        val1Type = ctx.expr().type
        if (val1Type == "int" or val1Type == "float"):
            ctx.val = -ctx.expr().val
            ctx.type = val1Type
        elif val1Type == "null":
            ctx.type = "null"
            ctx.val = None

    # expr || expr
    def exitConcat(self, ctx):
        ctx.type = "char"
        ctx.size = None
        ctx.id = None
        ctx.tbl = None

        if ctx.expr(0).type != "null" and ctx.expr(1).type != "null":
            ctx.val = str(ctx.expr(0).val) + str(ctx.expr(1).val)
        else:
            ctx.type = "null"
            ctx.val = None


    # expr * expr
    def exitMultiply(self, ctx):
        ctx.type = "int"
        ctx.size = None
        ctx.val = 0
        ctx.id = None
        ctx.tbl = None

        val0Type = ctx.expr(0).type
        val1Type = ctx.expr(0).type
        if (val0Type == "int" or val0Type == "float") and (val1Type == "int" or val1Type == "float"):
            ctx.val = ctx.expr(0).val * ctx.expr(1).val
            if val0Type == "float" or val1Type == "float":
                ctx.type = "float"
        elif val0Type == "null" or val1Type == "null":
            ctx.type = "null"
            ctx.val = None
        
    # expr / expr
    def exitDivide(self, ctx):
        ctx.type = "int"
        ctx.size = None
        ctx.val = 0
        ctx.id = None
        ctx.tbl = None

        val0Type = ctx.expr(0).type
        val1Type = ctx.expr(0).type
        if (val0Type == "int" or val0Type == "float") and (val1Type == "int" or val1Type == "float"):
            ctx.val = ctx.expr(0).val / ctx.expr(1).val
            if val0Type == "float" or val1Type == "float":
                ctx.type = "float"
            else:
                ctx.val = math.floor(ctx.val)
        elif val0Type == "null" or val1Type == "null":
            ctx.type = "null"
            ctx.val = None

    # expr % expr
    def exitModulo(self, ctx):
        ctx.type = "int"
        ctx.size = None
        ctx.val = 0
        ctx.id = None
        ctx.tbl = None

        val0Type = ctx.expr(0).type
        val1Type = ctx.expr(0).type
        if (val0Type == "int" or val0Type == "float") and (val1Type == "int" or val1Type == "float"):
            ctx.val = math.floor(ctx.expr(0).val) % math.floor(ctx.expr(1).val)
        elif val0Type == "null" or val1Type == "null":
            ctx.type = "null"
            ctx.val = None

    # expr + expr
    def exitAdd(self, ctx):
        ctx.type = None
        ctx.size = None
        ctx.val = None
        ctx.id = None
        ctx.tbl = None

        val0Type = ctx.expr(0).type
        val1Type = ctx.expr(0).type
        if (val0Type == "int" or val0Type == "float") and (val1Type == "int" or val1Type == "float"):
            ctx.val = ctx.expr(0).val + ctx.expr(1).val
            if val0Type == "float" or val1Type == "float":
                ctx.type = "float"
        elif val0Type == "null" or val1Type == "null":
            ctx.type = "null"
            ctx.val = None
        else:
            ctx.val = str(ctx.expr(0).val) + str(ctx.expr(1).val)
            ctx.type = "char"

    # expr - expr
    def exitSubtract(self, ctx):
        ctx.type = "int"
        ctx.size = None
        ctx.id = None
        ctx.tbl = None
        ctx.val = 0

        val0Type = ctx.expr(0).type
        val1Type = ctx.expr(0).type
        if (val0Type == "int" or val0Type == "float") and (val1Type == "int" or val1Type == "float"):
            ctx.val = ctx.expr(0).val - ctx.expr(1).val
            if val0Type == "float" or val1Type == "float":
                ctx.type = "float"
        elif val0Type == "null" or val1Type == "null":
            ctx.type = "null"
            ctx.val = None

    # expr >> expr
    def exitShiftRight(self, ctx):
        ctx.type = "int"
        ctx.size = None
        ctx.id = None
        ctx.tbl = None
        ctx.val = 0

        val0Type = ctx.expr(0).type
        val1Type = ctx.expr(0).type
        if (val0Type == "int" or val0Type == "float") and (val1Type == "int" or val1Type == "float"):
            ctx.val = math.floor(ctx.expr(0).val) >> math.floor(ctx.expr(1).val)
        elif val0Type == "null" or val1Type == "null":
            ctx.type = "null"
            ctx.val = None

    # expr << expr
    def exitShiftLeft(self, ctx):
        ctx.type = "int"
        ctx.size = None
        ctx.id = None
        ctx.tbl = None
        ctx.val = 0

        val0Type = ctx.expr(0).type
        val1Type = ctx.expr(0).type
        if (val0Type == "int" or val0Type == "float") and (val1Type == "int" or val1Type == "float"):
            ctx.val = math.floor(ctx.expr(0).val) << math.floor(ctx.expr(1).val)
        elif val0Type == "null" or val1Type == "null":
            ctx.type = "null"
            ctx.val = None

    # expr & expr
    def exitBitAnd(self, ctx):
        ctx.type = "int"
        ctx.size = None
        ctx.id = None
        ctx.tbl = None
        ctx.val = 0

        val0Type = ctx.expr(0).type
        val1Type = ctx.expr(0).type
        if (val0Type == "int" or val0Type == "float") and (val1Type == "int" or val1Type == "float"):
            ctx.val = math.floor(ctx.expr(0).val) & math.floor(ctx.expr(1).val)
        elif val0Type == "null" or val1Type == "null":
            ctx.type = "null"
            ctx.val = None

    # expr | expr
    def exitBitOr(self, ctx):
        ctx.type = "int"
        ctx.size = None
        ctx.id = None
        ctx.tbl = None
        ctx.val = 0

        val0Type = ctx.expr(0).type
        val1Type = ctx.expr(0).type
        if (val0Type == "int" or val0Type == "float") and (val1Type == "int" or val1Type == "float"):
            ctx.val = math.floor(ctx.expr(0).val) | math.floor(ctx.expr(1).val)
        elif val0Type == "null" or val1Type == "null":
            ctx.type = "null"
            ctx.val = None

    # expr < expr
    def exitLessThan(self, ctx):
        ctx.type = "int"
        ctx.size = None
        ctx.id = None
        ctx.tbl = None
        ctx.val = 0

        val0Type = ctx.expr(0).type
        val1Type = ctx.expr(0).type
        if (val0Type == "int" or val0Type == "float") and (val1Type == "int" or val1Type == "float"):
            ctx.val = math.floor(ctx.expr(0).val) < math.floor(ctx.expr(1).val) and 1 or 0
        elif val0Type == "null" or val1Type == "null":
            ctx.type = "null"
            ctx.val = None

    # expr <= expr
    def exitLessThanEqual(self, ctx):
        ctx.type = "int"
        ctx.size = None
        ctx.id = None
        ctx.tbl = None
        ctx.val = 0

        val0Type = ctx.expr(0).type
        val1Type = ctx.expr(0).type
        if (val0Type == "int" or val0Type == "float") and (val1Type == "int" or val1Type == "float"):
            ctx.val = math.floor(ctx.expr(0).val) <= math.floor(ctx.expr(1).val) and 1 or 0
        elif val0Type == "null" or val1Type == "null":
            ctx.type = "null"
            ctx.val = None

    # expr > expr
    def exitGreaterThan(self, ctx):
        ctx.type = "int"
        ctx.size = None
        ctx.id = None
        ctx.tbl = None
        ctx.val = 0

        val0Type = ctx.expr(0).type
        val1Type = ctx.expr(0).type
        if (val0Type == "int" or val0Type == "float") and (val1Type == "int" or val1Type == "float"):
            ctx.val = math.floor(ctx.expr(0).val) > math.floor(ctx.expr(1).val) and 1 or 0
        elif val0Type == "null" or val1Type == "null":
            ctx.type = "null"
            ctx.val = None

    # expr >= expr
    def exitGreaterThanEqual(self, ctx):
        ctx.type = "int"
        ctx.size = None
        ctx.id = None
        ctx.tbl = None
        ctx.val = 0

        val0Type = ctx.expr(0).type
        val1Type = ctx.expr(0).type
        if (val0Type == "int" or val0Type == "float") and (val1Type == "int" or val1Type == "float"):
            ctx.val = math.floor(ctx.expr(0).val) >= math.floor(ctx.expr(1).val) and 1 or 0
        elif val0Type == "null" or val1Type == "null":
            ctx.type = "null"
            ctx.val = None

    # expr = expr
    # expr == expr
    def exitEqual(self, ctx):
        ctx.type = "int"
        ctx.size = None
        ctx.id = None
        ctx.tbl = None
        ctx.val = ctx.expr(0).val == ctx.expr(1).val and 1 or 0

        val0Type = ctx.expr(0).type
        val1Type = ctx.expr(0).type
        if val0Type == "null" or val1Type == "null":
            ctx.type = "null"
            ctx.val = None
    # expr <> expr
    # expr != expr
    def exitNotEqual(self, ctx):
        ctx.type = "int"
        ctx.size = None
        ctx.id = None
        ctx.tbl = None
        ctx.val = ctx.expr(0).val != ctx.expr(1).val and 1 or 0

        val0Type = ctx.expr(0).type
        val1Type = ctx.expr(0).type
        if val0Type == "null" or val1Type == "null":
            ctx.type = "null"
            ctx.val = None
    # expr && expr
    def exitBooleanAnd(self, ctx):
        ctx.type = "int"
        ctx.size = None
        ctx.id = None
        ctx.tbl = None
        ctx.val = 0

        val0Type = ctx.expr(0).type
        val1Type = ctx.expr(0).type
        if (val0Type == "int" or val0Type == "float") and (val1Type == "int" or val1Type == "float"):
            ctx.val = (ctx.expr(0).val and ctx.expr(1).val) and 1 or 0
        elif val0Type == "null" or val1Type == "null":
            ctx.type = "null"
            ctx.val = None

    # expr || expr
    def exitBooleanOr(self, ctx):
        ctx.type = "int"
        ctx.size = None
        ctx.id = None
        ctx.tbl = None
        ctx.val = 0

        val0Type = ctx.expr(0).type
        val1Type = ctx.expr(0).type
        if (val0Type == "int" or val0Type == "float") and ctx.expr(0).val:
            ctx.val = 1
        elif(val1Type == "int" or val1Type == "float") and ctx.expr(1).val:
            ctx.val = 1
        elif val0Type == "null" or val1Type == "null":
            ctx.type = "null"
            ctx.val = None



# =====================================================================================================================
# Database table class: holds schema with data, also contains methods for table manipulation
class DBTable:
    schema = []
    data = []

    def __init__(self, columns):
        self.schema = []
        self.data = []
        for columnName, columnSchema in columns:
            self.schema.append( (columnName, {'type': columnSchema['type'] ,'size': columnSchema['size']}) )

    # Returns schema for specified column
    def getColumnSchema(self, name):
        return dict(self.schema).get(name)

    # Returns location of specified column
    def getColumnIndex(self, name):
        return self.getColumnNames().index(name)

    # Returns column names without schema
    def getColumnNames(self):
        return [v[0] for v in self.schema]

    # Returns tuples of column names and schema
    def getColumns(self):
        return copy.deepcopy(self.schema)

    # Returns lists of lists of rows
    def getRows(self):
        return copy.deepcopy(self.data)

    # Returns lists of dictionaries of rows, each row is indexed by the column name
    def getLabeledRows(self):
        rows = []
        for row in self.data:
            rows.append(self.labelRow(row))
        return rows

    # Labels list of raw data values to dictionary, indexed by column name
    def labelRow(self, row):
        return dict(zip(self.getColumnNames(),row))

    # Resolves an expression with current table
    def resolveExpression(self, expr:SQL457Parser.ExprContext, row=None):
        return resolveExpression(expr, {'self':self.schema}, {'self':row})

    # Adds a column to table
    def appendColumn(self, col):
        if col.name in self.getColumnNames():
            raise DBMSDuplicateColumn(col.name)
        self.schema.append( (col.name, {"type": col.type,"size": col.size}) )

    # Adds multiple columns to the table
    def appendColumns(self, cols):
        for newCol in cols:
            self.appendColumn(newCol)

    # Returns string representation of the table
    def toString(self):
        out = ""

        definitions = []
        for columnName, columnSchema in self.schema:
            if columnSchema["size"]:
                definitions += ["{0} {1}({2})".format(columnName, columnSchema["type"], columnSchema["size"])]
            elif columnSchema["type"]:
                definitions += ["{0} {1}".format(columnName, columnSchema["type"])]
            else:
                definitions += ["{0}".format(columnName)]

        out = "|".join(definitions)

        for r in self.data:
            out += "\n"
            out += ("|".join([ str(c) if not c is None else "" for c in r ]))

        return out

    # Checks value against given schema
    def checkValue(self, columnSchema, value):
        if columnSchema["type"] == "int":
            if value.type != "int" and (value.type != "float" or value.val != math.floor(value.val)):
                raise DBMSTypeMismatch(columnSchema["name"], columnSchema["type"], value.type)
        elif columnSchema["type"] == "float":
            if value.type != "int" and value.type != "float":
                raise DBMSTypeMismatch(columnSchema["name"], columnSchema["type"], value.type)
        elif columnSchema["type"] == "char":
            if value.type != "char":
                raise DBMSTypeMismatch(columnSchema["name"], columnSchema["type"], value.type)
        elif columnSchema["size"] and columnSchema["size"] < value.size:
            raise DBMSValueTooBig(columnSchema["name"], columnSchema["size"], value.size)
        elif columnSchema["type"] == "varchar":
            if value.type != "char":
                raise DBMSTypeMismatch(columnSchema["name"], columnSchema["type"], value.type)

    # Inserts row into the table
    def insert(self, values):
        rowData = []
        for columnName, columnSchema in self.schema:
            v = values.pop(0)
            self.resolveExpression(v)
            self.checkValue(columnSchema, v)
            rowData.append(v.val)

        self.data.append(rowData)
        return 1

    # Deletes rows matching given condition
    def delete(self, expr):
        newRow = []
        removeCount = 0
        for row in self.data:
            if self.resolveExpression(expr, self.labelRow(row)).val:
                removeCount += 1
            else:
                newRow.append(row)

        self.data = newRow
        return removeCount

    # Updates values for rows matching given condition
    def update(self, columns, expr):
        updateCount = 0

        for rowIndex, row in enumerate(self.data):
            if not self.resolveExpression(expr, self.labelRow(row)).val:
                continue

            for updateColumn in columns:
                columnName = updateColumn.identifier().id
                columnSchema = self.getColumnSchema(columnName)
                if not columnSchema:
                    raise DBMSUnknownColumn(updateColumn.identifier().id)

                columnIndex = self.getColumnIndex(columnName)

                newExpr = updateColumn.expr()

                self.resolveExpression(newExpr, self.labelRow(row))
                self.checkValue(columnSchema, newExpr)

                self.data[rowIndex][columnIndex] = newExpr.val
            updateCount += 1



        return updateCount


# =====================================================================================================================
# Main class for database management system
# Manages tables such as loading, creating, and deleting old.
# Also forwards instructions from parser to tables

class DBMS:
    def __init__(self, path):
        self.databases = Path(path)
        self.currentDatabase = None
        self.databases.mkdir(exist_ok=True)

        self.transaction = False
        self.transactionClaim = False
        self.tableTransactions = dict()

    # Creates database in the system
    def createDatabase(self, dbName):
        db = self.databases / dbName

        try:
            db.mkdir()
            logging.info("Database '%s' created." % dbName)
        except FileExistsError:
            logging.error("!Failed to create database '%s' because it already exists." % dbName)

    # Drops database from the system
    def dropDatabase(self, dbName):
        db = self.databases / dbName
        if not db.exists():
            logging.error("!Failed to delete '%s' because it does not exist." % dbName)
            return

        for child in db.iterdir():
            child.unlink()

        if db == self.currentDatabase:
            self.currentDatabase = None

        db.rmdir()
        logging.info("Database '%s' deleted." % dbName)

    # Selects database in the system
    def useDatabase(self, dbName):
        db = self.databases / dbName
        if not db.exists():
            logging.error("!Failed to use database '%s' because it does not exist." % dbName)
            return

        self.currentDatabase = db
        self.databaseLock = db.with_suffix(".lock")

        logging.info("Using database '%s'." % dbName)

    # Read the specified table from a file
    def readTableFile(self, tblName ):
        if self.currentDatabase is None:
            raise DBMSDatabaseMissing()
    
        tblFile = self.currentDatabase / tblName

        if not tblFile.exists():
            raise DBMSTableMissing()

        if self.transaction and tblName in self.tableTransactions:
            tblData = self.tableTransactions[tblName]
            if not tblData:
                raise DBMSTableMissing()

            return tblData
        else:
            return pickle.loads(tblFile.read_bytes())
        
    # Write the table into the file
    def writeTableFile(self, tblName, data ):
        if self.currentDatabase is None:
            raise DBMSDatabaseMissing()
    
        if self.databaseLock.exists() and not self.transactionClaim:
            raise DBMSTableLocked()

        if self.transaction:
            self.tableTransactions[tblName] = data
        else:
            tblFile = self.currentDatabase / tblName
            tblFile.write_bytes(pickle.dumps(data))
        
    # Delete the table file
    def deleteTableFile(self, tblName, data ):
        if self.databaseLock.exists() and not self.transactionClaim:
            raise DBMSTableLocked()

        if self.transaction:
            self.tableTransactions[tblName] = {}
        else:
            tblFile = self.currentDatabase / tblName
            tblFile.unlink()


    # Creates new table in database
    def createTable(self, tblName, columns):
        if self.currentDatabase is None:
            logging.error("!Failed to create table '%s' because database is missing." % tblName)
            return

        tbl = self.currentDatabase / tblName
        if tbl.exists():
            logging.error("!Failed to create table '%s' because it already exists." % tblName)
            return

        try:
            tblData = DBTable([(c.name, {'type':c.type,'size':c.size}) for c in columns])
            self.writeTableFile(tblName, tblData)

            logging.info("Table '%s' created." % tblName)
        except DBMSDatabaseMissing:
            logging.error("!Failed to create table '%s' because database is missing." % tblName)
        except DBMSTableLocked:
            logging.error("Error: Table '%s' is locked!" % tblName)


    # Returns new table with given conditions
    def selectTable(self, resultColumns, tableSources, tableReference):
        # Dictionaries for processing
        allColumns = OrderedDict()
        allRows = {}
        tableNames = []
        tableNamesOuter = set()

        leftOuterJoin = False
        rightOuterJoin = False

        if isinstance(tableReference, SQL457Parser.JoinLeftOuterContext):
            leftOuterJoin = True
        elif isinstance(tableReference, SQL457Parser.JoinRightOuterContext):
            rightOuterJoin = True
        elif isinstance(tableReference, SQL457Parser.JoinFullOuterContext):
            leftOuterJoin = True
            rightOuterJoin = True



        # Check the left tables
        if tableSources:

            # Process source tables
            for source in tableSources:
                if source.alias in tableNames:
                    logging.error("!Failed to query table, ambiguous table name '%s'." % source.alias)
                    return
                
                try:
                    tblData = self.readTableFile(source.tbl)
                except DBMSDatabaseMissing:
                    logging.error("!Failed to query table '%s' because database is missing." % source.tbl)
                    return
                except DBMSTableMissing:
                    logging.error("!Failed to query table '%s' because it does not exist." % source.tbl)
                    return
                
                allRows[source.alias] = list( enumerate(tblData.getLabeledRows()) )
                allColumns[source.alias] = tblData.getColumns()
                tableNames.append(source.alias)
                if leftOuterJoin:
                    tableNamesOuter.add(source.alias)

        # Check the right tables
        if tableReference and hasattr(tableReference, 'tableSource'):

            # Process reference tables
            for source in tableReference.tableSource():
                if source.alias in tableNames:
                    logging.error("!Failed to query table, ambiguous table name '%s'." % source.alias)
                    return

                try:
                    tblData = self.readTableFile(source.tbl)
                except DBMSDatabaseMissing:
                    logging.error("!Failed to query table '%s' because database is missing." % source.tbl)
                    return
                except DBMSTableMissing:
                    logging.error("!Failed to query table '%s' because it does not exist." % source.tbl)
                    return
                
                allRows[source.alias] = list( enumerate(tblData.getLabeledRows()) )
                allColumns[source.alias] = tblData.getColumns()
                tableNames.append(source.alias)
                if rightOuterJoin:
                    tableNamesOuter.add(source.alias)

        try:
            # Generate columns
            newColumns = []
            for column in resultColumns:
                if column.everything:
                    # Add all columns of all referenced tables
                    for tblName, tblColumns in allColumns.items():
                        for c in tblColumns:
                            newColumns.append( (c, None) )

                elif column.table:
                    # Add all columns of specific table
                    columnTableName = column.identifier().id
                    if not columnTableName in tableNames:
                        raise DBMSUnknownTable(tableName)

                    for c in allColumns[columnTableName]:
                        newColumns.append( (c, None) )
                else:
                    # Individual columns
                    newColmExpr = column.expr()
                    resolveExpression(newColmExpr, allColumns)
                    if newColmExpr.type == "id":
                        # Identifier
                        if newColmExpr.tbl:
                            if not newColmExpr.tbl in tableNames:
                                raise DBMSUnknownTable(tableName)

                            columnSchema = dict(allColumns[newColmExpr.tbl]).get(newColmExpr.id)

                            if not columnSchema:
                                raise DBMSUnknownColumn(newColmExpr.val)


                            newColumns.append( ((newColmExpr.val,columnSchema), column) ) 
                        else:
                            tmpColumn = None
                            for tblName, columns in allColumns.items():
                                columnsDict =  dict(columns)
                                if newColmExpr.id in columnsDict:
                                    tmpColumn = columnsDict[newColmExpr.id]
                                    break

                            if tmpColumn:
                                logging.debug(tmpColumn)
                                newColumns.append(((newColmExpr.id, tmpColumn), column))
                            else:
                                raise DBMSUnknownColumn("%s" % (newColmExpr.id))

                    else:
                        # Expression Column
                        newColumns.append( ((getCtxString(newColmExpr),{"type": None,"size": None}), column) )

            # Generate the table
            newTable = DBTable([v[0] for v in newColumns])
            matches = []


            # Setup tracker for skipped rows
            # If gap is greater than 1, it will populate the table with missing outer rows
            outerTracker = dict([(tblName, -1) for tblName in tableNamesOuter])
            def checkOuter(currentRows):
                for tblName, rowNum in outerTracker.items():
                    for rowIndex in range(rowNum,currentRows[tblName]-1):
                        row = {tblName: allRows[tblName][rowIndex][1]}
                        matches.append(row)
                        logging.debug(">> OUTER\t%s %s %s" % (row,rowNum,currentRows[tblName]))
                    outerTracker[tblName] = currentRows[tblName]


            # Find table matches
            for rowSet in itertools.product(*allRows.values()):
                if not rowSet:
                    matches.append({})
                    continue
                (indexes, unnumberedRows) = zip(*rowSet)
                tableIndexedRows = dict(zip(tableNames, unnumberedRows))

                checkOuter(dict(zip(tableNames,indexes)))

                ok = 1
                if hasattr(tableReference, 'expr'):
                    ok = resolveExpression(tableReference.expr(), allColumns, tableIndexedRows).val

                if ok:
                    matches.append(tableIndexedRows)
                    logging.debug(">> MATCHED\t%s\t%s" % (tableIndexedRows,indexes))
                else:
                    logging.debug(">>\t\t%s\t%s" % (tableIndexedRows,indexes))

            # Check for remaining rows
            checkOuter(dict([(tblName, len(rows)+1) for tblName, rows in allRows.items()]))

            # Transfer matches into our new table
            for match in matches:
                row = []

                for column, ctx in newColumns:
                    if isinstance(ctx, SQL457Parser.ResultColumnContext) and ctx.expr():
                        row.append( resolveExpression(ctx.expr(), allColumns, match).val )
                    elif not ctx is None:
                        row.append( match[ctx][column[0]] )
                    else:
                        foundRow = None
                        for tblName, r in match.items():
                            if not r.get(column[0]) is None:
                                foundRow = r.get(column[0])
                                break
                        row.append( foundRow )
                              
                newTable.data.append(row)

            logging.debug("")
            logging.debug(">> Table Schema\t%s" % newTable.schema)
            logging.debug(">> Table Data\t%s" % newTable.data)
            return newTable

        except DBMSUnknownColumn as exp:
            logging.error("!Failed to query because can't resolve unknown column '%s'." % (exp.args))
            return
        except DBMSUnknownTable as exp:
            logging.error("!Failed to query because can't resolve unknown table '%s'." % (exp.args))
            return

    # Drops specified table from the database
    def dropTable(self, tblName):
        try:
            deleteTableFile(tblName)
            logging.info("Table %s deleted." % tblName)
        except DBMSDatabaseMissing:
            logging.error("!Failed to delete table '%s' because database is missing." % tblName)
        except DBMSTableMissing:
            logging.error("!Failed to delete '%s' because it does not exist." % tblName)
        except DBMSTableLocked:
            logging.error("Error: Table '%s' is locked!" % tblName)

        
    # Add additional columns for specified table
    def alterTable(self, tblName, columns):
        try:
            tblData = self.readTableFile(tblName)
            tblData.appendColumns(columns)
            self.writeTableFile(tblName, tblData)
            logging.info("Table %s modified." % tblName)

        except DBMSDatabaseMissing:
            logging.error("!Failed to alter table '%s' because database is missing." % tblName)
        except DBMSTableMissing:
            logging.error("!Failed to alter table '%s' because it does not exist." % tblName)
        except DBMSTableLocked:
            logging.error("Error: Table '%s' is locked!" % tblName)
        except DBMSDuplicateColumn as exp:
            logging.error("!Failed to alter table '%s' because table already contains '%s' column." % (tblName, exp))

    
    # Insert data for specified table
    def insert(self, tblName, values):
        try:
            tblData = self.readTableFile(tblName)
            count = tblData.insert( values )
            self.writeTableFile(tblName, tblData)
            logging.info("%i new record inserted." % count)
        
        except DBMSDatabaseMissing:
            logging.error("!Failed to insert into table '%s' because database is missing." % tblName)
        except DBMSTableMissing:
            logging.error("!Failed to insert into table '%s' because table does not exist." % tblName)
        except DBMSTableLocked:
            logging.error("Error: Table '%s' is locked!" % tblName)
        except DBMSTypeMismatch as exp:
            logging.error("!Failed to insert into table '%s' because types are incompatible in column '%s' (%s != %s)." % (tblName, *exp.args))
        except DBMSValueTooBig as exp:
            logging.error("!Failed to insert into table '%s' because value is too big in column '%s' (max: %i, received: %i)." % (tblName, *exp.args))

    # Deletes data with given condition from specified table
    def delete(self, tblName, expr):
        try:
            tblData = self.readTableFile(tblName)
            count = tblData.delete( expr )
            self.writeTableFile(tblName, tblData)

            if count>1:
                logging.info("%i records deleted." % count)
            else:
                logging.info("%i record deleted." % count)
        
        except DBMSDatabaseMissing:
            logging.error("!Failed to delete from table '%s 'because database is missing." % tblName)
        except DBMSTableMissing:
            logging.error("!Failed to delete from table '%s' because table does not exist." % tblName)
        except DBMSTableLocked:
            logging.error("Error: Table '%s' is locked!" % tblName)
        except DBMSUnknownColumn as exp:
            logging.error("!Failed to delete from table '%s' because can't resolve unknown column '%s'." % (tblName, *exp.args))


    # Updates table values matching specified condition
    def update(self, tblName, columns, expr):
        try:
            tblData = self.readTableFile(tblName)
            count = tblData.update(columns, expr)
            self.writeTableFile(tblName, tblData)

            if count>1:
                logging.info("%i records modified." % count)
            else:
                logging.info("%i record modified." % count)
        
        except DBMSDatabaseMissing:
            logging.error("!Failed to update table '%s' because database is missing." % tblName)
        except DBMSTableMissing:
            logging.error("!Failed to update table '%s' because table does not exist." % tblName)
        except DBMSTableLocked:
            logging.error("Error: Table '%s' is locked!" % tblName)
        except DBMSTypeMismatch as exp:
            logging.error("!Failed to update table '%s' because types are incompatible in column '%s' (%s != %s)." % (tblName, *exp.args))
        except DBMSUnknownColumn as exp:
            logging.error("!Failed to update table '%s' because can't resolve unknown column '%s'." % (tblName, *exp.args))

    # Locks the table
    def beginTransaction(self):
        if self.currentDatabase is None:
            logging.error("!Failed to start transaction because database is missing." )
            return
        
        if self.transaction:
            logging.error("!Failed to start transaction because transaction was already started.")
            return

        lockFile = self.databaseLock

        try:
            self.tableTransactions = {}
            self.transaction = True
            Path.touch(lockFile, exist_ok=False)
            self.transactionClaim = True
        except FileExistsError:
            pass

        logging.info("Transaction starts.")

    # Makes changes, and unlocks the table
    def commit(self):
        if self.currentDatabase is None:
            logging.error("!Failed to commit table '%s' because database is missing.")
            return

        if not self.transaction:
            logging.error("!Failed to commit because no transaction was started.")
            return

        self.transaction = False

        if not self.tableTransactions:
            logging.error("Transaction abort.")
            return

        self.transactionClaim = False
        self.databaseLock.unlink()

        for k, v in self.tableTransactions.items():
            if v:
                self.writeTableFile(k, v)
            else:
                self.deleteTableFile(k)


        logging.info("Transaction committed.")

# =====================================================================================================================
# This is an executive part of the parser.
# As the tree is traversed, the nodes specified in this class
# are being called, which are then executes methods within DBMS.

class SQL457MyVisitor(SQL457Visitor):
    def __init__(self, dbms):
        self.dbms = dbms

    def visitSqlStmtList(self, ctx:SQL457Parser.SqlStmtListContext):
        self.visitChildren(ctx)

    def visitSqlStmt(self, ctx:SQL457Parser.SqlStmtContext):
        if ctx.getChildCount():
            logging.debug("\n>> QUERY: %s" % re.sub(r'\s\s\s*', " ", getCtxString(ctx)))
        
        self.visitChildren(ctx)
    def visitCreateDatabaseStmt(self, ctx):
        self.dbms.createDatabase(ctx.identifier().id)

    def visitDropDatabaseStmt(self, ctx):
        self.dbms.dropDatabase(ctx.identifier().id)

    def visitUseStmt(self, ctx):
        self.dbms.useDatabase(ctx.identifier().id)

    def visitCreateTableStmt(self, ctx:SQL457Parser.CreateTableStmtContext):
        self.dbms.createTable(ctx.identifier().id, ctx.columnDef())

    def visitDropTableStmt(self, ctx:SQL457Parser.DropTableStmtContext):
        self.dbms.dropTable(ctx.identifier().id)

    def visitSelectStmt(self, ctx):
        table = self.dbms.selectTable(ctx.resultColumn(), ctx.tableSource(), ctx.tableReference())
        if table:
            logging.info(table.toString())

    def visitAlterTableStmt(self, ctx):
        self.dbms.alterTable(ctx.identifier().id, ctx.columnDef())

    def visitInsertStmt(self, ctx):
        self.dbms.insert(ctx.identifier().id, ctx.expr())

    def visitUpdateStmt(self, ctx):
        self.dbms.update(ctx.identifier().id, ctx.updateColumn(), ctx.expr())

    def visitDeleteStmt(self, ctx):
        self.dbms.delete(ctx.identifier().id, ctx.expr())

    def visitBeginTransactionStmt(self, ctx):
        self.dbms.beginTransaction()

    def visitCommitStmt(self, ctx):
        self.dbms.commit()

# =====================================================================================================================
# Tree walker listener, used to resolve static values within the tree.
# It is automatically executed once the program starts.
# This is purely used for optimization purposes as these values only 
# need to be processed once during runtime.
class SQL457MyListener(SQL457Listener):

    # Abstracted literal value (int, float, string, etc.)
    def exitLiteralValue(self, ctx):
        child = ctx.getChild(0)

        ctx.val = child.val
        ctx.type = child.type
        ctx.size = child.size

    # Integer Type
    def exitLiteralInteger(self, ctx):
        ctx.type = "int"
        ctx.size = None
        if ctx.getText().lower() == "true":
            ctx.val = 1
        elif ctx.getText().lower() == "false":
            ctx.val = 0
        else:
            ctx.val = int(ctx.getText())

    # String Type
    def exitLiteralString(self, ctx):
        text = str(ctx.getText())
        if text[0] == "\"":
            text = text[1:-1]
            text = text.replace("\"\"","\"")
        elif text[0] == "'":
            text = text[1:-1]
            text = text.replace("''","'")

        ctx.val = text
        ctx.type = "char"
        ctx.size = len(text)

    # Float Type
    def exitLiteralFloat(self, ctx):
        ctx.val = float(ctx.getText())
        ctx.type = "float"
        ctx.size = None

    # Null Type
    def exitLiteralNull(self, ctx):
        ctx.val = None
        ctx.type = None
        ctx.type = None

    # Identifier type (for tables, columns, database names, etc.)
    def exitIdentifier(self, ctx):
        ctx.id = ctx.getText().strip("[]").lower()
        ctx.val = None
        ctx.type = None
        ctx.size = None

    # Column definitions
    def exitColumnDef(self, ctx):
        ctx.name = ctx.identifier().id

        if ctx.columnType() is not None:
            ctx.type = ctx.columnType().getText()
            ctx.size = None
        else:
            ctx.type = ctx.columnTypeArg().getText()
            ctx.size = int(ctx.columnSize().literalInteger().val)

    # Tables, specifically for 'insert' query where tables have aliases
    def exitTableSource(self, ctx):
        ctx.tbl = ctx.tbl.id
        if ctx.alias is not None:
            ctx.alias = ctx.alias.id
        else:
            ctx.alias = ctx.tbl



# =====================================================================================================================
# Parser Error handling: This stops parsing process as soon as first error is detected

class SQL457ParserError(Exception):
    pass


class MyErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise SQL457ParserError(str(line) + ":" + str(column) + ": syntax error, " + str(msg))

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambAlts, configs):
        pass

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        pass

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        raise SQL457ParserError("Context error, " + str(configs))




# =====================================================================================================================
# Main: Initializes the database and maintains infinite loop for user input.

if __name__ == '__main__':
    myDatabase = DBMS("./.dbs")

    re_stmt_end = re.compile('.*;\s*$',re.DOTALL)

    stmt = ""
    # Accept user input until end-of-file
    while True:
        try:
            stmt += input()
        except (EOFError, KeyboardInterrupt):
            logging.info("All done.")
            exit()

        # Buffer the input until semicolon is at the end of string
        if not re_stmt_end.match(stmt):
            stmt += "\n"
            continue
        
        try:
            # Prepare the parser
            lexer = SQL457Lexer(InputStream(stmt))
            lexer._listeners = [MyErrorListener()]
            stream = CommonTokenStream(lexer)

            parser = SQL457Parser(stream)
            parser._listeners = [MyErrorListener()]

            root = parser.sqlStmtList()

            # Resolves static values in the tree
            walker = ParseTreeWalker()
            treeOptimizer = SQL457MyListener()
            walker.walk(treeOptimizer, root)

            # Run the visitor on the parsed tree
            visitor = SQL457MyVisitor(myDatabase)
            visitor.visit(root)

            # Reset input
            stmt = ""
        except SQL457ParserError as exp:
            logging.error("!Failed to parse query => %s" % exp)
            stmt = ""
