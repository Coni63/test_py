poetry install
poetry run java -jar antlr-4.13.2-complete.jar -Dlanguage=Python3 PlSqlLexer.g4
poetry run java -jar antlr-4.13.2-complete.jar -Dlanguage=Python3 PlSqlParser.g4

https://github.com/antlr/grammars-v4/tree/master/sql/plsql
https://github.com/antlr/antlr4
