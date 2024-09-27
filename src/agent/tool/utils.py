import ast
from textwrap import dedent

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

def update_tool_to_module(location: str, tool_data: dict):
    # Load the module contents
    with open(location, 'r') as f:
        module = f.read()
    # Parse the module contents into an AST
    tree = ast.parse(module)
    nodes=tree.body
    tool_model,tool_definition=tool_data.get('tool').split('\n\n')
    for index,node in enumerate(nodes):
        if isinstance(node, ast.ClassDef) and node.name == tool_data['name'].replace(' Tool',''):
            nodes[index]=ast.parse(tool_model)
        elif isinstance(node, ast.FunctionDef) and node.name == tool_data['tool_name']:
            nodes[index]=ast.parse(tool_definition)
    # Write the updated module contents back to the file
    with open(location, 'w') as f:
        updated_module = ast.unparse(nodes)
        f.write(f'{updated_module}\n\n')

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

def save_tool_to_module(location: str, tool_data: dict):
    with open(location,'a',encoding='utf-8') as f:
        f.write(f"{dedent(tool_data.get('tool'))}\n\n")

def read_markdown_file(file_path: str) -> str:
    with open(file_path, 'r',encoding='utf-8') as f:
        markdown_content = f.read()
    return markdown_content