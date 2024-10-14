import antlr4
from antlr4.tree.Tree import ParseTreeWalker

from dependancies.PlSqlLexer import PlSqlLexer
from dependancies.PlSqlParser import PlSqlParser
from listener import DependencyListener


# Read the PL/SQL code from a file
def parse_plsql_code(plsql_code):
    input_stream = antlr4.InputStream(plsql_code)
    lexer = PlSqlLexer(input_stream)
    stream = antlr4.CommonTokenStream(lexer)

    parser = PlSqlParser(stream)

    tree = parser.sql_script()
    # tree = parser.compilation_unit()
    # tree = parser.procedure_body()
    # tree = parser.unit_statement()
    # tree = parser.block()
    
    return tree, parser


# Example PL/SQL code
# plsql_code = """
# CREATE OR REPLACE PROCEDURE example_proc IS
# BEGIN
#    example_func();
#    SELECT * INTO some_var FROM some_table;
# END;
# """

# with open("module.sql", "r") as f:
#     plsql_code = f.read()


plsql_code = """
/*
TEST COMMENT
*/
CREATE OR REPLACE PROCEDURE proc_A IS
BEGIN
   proc_B();            -- Procedure call
   some_func();         -- Function call
END;

CREATE OR REPLACE PROCEDURE proc_B IS
BEGIN
   another_func();       -- Function call
   update_test_table_func();  -- Function call
END;

CREATE OR REPLACE FUNCTION update_test_table_func RETURN VARCHAR2 IS
BEGIN
   RETURN 'Table updated successfully';
END;
"""

# Parse code to tree
tree, parser = parse_plsql_code(plsql_code)
print(tree.toStringTree(recog=parser))

# walk and structure dependancies
walker = ParseTreeWalker()
listener = DependencyListener()
walker.walk(listener, tree)

print("Procedure calls:")
for procedure, functions in listener.procedure_calls.items():
    print(f"{procedure} calls: {functions}")