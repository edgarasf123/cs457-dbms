// Author: Edgaras Fiodorovas
// Date:   12-13-2018

grammar SQL457;

sqlStmtList
 : sqlStmt ( ';' sqlStmt )* EOF
;

sqlStmt
 :(createDatabaseStmt
 | dropDatabaseStmt
 | useStmt
 | createTableStmt
 | dropTableStmt
 | selectStmt
 | alterTableStmt
 | insertStmt
 | updateStmt
 | deleteStmt
 | beginTransactionStmt
 | commitStmt
 | /*empty*/)
;

// CREATE DATABASE
createDatabaseStmt
 : K_CREATE K_DATABASE identifier
;

// DROP DATABASE
dropDatabaseStmt
 : K_DROP K_DATABASE identifier
;

// USE
useStmt
 : K_USE identifier
;

// CREATE TABLE
createTableStmt
 : K_CREATE K_TABLE identifier '(' columnDef ( ',' columnDef )* ')'
;

// DROP TABLE
dropTableStmt
 : K_DROP K_TABLE identifier
;

// SELECT
selectStmt
 : K_SELECT resultColumn (',' resultColumn)* (K_FROM tableSource (','tableSource)* tableReference)?
;

// BEGIN
beginTransactionStmt
 : K_BEGIN K_TRANSACTION
;

// COMMIT
commitStmt
 : K_COMMIT
;

tableReference
 :K_WHERE expr # where
 |K_INNER K_JOIN tableSource (','tableSource)* (K_ON expr)? # joinInner
 |K_LEFT K_OUTER? K_JOIN tableSource (','tableSource)* (K_ON expr)? # joinLeftOuter
 |K_RIGHT K_OUTER? K_JOIN tableSource (','tableSource)* (K_ON expr)? # joinRightOuter
 |K_FULL K_OUTER? K_JOIN tableSource (','tableSource)* (K_ON expr)? # joinFullOuter
 | # empty
;

tableSource
 : tbl=identifier
 | tbl=identifier alias=identifier
;


resultColumn
 : expr
 | everything='*'
 | table=identifier '.' '*'
;

// ALTER TABLE
alterTableStmt
 : K_ALTER K_TABLE identifier K_ADD (
    columnDef
    | ( '(' columnDef ( ',' columnDef )* ')' )
 )
;

// INSERT
insertStmt
 : K_INSERT K_INTO identifier K_VALUES '(' expr ( ',' expr )* ')'
;

// UPDATE
updateStmt
 : K_UPDATE identifier K_SET updateColumn (',' updateColumn)* K_WHERE expr
;

updateColumn
 : identifier '=' expr
;

// DELETE
deleteStmt
 : K_DELETE K_FROM identifier K_WHERE expr
;


// Other
columnDef
 : identifier ( columnType | (columnTypeArg '(' columnSize ')' ) )
;


expr
 : '(' expr ')'		# paranthesis
 | column=identifier	# column
 | table=identifier '.' column=identifier # column
 | literalValue		# value
 | expr '||' expr 	# concat
 | expr '*' expr 	# multiply
 | expr '/' expr 	# divide
 | expr '%' expr 	# modulo
 | expr '+' expr 	# add
 | expr '-' expr 	# subtract
 | expr '<<' expr 	# shiftRight
 | expr '>>' expr 	# shiftLeft
 | expr '&' expr 	# bitAnd
 | expr '|' expr 	# bitOr
 | expr '<' expr 	# lessThan
 | expr '<=' expr 	# lessThanEqual
 | expr '>' expr 	# greaterThan
 | expr '>=' expr 	# greaterThanEqual
 | expr '=' expr 	# equal
 | expr '==' expr 	# equal
 | expr '!=' expr 	# notEqual
 | expr '<>' expr 	# notEqual
 | expr K_AND expr 	# booleanAnd
 | expr K_OR expr 	# booleanOr
 | K_NOT expr		# inverse
 | '-' expr			# negative
;



columnSize : literalInteger ;

columnType
 : T_INT
 | T_VARCHAR
 | T_CHAR
 | T_FLOAT
;

columnTypeArg
 : T_VARCHAR
 | T_CHAR
;

identifier
 : IDENTIFIER
;

literalValue
 : literalInteger
 | literalFloat
 | literalString
 | literalNull
;


literalInteger: INTEGER | K_TRUE | K_FALSE;
literalFloat: FLOAT;
literalString: STRING_LITERAL;
literalNull: K_NULL;

// Lexer Rules

T_INT : I N T;
T_CHAR : C H A R;
T_VARCHAR : V A R C H A R;
T_FLOAT : F L O A T;

K_COMMIT : C O M M I T;
K_BEGIN : B E G I N;
K_TRANSACTION : T R A N S A C T I O N;
K_NOT : N O T;
K_NULL : N U L L;
K_TRUE : T R U E;
K_FALSE : F A L S E;
K_AND : A N D;
K_OR : O R;
K_USE : U S E;
K_ADD : A D D;
K_SET : S E T;
K_ALTER : A L T E R;
K_CREATE : C R E A T E;
K_DATABASE : D A T A B A S E;
K_UPDATE : U P D A T E;
K_DELETE : D E L E T E;
K_DROP : D R O P;
K_FROM : F R O M;
K_INSERT : I N S E R T;
K_INTO : I N T O;
K_TABLE : T A B L E;
K_SELECT : S E L E C T;
K_VALUES : V A L U E S;
K_WHERE : W H E R E;
K_INNER : I N N E R;
K_OUTER : O U T E R;
K_JOIN : J O I N;
K_LEFT : L E F T;
K_RIGHT : R I G H T;
K_FULL : F U L L;
K_ON : O N;



EQUAL : '=';
LESS_THAN : '<';
LESS_THAN_EQUAL : LESS_THAN EQUAL;
GREATER_THAN : '>';
GREATER_THAN_EQUAL : GREATER_THAN EQUAL;



FLOAT : DIGIT+ '.' DIGIT+;
INTEGER : DIGIT+;

IDENTIFIER
 : [a-zA-Z_] [a-zA-Z_0-9]*
 | '[' [a-zA-Z_] [a-zA-Z_0-9]* ']'
;

STRING_LITERAL
 : '\'' (~ '\'' | '\'\'' | '\\\'' )* '\''
 | '"' ( ~'"' | '""' | '\\"' )* '"'
;


SINGLE_LINE_COMMENT
 : '--' ~[\r\n]* -> channel(HIDDEN)
;

MULTILINE_COMMENT
 : '/*' .*? ( '*/' | EOF ) -> channel(HIDDEN)
;

SPACES
 : [ \u000B\t\r\n] -> channel(HIDDEN)
;


fragment DIGIT : [0-9];

fragment A : [aA];
fragment B : [bB];
fragment C : [cC];
fragment D : [dD];
fragment E : [eE];
fragment F : [fF];
fragment G : [gG];
fragment H : [hH];
fragment I : [iI];
fragment J : [jJ];
fragment K : [kK];
fragment L : [lL];
fragment M : [mM];
fragment N : [nN];
fragment O : [oO];
fragment P : [pP];
fragment Q : [qQ];
fragment R : [rR];
fragment S : [sS];
fragment T : [tT];
fragment U : [uU];
fragment V : [vV];
fragment W : [wW];
fragment X : [xX];
fragment Y : [yY];
fragment Z : [zZ];