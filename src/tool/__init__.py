from pydantic import BaseModel
from inspect import getdoc
from textwrap import dedent
import ast

def tool(name:str,args_schema:BaseModel):
    def wrapper(func):
        func.name = name
        func.schema = args_schema.model_json_schema()
        func.schema.pop('title')
        func.description = getdoc(func)
        return func
    return wrapper

def extract_tools_from_module(location:str):
    with open(location,'r') as f:
        tree=ast.parse(f.read())
    tool_definitions=[]
    models_defintions=[]
    tool_names=[]
    func_names=[]
    tools=[]
    for node in tree.body:
        if isinstance(node,ast.FunctionDef):
            func_names.append(node.name)
            tool_definitions.append(ast.unparse(node))
            for decorator in node.decorator_list:
                if isinstance(decorator,ast.Call):
                    tool_names.append(ast.unparse(decorator.args))
        if isinstance(node,ast.ClassDef):
            models_defintions.append(ast.unparse(node))
    for i in range(len(tool_names)):
        tools.append({'tool_name':tool_names[i].replace('\'',''),
        'tool':models_defintions[i]+'\n\n'+tool_definitions[i],
        'func_name':func_names[i]})
    return tools

def tool_to_ast(tool_def:str):
    tool_name = None
    func_name = None
    func_doc = None
    try:
        node=ast.parse(tool_def)
        for node in ast.walk(node):
            if isinstance(node, ast.FunctionDef):
                func_name = node.name  # Function name
                func_doc = ast.get_docstring(node)  # Function docstring (documentation)
                # Traverse decorators
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name):
                        decorator_name = decorator.func.id
                        decorator_args = [arg.s for arg in decorator.args if isinstance(arg, ast.Str)]
                        if decorator_args:
                            tool_name = decorator_args[0]
        return {'tool_name': tool_name, 'func_name': func_name, 'description': func_doc, 'tool': tool_def}
    except SyntaxError as error:
        return {'error': str(error)}
    
def save_tool_to_module(location: str, tool:str):
    with open(location,'a',encoding='utf-8') as f:
        f.write(f"{dedent(tool)}\n\n")

def remove_tool_from_module(location: str, tool_data: dict):
    # Load the module contents
    with open(location, 'r') as f:
        module = f.read()
    # Parse the module contents into an AST
    tree = ast.parse(module)
    nodes=tree.body
    drop_nodes=[]
    for index,node in enumerate(nodes):
        if isinstance(node, ast.ClassDef) and node.name == tool_data['name'].replace(' Tool',''):
            drop_nodes.append(node)
        elif isinstance(node, ast.FunctionDef) and node.name == tool_data['tool_name']:
            drop_nodes.append(node)
    nodes=[node for node in nodes if node not in drop_nodes]
    # Write the updated module contents back to the file
    with open(location, 'w') as f:
        updated_module = ast.unparse(nodes)
        f.write(f'{updated_module}\n\n')