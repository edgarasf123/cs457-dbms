# Generated from ./SQL457.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .SQL457Parser import SQL457Parser
else:
    from SQL457Parser import SQL457Parser

# This class defines a complete generic visitor for a parse tree produced by SQL457Parser.

class SQL457Visitor(ParseTreeVisitor):

    # Visit a parse tree produced by SQL457Parser#sqlStmtList.
    def visitSqlStmtList(self, ctx:SQL457Parser.SqlStmtListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#sqlStmt.
    def visitSqlStmt(self, ctx:SQL457Parser.SqlStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#createDatabaseStmt.
    def visitCreateDatabaseStmt(self, ctx:SQL457Parser.CreateDatabaseStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#dropDatabaseStmt.
    def visitDropDatabaseStmt(self, ctx:SQL457Parser.DropDatabaseStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#useStmt.
    def visitUseStmt(self, ctx:SQL457Parser.UseStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#createTableStmt.
    def visitCreateTableStmt(self, ctx:SQL457Parser.CreateTableStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#dropTableStmt.
    def visitDropTableStmt(self, ctx:SQL457Parser.DropTableStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#selectStmt.
    def visitSelectStmt(self, ctx:SQL457Parser.SelectStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#beginTransactionStmt.
    def visitBeginTransactionStmt(self, ctx:SQL457Parser.BeginTransactionStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#commitStmt.
    def visitCommitStmt(self, ctx:SQL457Parser.CommitStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#where.
    def visitWhere(self, ctx:SQL457Parser.WhereContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#joinInner.
    def visitJoinInner(self, ctx:SQL457Parser.JoinInnerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#joinLeftOuter.
    def visitJoinLeftOuter(self, ctx:SQL457Parser.JoinLeftOuterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#joinRightOuter.
    def visitJoinRightOuter(self, ctx:SQL457Parser.JoinRightOuterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#joinFullOuter.
    def visitJoinFullOuter(self, ctx:SQL457Parser.JoinFullOuterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#empty.
    def visitEmpty(self, ctx:SQL457Parser.EmptyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#tableSource.
    def visitTableSource(self, ctx:SQL457Parser.TableSourceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#resultColumn.
    def visitResultColumn(self, ctx:SQL457Parser.ResultColumnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#alterTableStmt.
    def visitAlterTableStmt(self, ctx:SQL457Parser.AlterTableStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#insertStmt.
    def visitInsertStmt(self, ctx:SQL457Parser.InsertStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#updateStmt.
    def visitUpdateStmt(self, ctx:SQL457Parser.UpdateStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#updateColumn.
    def visitUpdateColumn(self, ctx:SQL457Parser.UpdateColumnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#deleteStmt.
    def visitDeleteStmt(self, ctx:SQL457Parser.DeleteStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#columnDef.
    def visitColumnDef(self, ctx:SQL457Parser.ColumnDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#add.
    def visitAdd(self, ctx:SQL457Parser.AddContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#inverse.
    def visitInverse(self, ctx:SQL457Parser.InverseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#lessThanEqual.
    def visitLessThanEqual(self, ctx:SQL457Parser.LessThanEqualContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#greaterThanEqual.
    def visitGreaterThanEqual(self, ctx:SQL457Parser.GreaterThanEqualContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#bitOr.
    def visitBitOr(self, ctx:SQL457Parser.BitOrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#subtract.
    def visitSubtract(self, ctx:SQL457Parser.SubtractContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#column.
    def visitColumn(self, ctx:SQL457Parser.ColumnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#notEqual.
    def visitNotEqual(self, ctx:SQL457Parser.NotEqualContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#concat.
    def visitConcat(self, ctx:SQL457Parser.ConcatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#paranthesis.
    def visitParanthesis(self, ctx:SQL457Parser.ParanthesisContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#equal.
    def visitEqual(self, ctx:SQL457Parser.EqualContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#negative.
    def visitNegative(self, ctx:SQL457Parser.NegativeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#shiftRight.
    def visitShiftRight(self, ctx:SQL457Parser.ShiftRightContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#shiftLeft.
    def visitShiftLeft(self, ctx:SQL457Parser.ShiftLeftContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#bitAnd.
    def visitBitAnd(self, ctx:SQL457Parser.BitAndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#lessThan.
    def visitLessThan(self, ctx:SQL457Parser.LessThanContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#divide.
    def visitDivide(self, ctx:SQL457Parser.DivideContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#booleanOr.
    def visitBooleanOr(self, ctx:SQL457Parser.BooleanOrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#multiply.
    def visitMultiply(self, ctx:SQL457Parser.MultiplyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#value.
    def visitValue(self, ctx:SQL457Parser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#modulo.
    def visitModulo(self, ctx:SQL457Parser.ModuloContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#greaterThan.
    def visitGreaterThan(self, ctx:SQL457Parser.GreaterThanContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#booleanAnd.
    def visitBooleanAnd(self, ctx:SQL457Parser.BooleanAndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#columnSize.
    def visitColumnSize(self, ctx:SQL457Parser.ColumnSizeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#columnType.
    def visitColumnType(self, ctx:SQL457Parser.ColumnTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#columnTypeArg.
    def visitColumnTypeArg(self, ctx:SQL457Parser.ColumnTypeArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#identifier.
    def visitIdentifier(self, ctx:SQL457Parser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#literalValue.
    def visitLiteralValue(self, ctx:SQL457Parser.LiteralValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#literalInteger.
    def visitLiteralInteger(self, ctx:SQL457Parser.LiteralIntegerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#literalFloat.
    def visitLiteralFloat(self, ctx:SQL457Parser.LiteralFloatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#literalString.
    def visitLiteralString(self, ctx:SQL457Parser.LiteralStringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQL457Parser#literalNull.
    def visitLiteralNull(self, ctx:SQL457Parser.LiteralNullContext):
        return self.visitChildren(ctx)



del SQL457Parser