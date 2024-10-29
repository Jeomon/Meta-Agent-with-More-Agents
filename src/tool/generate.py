from src.agent.tool.utils import read_markdown_file
from src.message import HumanMessage,SystemMessage
from src.inference import BaseInference
import ast

def generate(query:str,llm:BaseInference):
    system_prompt = read_markdown_file('./src/agent/tool/prompt/generate.md')
    user_prompt = f'**Query:**\n`{query}`'
    system_message = SystemMessage(system_prompt)
    human_message = HumanMessage(user_prompt)
    messages = [system_message, human_message]
    tool_data = llm.invoke(messages, json=True)
    error = ''
    while True:
        try:
            ast.parse(tool_data.content.get('tool'))
            error = ''
            break
        except Exception as e:
            error = e
            print(f'Error: {error}')
            messages.append(HumanMessage(error))
            tool_data = llm.invoke(messages, json=True)
    return {
        'name': tool_data.content.get('name'),
        'tool_name': tool_data.content.get('tool_name'),
        'tool': tool_data.content.get('tool')
    }