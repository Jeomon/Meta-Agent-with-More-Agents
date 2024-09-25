import xml.etree.ElementTree as ET
import re

def extract_from_xml(xml_output):
    """
    Extracts information from the COT agent output based on the options (Reasoning, Answer, Reflection).
    Returns a dictionary containing relevant data from the XML response.
    """

    # Dictionary to store extracted data
    response_data = {
        "Route": None,
        "Thought": None,
        "Observation": None,
        "Final Answer": None,
        "Reflection": None
    }
    #Extract the option tag from the XML string
    option_tag_pattern = re.compile(r'(<Option>.*?</Option>)', re.DOTALL)
    match = option_tag_pattern.search(xml_output)
    # Parse the XML string
    root = ET.fromstring(match.group(1))

    # Check if it's Option 1 (Reasoning and Observation)
    if root.find(".//Route").text == "Reason":
        response_data['Route'] = "Reason"
        response_data['Thought'] = root.find(".//Thought").text.strip()
        response_data['Observation'] = root.find(".//Observation").text.strip()

    # Check if it's Option 2 (Providing the Final Answer)
    elif root.find(".//Route").text == "Answer":
        response_data['Route'] = "Answer"
        response_data['Thought'] = root.find(".//Thought").text.strip()
        response_data['Final Answer'] = root.find(".//Final-Answer").text.strip()

    # Check if it's Option 3 (Reflection and Self-Assessment)
    elif root.find(".//Route").text == "Reflection":
        response_data['Route'] = "Reflection"
        response_data['Thought'] = root.find(".//Thought").text.strip()
        response_data['Reflection'] = root.find(".//Reflection").text.strip()

    return response_data

def read_markdown_file(file_path: str) -> str:
    with open(file_path, 'r',encoding='utf-8') as f:
        markdown_content = f.read()
    return markdown_content