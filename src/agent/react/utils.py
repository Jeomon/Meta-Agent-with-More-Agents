import re
import ast

def extract_llm_response(response: str) -> dict:
    # Initialize variables to store extracted information
    result = {
        'Thought': None,
        'Action Name': None,
        'Action Input': None,
        'Query': None,
        'Final Answer': None,
        'Route': None
    }

    # Define regular expressions for different parts of the response
    thought_regex = re.compile(r'<Thought>\s*(.*?)\s*</Thought>', re.DOTALL)
    action_name_regex = re.compile(r'<Action Name>\s*(.*?)\s*</Action Name>', re.DOTALL)
    action_input_regex = re.compile(r'<Action Input>\s*(\{.*?\})\s*</Action Input>', re.DOTALL)
    query_regex = re.compile(r'<Query>\s*(.*?)\s*</Query>', re.DOTALL)
    final_answer_regex = re.compile(r'<Final Answer>\s*(.*?)\s*</Final Answer>', re.DOTALL)
    route_regex = re.compile(r'<Route>\s*(.*?)\s*</Route>', re.DOTALL)

    # Extract Thought
    thought_match = thought_regex.search(response)
    if thought_match:
        result['Thought'] = thought_match.group(1).strip()

    # Extract Action Name
    action_name_match = action_name_regex.search(response)
    if action_name_match:
        result['Action Name'] = action_name_match.group(1).strip()

    # Extract Action Input
    action_input_match = action_input_regex.search(response)
    if action_input_match:
        action_input_str = action_input_match.group(1).strip()
        try:
            result['Action Input'] = ast.literal_eval(action_input_str)
        except (ValueError, SyntaxError):
            result['Action Input'] = action_input_str  # If parsing fails, keep it as a string

    # Extract Query
    query_match = query_regex.search(response)
    if query_match:
        result['Query'] = query_match.group(1).strip()

    # Extract Final Answer
    final_answer_match = final_answer_regex.search(response)
    if final_answer_match:
        result['Final Answer'] = final_answer_match.group(1).strip()

    # Extract Route
    route_match = route_regex.search(response)
    if route_match:
        result['Route'] = route_match.group(1).strip()

    return result

def read_markdown_file(file_path: str) -> str:
    with open(file_path, 'r',encoding='utf-8') as f:
        markdown_content = f.read()
    return markdown_content