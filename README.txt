==================================================================================================
# Author: Edgaras Fiodorovas
# Date:   12-14-2018
==================================================================================================
Language: 
    python3
Run Command:
    python pa4.py < PA4_test.sql
==================================================================================================
If you want to use SQL keyword as identifier of database, table, or column name, you have to
suround it in the brackets.

For instance: 
	create database [database]
	use [database]
==================================================================================================
The implementation is using antlr4 parsing library, the grammar is defined in SQL457.g4
Note: The submission archive already has compiled grammar, no need to run this command.

To compile the grammar language, execute following command:
    java -jar ./grammar/antlr-4.7.1-complete.jar -Dlanguage=Python3 -visitor -o ./grammar ./SQL457.g4
==================================================================================================
