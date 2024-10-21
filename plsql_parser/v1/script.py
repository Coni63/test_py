import re

from itertools import cycle
from pathlib import Path

import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network


def remove_block_comment(code: str) -> str:
    regex = r"/\*[\s\S]*?\*/"
    return re.sub(regex, '', code, flags=re.MULTILINE)

def remove_single_line_comment(code: str) -> str:
    # regex = r"^.*(--.*)$"
    regex = r"(.*?)(--.*$)"
    # return re.sub(regex, '', code, flags=re.MULTILINE)
    return re.sub(regex, r'\1', code, flags=re.MULTILINE)

def extract_function(pl_sql_code: str, package_name: str) -> list:

    # Updated regular expressions for matching functions and procedures
    function_pattern = re.compile(r'(?i)(?:CREATE\s+(?:OR\s+REPLACE\s+)?)?FUNCTION\s+(\w+)', re.MULTILINE)
    procedure_pattern = re.compile(r'(?i)(?:CREATE\s+(?:OR\s+REPLACE\s+)?)?PROCEDURE\s+(\w+)', re.MULTILINE)
    
    # Find all functions and procedures
    functions = function_pattern.finditer(pl_sql_code)
    procedures = procedure_pattern.finditer(pl_sql_code)
    
    results = []

    for match in list(functions) + list(procedures):
        name = match.group(1)
        start = match.start()
        
        # Find the corresponding END
        end_match = re.search(r'(?i)\bEND\s+' + re.escape(name) + r'\s*;', pl_sql_code[start:])
        if end_match:
            end = start + end_match.end()
            body = pl_sql_code[start:end]
            
            # Check if it has BEGIN/END
            has_begin_end = 'BEGIN' in body.upper() and 'END' in body.upper()
            
            # Determine if it's a function or procedure
            type_ = 'FUNCTION' if 'FUNCTION' in body.upper() else 'PROCEDURE'
            
            results.append({
                'name': f"{package_name}.{name}",
                'type': type_,
                'has_begin_end': has_begin_end,
                'body': body.strip()
            })
    return results

def extract_function_call(package_content: str, package_name: str):
    call_pattern = re.compile(r'(\w+\.)?(\w+)\s*\(', re.IGNORECASE)            
    calls = []
    for call_match in call_pattern.finditer(package_content):
        package_prefix = call_match.group(1)
        function_name = call_match.group(2)
        if package_prefix:
            calls.append(f"{package_prefix}{function_name}")
        else:
            calls.append(f"{package_name}.{function_name}")
    return list(set(calls))


def extract_tables(plsql_function: str) -> list[str]:
    # Convert to uppercase for case-insensitive matching
    plsql_function = plsql_function.upper()
    
    # Patterns to match table names in various SQL contexts
    patterns = [
        r'\bFROM\s+(\w+)',                  # SELECT ... FROM table
        r'\bJOIN\s+(\w+)',                  # JOIN table
        r'\bUPDATE\s+(\w+)',                # UPDATE table
        r'\bINTO\s+(\w+)',                  # INSERT INTO table
        r'\bDELETE\s+FROM\s+(\w+)',         # DELETE FROM table
        r'\bALTER\s+TABLE\s+(\w+)',         # ALTER TABLE table
        r'\bCREATE\s+TABLE\s+(\w+)',        # CREATE TABLE table
        r'\bDROP\s+TABLE\s+(\w+)',          # DROP TABLE table
        r'\bTRUNCATE\s+TABLE\s+(\w+)',      # TRUNCATE TABLE table
        r':(\w+)%ROWTYPE',                  # variable_name table%ROWTYPE
        r'\bTABLE\s*\(\s*(\w+)',            # TABLE(table_name) for collection expressions
    ]
    
    tables = set()
    
    for pattern in patterns:
        matches = re.findall(pattern, plsql_function)
        tables.update(matches)
    
    # Remove common SQL keywords that might be mistaken for table names
    keywords = {'SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'UNION', 'MINUS', 'INTERSECT', 'ORDER', 'GROUP', 'HAVING', 'BY', 'ASC', 'DESC'}
    tables = tables - keywords
    
    return sorted(list(tables))

def prune_and_convert_to_graph(all_procedures: list[dict]) -> list[dict]:
    package_function = {x["name"] for x in all_procedures}
    
    # remove std libs calls
    for proc in all_procedures:
        new_proc = []
        for x in proc["calls"]:
            if x in package_function:
                new_proc.append(x)
            else:
                print(f"filtered {x}")
        proc["calls"] = new_proc

    #remove the body function
    return [{k: v for k, v in record.items() if k != "body"} for record in all_procedures]


def plot_dependency_graph(dependency_dict):
    # Create a directed graph
    G = nx.DiGraph()

    # Available colors excluding red (you can adjust this list)
    available_colors = cycle(['blue', 'green', 'purple', 'orange', 'yellow', 'pink', 'cyan', 'brown'])
    module_colors = {}  # Dictionary to store assigned color for each module

    # Add nodes and edges
    for func in dependency_dict:
        G.add_node(func["name"], color='blue', type='function')
        for called_func in func['calls']:
            module_name, function = called_func.split(".", maxsplit=1)

            # Assign a color to the module if it's not already assigned
            if module_name not in module_colors:
                module_colors[module_name] = next(available_colors)

            G.add_node(called_func, color=module_colors[module_name], type='function')
            G.add_edge(func["name"], called_func)
        for table in func['tables']:
            G.add_node(table, color='red', type='table')
            G.add_edge(func["name"], table)

    # nx.write_gexf(G, "test.gexf")  # use gephi after

    nx.draw(G, with_labels = True)
    nt = Network('100vh', '100vw')
    nt.from_nx(G)
    nt.show('nx.html', notebook=False)


def main():
    all_procedures = []
    for file in Path("codebase").glob("*.pkb"):
        package_name = file.stem
        try:
            code = file.read_text().lower()
            
            code = remove_block_comment(code)
            code = remove_single_line_comment(code)

            analysis_results = extract_function(code, package_name)

            for item in analysis_results:
                item["calls"] = extract_function_call(item['body'], package_name)
                item["tables"] = extract_tables(item['body'])

            all_procedures += analysis_results
            print(package_name, "OK")
        except Exception as e:
            print(package_name, f"FAIL: {e}")

    filtered_procedures = prune_and_convert_to_graph(all_procedures)
    plot_dependency_graph(filtered_procedures)

if __name__ == "__main__":
    main()