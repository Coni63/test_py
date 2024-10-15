from dependancies.PlSqlParserListener import PlSqlParserListener
from node import Node

class DependencyListener(PlSqlParserListener):
    def __init__(self):
        # Dictionary to store procedures and the functions/procedures they call
        self.procedure_calls = {}
        # Variable to keep track of the current procedure name
        self.current_procedure = []

    # def enterProcedure_name(self, ctx):
    #     # Capture the name of the procedure
    #     self.current_procedure = ctx.getText()
    #     print(f"Entering procedure: {self.current_procedure}")
        
    #     # Initialize the list of calls for this procedure
    #     if self.current_procedure not in self.procedure_calls:
    #         self.procedure_calls[self.current_procedure] = []

    # def exitProcedure_name(self, ctx):
    #     # Clear the current procedure when exiting
    #     print(f"Exiting procedure: {self.current_procedure}")
    #     self.current_procedure = None

    def enterCreate_procedure_body(self, ctx):
        # Capture the name of the procedure when we enter the body
        procedure_name = ctx.procedure_name().getText()
        self.current_procedure.append(procedure_name)
        print(f"Entering procedure body: {self.current_procedure[-1]}")
        
        # Initialize the list of function/procedure calls for this procedure
        if self.current_procedure[-1] not in self.procedure_calls:
            self.procedure_calls[self.current_procedure[-1]] = Node()

    # Exiting the procedure body (after the "END" statement)
    def exitCreate_procedure_body(self, ctx):
        print(f"Exiting procedure body: {self.current_procedure}")
        self.current_procedure.pop()

    def enterFunction_name(self, ctx):
        # Capture function calls inside a procedure
        function_name = ctx.getText()
        if self.current_procedure:
            print(f"Function '{function_name}' called inside procedure '{self.current_procedure[-1]}'")
            # Add the function to the list of functions called within the current procedure
            self.procedure_calls[self.current_procedure[-1]].func.append(function_name)

    # def exitFunction_name(self, ctx):
    #     print(f"Exiting function: {self.current_procedure}")
    #     self.current_procedure.pop()


    def enterRoutine_name(self, ctx):
        # Capture procedure or function calls inside a procedure
        if self.current_procedure:
            call_text = ctx.getText()
            print(f"Call statement found: {call_text} inside procedure {self.current_procedure}")
            
            # Add the called function/procedure to the current procedure's list of calls
            self.procedure_calls[self.current_procedure[-1]].proc.append(call_text)
        else:
            # print(ctx.getText())
            print("Something is wrong")


    def enterTableview_name(self, ctx):
        # Capture table names
        # if self.current_procedure:
        table_name = ctx.getText()
        print(f"Table accessed: {table_name}")
        
        if self.current_procedure:
            # Add the called function/procedure to the current procedure's list of calls
            self.procedure_calls[self.current_procedure[-1]].table.append(table_name)

    def enterUpdate_statement(self, ctx):
        print(f"enterUpdate_statement")

    def enterCreate_function_body(self, ctx):
        # Capture the name of the procedure when we enter the body
        procedure_name = ctx.function_name().getText()
        self.current_procedure.append(procedure_name)
        print(f"Entering function body: {self.current_procedure}")
        # Initialize the list of function/procedure calls for this procedure
        if self.current_procedure[-1] not in self.procedure_calls:
            self.procedure_calls[self.current_procedure[-1]] = Node()

    def exitCreate_function_body(self, ctx):
        print(f"exitCreate_function_body")
        if self.current_procedure:
            self.current_procedure.pop()