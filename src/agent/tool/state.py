from typing import TypedDict,Annotated,Optional
from src.message import BaseMessage

class AgentState(TypedDict):
    input:str
    route:str
    tool_data:dict
    error:str
    output:str