import re

def extract_llm_response(xml_output):
    # Dictionary to store extracted data
    response_data = {
        "Route": None,
        "Thought": None,
        "Observation": None,
        "Final Answer": None,
        "Reflection": None
    }
    # Define regex patterns for each field
    route_pattern = re.compile(r'<Route>(.*?)</Route>', re.DOTALL)
    thought_pattern = re.compile(r'<Thought>(.*?)</Thought>', re.DOTALL)
    observation_pattern = re.compile(r'<Observation>(.*?)</Observation>', re.DOTALL)
    final_answer_pattern = re.compile(r'<Final-Answer>(.*?)</Final-Answer>', re.DOTALL)
    reflection_pattern = re.compile(r'<Reflection>(.*?)</Reflection>', re.DOTALL)

    # Extract values based on the patterns
    route_match = route_pattern.search(xml_output)
    thought_match = thought_pattern.search(xml_output)
    observation_match = observation_pattern.search(xml_output)
    final_answer_match = final_answer_pattern.search(xml_output)
    reflection_match = reflection_pattern.search(xml_output)

    # Populate the dictionary if values are found
    if route_match:
        response_data['Route'] = route_match.group(1).strip()

        # Based on Route, extract the rest of the data
        if response_data['Route'] == "Reason":
            if thought_match:
                response_data['Thought'] = thought_match.group(1).strip()
            if observation_match:
                response_data['Observation'] = observation_match.group(1).strip()

        elif response_data['Route'] == "Answer":
            if thought_match:
                response_data['Thought'] = thought_match.group(1).strip()
            if final_answer_match:
                response_data['Final Answer'] = final_answer_match.group(1).strip()

        elif response_data['Route'] == "Reflection":
            if thought_match:
                response_data['Thought'] = thought_match.group(1).strip()
            if reflection_match:
                response_data['Reflection'] = reflection_match.group(1).strip()
    return response_data

def read_markdown_file(file_path: str) -> str:
    with open(file_path, 'r',encoding='utf-8') as f:
        markdown_content = f.read()
    return markdown_content