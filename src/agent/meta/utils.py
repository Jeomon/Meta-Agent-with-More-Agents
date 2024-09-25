import xml.etree.ElementTree as ET

def extract_from_xml(xml_string):
    # Parse the XML string
    try:
        root = ET.fromstring(xml_string)
    except ET.ParseError as e:
        return {"error": str(e)}
    
    # Initialize the result dictionary
    result = {
        'Agent Name': None,
        'Agent Description': None,
        'Agent Query': None,
        'Tasks': [],
        'Tool': None,
        'Answer': None
    }
    
    # Check if root tag is "Agent"
    if root.tag == "Agent":
        # Extract Agent Name
        agent_name = root.find("./Agent-Name")
        if agent_name is not None:
            result['Agent Name'] = agent_name.text.strip()
        
        # Extract Agent Description
        agent_description = root.find("./Agent-Description")
        if agent_description is not None:
            result['Agent Description'] = agent_description.text.strip()
        
        # Extract Agent Query
        agent_query = root.find("./Agent-Query")
        if agent_query is not None:
            result['Agent Query'] = agent_query.text.strip()
        
        # Extract Tasks
        tasks = root.findall("./Tasks/Task")
        for task in tasks:
            if task is not None and task.text:
                result['Tasks'].append(task.text.strip())
        
        # Extract Tool (if present)
        tool = root.find("./Tool")
        if tool is not None:
            tool_info = {}
            tool_name = tool.find("Tool-Name")
            tool_description = tool.find("Tool-Description")
            if tool_name is not None:
                tool_info['Tool Name'] = tool_name.text.strip()
            if tool_description is not None:
                tool_info['Tool Description'] = tool_description.text.strip()
            result['Tool'] = tool_info
    
    # Check if root tag is "Final-Answer"
    elif root.tag == "Final-Answer":
        result['Answer'] = root.text.strip()
    return result

def read_markdown_file(file_path: str) -> str:
    with open(file_path, 'r',encoding='utf-8') as f:
        markdown_content = f.read()
    return markdown_content