from src.tool import tool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
load_dotenv()

class FileWriter(BaseModel):
    file_name:str=Field(...,description="The name of the file to be created.",example=['example.txt'])
    content:str=Field(...,description="The content to be written to the file.",example=['Hello, World!'])

@tool("File Writer Tool",args_schema=FileWriter)
def file_writer_tool(file_name:str,content:str):
    '''
    Creates a new file with the given name and writes the provided content to it.
    '''
    try:
        with open(file_name,"w") as file:
            file.write(content)
        return f"File {file_name} created successfully."
    except Exception as err:
        return f"Error: {err}"

