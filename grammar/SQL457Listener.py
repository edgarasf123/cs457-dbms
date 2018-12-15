# Generated from ./SQL457.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .SQL457Parser import SQL457Parser
else:
    from SQL457Parser import SQL457Parser

# This class defines a complete listener for a parse tree produced by SQL457Parser.
class SQL457Listener(ParseTreeListener):

    # Enter a parse tree produced by SQL457Parser#sqlStmtList.
    def enterSqlStmtList(self, ctx:SQL457Parser.SqlStmtListContext):
        pass

    # Exit a parse tree produced by SQL457Parser#sqlStmtList.
    def exitSqlStmtList(self, ctx:SQL457Parser.SqlStmtListContext):
        pass


    # Enter a parse tree produced by SQL457Parser#sqlStmt.
    def enterSqlStmt(self, ctx:SQL457Parser.SqlStmtContext):
        pass

    # Exit a parse tree produced by SQL457Parser#sqlStmt.
    def exitSqlStmt(self, ctx:SQL457Parser.SqlStmtContext):
        pass


    # Enter a parse tree produced by SQL457Parser#createDatabaseStmt.
    def enterCreateDatabaseStmt(self, ctx:SQL457Parser.CreateDatabaseStmtContext):
        pass

    # Exit a parse tree produced by SQL457Parser#createDatabaseStmt.
    def exitCreateDatabaseStmt(self, ctx:SQL457Parser.CreateDatabaseStmtContext):
        pass


    # Enter a parse tree produced by SQL457Parser#dropDatabaseStmt.
    def enterDropDatabaseStmt(self, ctx:SQL457Parser.DropDatabaseStmtContext):
        pass

    # Exit a parse tree produced by SQL457Parser#dropDatabaseStmt.
    def exitDropDatabaseStmt(self, ctx:SQL457Parser.DropDatabaseStmtContext):
        pass


    # Enter a parse tree produced by SQL457Parser#useStmt.
    def enterUseStmt(self, ctx:SQL457Parser.UseStmtContext):
        pass

    # Exit a parse tree produced by SQL457Parser#useStmt.
    def exitUseStmt(self, ctx:SQL457Parser.UseStmtContext):
        pass


    # Enter a parse tree produced by SQL457Parser#createTableStmt.
    def enterCreateTableStmt(self, ctx:SQL457Parser.CreateTableStmtContext):
        pass

    # Exit a parse tree produced by SQL457Parser#createTableStmt.
    def exitCreateTableStmt(self, ctx:SQL457Parser.CreateTableStmtContext):
        pass


    # Enter a parse tree produced by SQL457Parser#dropTableStmt.
    def enterDropTableStmt(self, ctx:SQL457Parser.DropTableStmtContext):
        pass

    # Exit a parse tree produced by SQL457Parser#dropTableStmt.
    def exitDropTableStmt(self, ctx:SQL457Parser.DropTableStmtContext):
        pass


    # Enter a parse tree produced by SQL457Parser#selectStmt.
    def enterSelectStmt(self, ctx:SQL457Parser.SelectStmtContext):
        pass

    # Exit a parse tree produced by SQL457Parser#selectStmt.
    def exitSelectStmt(self, ctx:SQL457Parser.SelectStmtContext):
        pass


    # Enter a parse tree produced by SQL457Parser#beginTransactionStmt.
    def enterBeginTransactionStmt(self, ctx:SQL457Parser.BeginTransactionStmtContext):
        pass

    # Exit a parse tree produced by SQL457Parser#beginTransactionStmt.
    def exitBeginTransactionStmt(self, ctx:SQL457Parser.BeginTransactionStmtContext):
        pass


    # Enter a parse tree produced by SQL457Parser#commitStmt.
    def enterCommitStmt(self, ctx:SQL457Parser.CommitStmtContext):
        pass

    # Exit a parse tree produced by SQL457Parser#commitStmt.
    def exitCommitStmt(self, ctx:SQL457Parser.CommitStmtContext):
        pass


    # Enter a parse tree produced by SQL457Parser#where.
    def enterWhere(self, ctx:SQL457Parser.WhereContext):
        pass

    # Exit a parse tree produced by SQL457Parser#where.
    def exitWhere(self, ctx:SQL457Parser.WhereContext):
        pass


    # Enter a parse tree produced by SQL457Parser#joinInner.
    def enterJoinInner(self, ctx:SQL457Parser.JoinInnerContext):
        pass

    # Exit a parse tree produced by SQL457Parser#joinInner.
    def exitJoinInner(self, ctx:SQL457Parser.JoinInnerContext):
        pass


    # Enter a parse tree produced by SQL457Parser#joinLeftOuter.
    def enterJoinLeftOuter(self, ctx:SQL457Parser.JoinLeftOuterContext):
        pass

    # Exit a parse tree produced by SQL457Parser#joinLeftOuter.
    def exitJoinLeftOuter(self, ctx:SQL457Parser.JoinLeftOuterContext):
        pass


    # Enter a parse tree produced by SQL457Parser#joinRightOuter.
    def enterJoinRightOuter(self, ctx:SQL457Parser.JoinRightOuterContext):
        pass

    # Exit a parse tree produced by SQL457Parser#joinRightOuter.
    def exitJoinRightOuter(self, ctx:SQL457Parser.JoinRightOuterContext):
        pass


    # Enter a parse tree produced by SQL457Parser#joinFullOuter.
    def enterJoinFullOuter(self, ctx:SQL457Parser.JoinFullOuterContext):
        pass

    # Exit a parse tree produced by SQL457Parser#joinFullOuter.
    def exitJoinFullOuter(self, ctx:SQL457Parser.JoinFullOuterContext):
        pass


    # Enter a parse tree produced by SQL457Parser#empty.
    def enterEmpty(self, ctx:SQL457Parser.EmptyContext):
        pass

    # Exit a parse tree produced by SQL457Parser#empty.
    def exitEmpty(self, ctx:SQL457Parser.EmptyContext):
        pass


    # Enter a parse tree produced by SQL457Parser#tableSource.
    def enterTableSource(self, ctx:SQL457Parser.TableSourceContext):
        pass

    # Exit a parse tree produced by SQL457Parser#tableSource.
    def exitTableSource(self, ctx:SQL457Parser.TableSourceContext):
        pass


    # Enter a parse tree produced by SQL457Parser#resultColumn.
    def enterResultColumn(self, ctx:SQL457Parser.ResultColumnContext):
        pass

    # Exit a parse tree produced by SQL457Parser#resultColumn.
    def exitResultColumn(self, ctx:SQL457Parser.ResultColumnContext):
        pass


    # Enter a parse tree produced by SQL457Parser#alterTableStmt.
    def enterAlterTableStmt(self, ctx:SQL457Parser.AlterTableStmtContext):
        pass

    # Exit a parse tree produced by SQL457Parser#alterTableStmt.
    def exitAlterTableStmt(self, ctx:SQL457Parser.AlterTableStmtContext):
        pass


    # Enter a parse tree produced by SQL457Parser#insertStmt.
    def enterInsertStmt(self, ctx:SQL457Parser.InsertStmtContext):
        pass

    # Exit a parse tree produced by SQL457Parser#insertStmt.
    def exitInsertStmt(self, ctx:SQL457Parser.InsertStmtContext):
        pass


    # Enter a parse tree produced by SQL457Parser#updateStmt.
    def enterUpdateStmt(self, ctx:SQL457Parser.UpdateStmtContext):
        pass

    # Exit a parse tree produced by SQL457Parser#updateStmt.
    def exitUpdateStmt(self, ctx:SQL457Parser.UpdateStmtContext):
        pass


    # Enter a parse tree produced by SQL457Parser#updateColumn.
    def enterUpdateColumn(self, ctx:SQL457Parser.UpdateColumnContext):
        pass

    # Exit a parse tree produced by SQL457Parser#updateColumn.
    def exitUpdateColumn(self, ctx:SQL457Parser.UpdateColumnContext):
        pass


    # Enter a parse tree produced by SQL457Parser#deleteStmt.
    def enterDeleteStmt(self, ctx:SQL457Parser.DeleteStmtContext):
        pass

    # Exit a parse tree produced by SQL457Parser#deleteStmt.
    def exitDeleteStmt(self, ctx:SQL457Parser.DeleteStmtContext):
        pass


    # Enter a parse tree produced by SQL457Parser#columnDef.
    def enterColumnDef(self, ctx:SQL457Parser.ColumnDefContext):
        pass

    # Exit a parse tree produced by SQL457Parser#columnDef.
    def exitColumnDef(self, ctx:SQL457Parser.ColumnDefContext):
        pass


    # Enter a parse tree produced by SQL457Parser#add.
    def enterAdd(self, ctx:SQL457Parser.AddContext):
        pass

    # Exit a parse tree produced by SQL457Parser#add.
    def exitAdd(self, ctx:SQL457Parser.AddContext):
        pass


    # Enter a parse tree produced by SQL457Parser#inverse.
    def enterInverse(self, ctx:SQL457Parser.InverseContext):
        pass

    # Exit a parse tree produced by SQL457Parser#inverse.
    def exitInverse(self, ctx:SQL457Parser.InverseContext):
        pass


    # Enter a parse tree produced by SQL457Parser#lessThanEqual.
    def enterLessThanEqual(self, ctx:SQL457Parser.LessThanEqualContext):
        pass

    # Exit a parse tree produced by SQL457Parser#lessThanEqual.
    def exitLessThanEqual(self, ctx:SQL457Parser.LessThanEqualContext):
        pass


    # Enter a parse tree produced by SQL457Parser#greaterThanEqual.
    def enterGreaterThanEqual(self, ctx:SQL457Parser.GreaterThanEqualContext):
        pass

    # Exit a parse tree produced by SQL457Parser#greaterThanEqual.
    def exitGreaterThanEqual(self, ctx:SQL457Parser.GreaterThanEqualContext):
        pass


    # Enter a parse tree produced by SQL457Parser#bitOr.
    def enterBitOr(self, ctx:SQL457Parser.BitOrContext):
        pass

    # Exit a parse tree produced by SQL457Parser#bitOr.
    def exitBitOr(self, ctx:SQL457Parser.BitOrContext):
        pass


    # Enter a parse tree produced by SQL457Parser#subtract.
    def enterSubtract(self, ctx:SQL457Parser.SubtractContext):
        pass

    # Exit a parse tree produced by SQL457Parser#subtract.
    def exitSubtract(self, ctx:SQL457Parser.SubtractContext):
        pass


    # Enter a parse tree produced by SQL457Parser#column.
    def enterColumn(self, ctx:SQL457Parser.ColumnContext):
        pass

    # Exit a parse tree produced by SQL457Parser#column.
    def exitColumn(self, ctx:SQL457Parser.ColumnContext):
        pass


    # Enter a parse tree produced by SQL457Parser#notEqual.
    def enterNotEqual(self, ctx:SQL457Parser.NotEqualContext):
        pass

    # Exit a parse tree produced by SQL457Parser#notEqual.
    def exitNotEqual(self, ctx:SQL457Parser.NotEqualContext):
        pass


    # Enter a parse tree produced by SQL457Parser#concat.
    def enterConcat(self, ctx:SQL457Parser.ConcatContext):
        pass

    # Exit a parse tree produced by SQL457Parser#concat.
    def exitConcat(self, ctx:SQL457Parser.ConcatContext):
        pass


    # Enter a parse tree produced by SQL457Parser#paranthesis.
    def enterParanthesis(self, ctx:SQL457Parser.ParanthesisContext):
        pass

    # Exit a parse tree produced by SQL457Parser#paranthesis.
    def exitParanthesis(self, ctx:SQL457Parser.ParanthesisContext):
        pass


    # Enter a parse tree produced by SQL457Parser#equal.
    def enterEqual(self, ctx:SQL457Parser.EqualContext):
        pass

    # Exit a parse tree produced by SQL457Parser#equal.
    def exitEqual(self, ctx:SQL457Parser.EqualContext):
        pass


    # Enter a parse tree produced by SQL457Parser#negative.
    def enterNegative(self, ctx:SQL457Parser.NegativeContext):
        pass

    # Exit a parse tree produced by SQL457Parser#negative.
    def exitNegative(self, ctx:SQL457Parser.NegativeContext):
        pass


    # Enter a parse tree produced by SQL457Parser#shiftRight.
    def enterShiftRight(self, ctx:SQL457Parser.ShiftRightContext):
        pass

    # Exit a parse tree produced by SQL457Parser#shiftRight.
    def exitShiftRight(self, ctx:SQL457Parser.ShiftRightContext):
        pass


    # Enter a parse tree produced by SQL457Parser#shiftLeft.
    def enterShiftLeft(self, ctx:SQL457Parser.ShiftLeftContext):
        pass

    # Exit a parse tree produced by SQL457Parser#shiftLeft.
    def exitShiftLeft(self, ctx:SQL457Parser.ShiftLeftContext):
        pass


    # Enter a parse tree produced by SQL457Parser#bitAnd.
    def enterBitAnd(self, ctx:SQL457Parser.BitAndContext):
        pass

    # Exit a parse tree produced by SQL457Parser#bitAnd.
    def exitBitAnd(self, ctx:SQL457Parser.BitAndContext):
        pass


    # Enter a parse tree produced by SQL457Parser#lessThan.
    def enterLessThan(self, ctx:SQL457Parser.LessThanContext):
        pass

    # Exit a parse tree produced by SQL457Parser#lessThan.
    def exitLessThan(self, ctx:SQL457Parser.LessThanContext):
        pass


    # Enter a parse tree produced by SQL457Parser#divide.
    def enterDivide(self, ctx:SQL457Parser.DivideContext):
        pass

    # Exit a parse tree produced by SQL457Parser#divide.
    def exitDivide(self, ctx:SQL457Parser.DivideContext):
        pass


    # Enter a parse tree produced by SQL457Parser#booleanOr.
    def enterBooleanOr(self, ctx:SQL457Parser.BooleanOrContext):
        pass

    # Exit a parse tree produced by SQL457Parser#booleanOr.
    def exitBooleanOr(self, ctx:SQL457Parser.BooleanOrContext):
        pass


    # Enter a parse tree produced by SQL457Parser#multiply.
    def enterMultiply(self, ctx:SQL457Parser.MultiplyContext):
        pass

    # Exit a parse tree produced by SQL457Parser#multiply.
    def exitMultiply(self, ctx:SQL457Parser.MultiplyContext):
        pass


    # Enter a parse tree produced by SQL457Parser#value.
    def enterValue(self, ctx:SQL457Parser.ValueContext):
        pass

    # Exit a parse tree produced by SQL457Parser#value.
    def exitValue(self, ctx:SQL457Parser.ValueContext):
        pass


    # Enter a parse tree produced by SQL457Parser#modulo.
    def enterModulo(self, ctx:SQL457Parser.ModuloContext):
        pass

    # Exit a parse tree produced by SQL457Parser#modulo.
    def exitModulo(self, ctx:SQL457Parser.ModuloContext):
        pass


    # Enter a parse tree produced by SQL457Parser#greaterThan.
    def enterGreaterThan(self, ctx:SQL457Parser.GreaterThanContext):
        pass

    # Exit a parse tree produced by SQL457Parser#greaterThan.
    def exitGreaterThan(self, ctx:SQL457Parser.GreaterThanContext):
        pass


    # Enter a parse tree produced by SQL457Parser#booleanAnd.
    def enterBooleanAnd(self, ctx:SQL457Parser.BooleanAndContext):
        pass

    # Exit a parse tree produced by SQL457Parser#booleanAnd.
    def exitBooleanAnd(self, ctx:SQL457Parser.BooleanAndContext):
        pass


    # Enter a parse tree produced by SQL457Parser#columnSize.
    def enterColumnSize(self, ctx:SQL457Parser.ColumnSizeContext):
        pass

    # Exit a parse tree produced by SQL457Parser#columnSize.
    def exitColumnSize(self, ctx:SQL457Parser.ColumnSizeContext):
        pass


    # Enter a parse tree produced by SQL457Parser#columnType.
    def enterColumnType(self, ctx:SQL457Parser.ColumnTypeContext):
        pass

    # Exit a parse tree produced by SQL457Parser#columnType.
    def exitColumnType(self, ctx:SQL457Parser.ColumnTypeContext):
        pass


    # Enter a parse tree produced by SQL457Parser#columnTypeArg.
    def enterColumnTypeArg(self, ctx:SQL457Parser.ColumnTypeArgContext):
        pass

    # Exit a parse tree produced by SQL457Parser#columnTypeArg.
    def exitColumnTypeArg(self, ctx:SQL457Parser.ColumnTypeArgContext):
        pass


    # Enter a parse tree produced by SQL457Parser#identifier.
    def enterIdentifier(self, ctx:SQL457Parser.IdentifierContext):
        pass

    # Exit a parse tree produced by SQL457Parser#identifier.
    def exitIdentifier(self, ctx:SQL457Parser.IdentifierContext):
        pass


    # Enter a parse tree produced by SQL457Parser#literalValue.
    def enterLiteralValue(self, ctx:SQL457Parser.LiteralValueContext):
        pass

    # Exit a parse tree produced by SQL457Parser#literalValue.
    def exitLiteralValue(self, ctx:SQL457Parser.LiteralValueContext):
        pass


    # Enter a parse tree produced by SQL457Parser#literalInteger.
    def enterLiteralInteger(self, ctx:SQL457Parser.LiteralIntegerContext):
        pass

    # Exit a parse tree produced by SQL457Parser#literalInteger.
    def exitLiteralInteger(self, ctx:SQL457Parser.LiteralIntegerContext):
        pass


    # Enter a parse tree produced by SQL457Parser#literalFloat.
    def enterLiteralFloat(self, ctx:SQL457Parser.LiteralFloatContext):
        pass

    # Exit a parse tree produced by SQL457Parser#literalFloat.
    def exitLiteralFloat(self, ctx:SQL457Parser.LiteralFloatContext):
        pass


    # Enter a parse tree produced by SQL457Parser#literalString.
    def enterLiteralString(self, ctx:SQL457Parser.LiteralStringContext):
        pass

    # Exit a parse tree produced by SQL457Parser#literalString.
    def exitLiteralString(self, ctx:SQL457Parser.LiteralStringContext):
        pass


    # Enter a parse tree produced by SQL457Parser#literalNull.
    def enterLiteralNull(self, ctx:SQL457Parser.LiteralNullContext):
        pass

    # Exit a parse tree produced by SQL457Parser#literalNull.
    def exitLiteralNull(self, ctx:SQL457Parser.LiteralNullContext):
        pass


