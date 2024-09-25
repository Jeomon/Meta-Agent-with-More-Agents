from pydantic import BaseModel,Field
from src.tool import tool

class UserInteraction(BaseModel):
    question: str = Field(..., description="The question you want to ask the user.", example="Hello, how are you?")

@tool('User Interaction Tool',args_schema=UserInteraction)
def user_interface_tool(question:str):
    '''
    The best way to interact with the user for clarification or asking questions and taking inputs from the user.
    '''
    ai_query=f'AI: {question}\nUser: '
    user_message=input(ai_query)
    return user_message