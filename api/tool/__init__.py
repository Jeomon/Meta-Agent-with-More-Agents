from src.tool import tool_to_ast,save_tool_to_module,remove_tool_from_module
from fastapi import APIRouter,status,Depends
from src.inference.groq import ChatGroq
from src.tool.generate import generate
from pydantic import BaseModel,Field
from sqlmodel import Session,select
from api.init_database import engine
from api.models import Tool,User
from api.user import get_current_user
from dotenv import load_dotenv
from os import environ

load_dotenv()

api_key=environ.get('GROQ_API_KEY')
llm=ChatGroq(model='llama-3.1-70b-versatile',api_key=api_key,temperature=0)

tool=APIRouter(prefix='/tool',tags=['Tool'])

@tool.get('/all')
def get_tools(current_user:dict=Depends(get_current_user)):
    if current_user is None:
        return {
            'status':'error',
            'message':'You need to be authenticated to access this route.'
        },status.HTTP_401_UNAUTHORIZED
    current_user=User(**current_user)
    with Session(engine) as session:
        tools=session.exec(select(Tool).where(Tool.user==current_user)).all()
        return {
            'status':'success',
            'tools':tools,
            'message':'tools fetched successfully.'
        },status.HTTP_200_OK

class ToolDefinition(BaseModel):
    tool_definition: str=Field(...,description="The definition of the tool.")

@tool.post('/add')
def add_tool(tool:ToolDefinition,current_user:dict=Depends(get_current_user)):
    if current_user is None:
        return {
            'status':'error',
            'message':'You need to be authenticated to access this route.'
        },status.HTTP_401_UNAUTHORIZED
    current_user=User(**current_user)
    tool_data=tool_to_ast(tool.tool_definition)
    if not tool_data.get('error'):
        tool_name=tool_data.get('tool_name')
        func_name=tool_data.get('func_name')
        description=tool_data.get('description')
        tool_definition=tool_data.get('tool')
        with Session(engine) as session:
            existing_tool = session.exec(select(Tool).where(Tool.user == current_user,Tool.name == tool_name)).first()
            if existing_tool:
                return {
                    'status':'error',
                    'message':'tool already exists.'
                },status.HTTP_400_BAD_REQUEST
            else:
                tool=Tool(**{
                    'name':tool_name,
                    'function_name':func_name,
                    'description':description
                })
                session.add(tool)
                session.commit()
                session.refresh(tool)
                save_tool_to_module('experimental.py',tool_definition)
                return {
                    'status':'success',
                    'tool':tool.model_dump(),
                    'message':'tool added successfully.'
                },status.HTTP_201_CREATED
    else:
        return {
            'status':'error',
            'message':tool_data.get('error')
        },status.HTTP_400_BAD_REQUEST

class Query(BaseModel):
    query: str=Field(...,description="The query to be searched.")

@tool.post('/generate')
def generate_tool(data:Query,current_user:dict=Depends(get_current_user)):
    if current_user is None:
        return {
            'status':'error',
            'message':'You need to be authenticated to access this route.'
        },status.HTTP_401_UNAUTHORIZED
    tool_response=generate(data.query,llm)
    tool_name=tool_response.get('name')
    func_name=tool_response.get('tool_name')
    tool_definition=tool_response.get('tool')
    return {
        'status':'success',
        'tool_name':tool_name,
        'func_name':func_name,
        'tool_definition':tool_definition
    },status.HTTP_200_OK

@tool.delete('/delete/{id}')
def delete_tool(id:str,current_user:dict=Depends(get_current_user)):
    if current_user is None:
        return {
            'status':'error',
            'message':'You need to be authenticated to access this route.'
        },status.HTTP_401_UNAUTHORIZED
    current_user=User(**current_user)
    with Session(engine) as session:
        existing_tool=session.exec(select(Tool).where(Tool.user==current_user,Tool.id==id)).first()
        if existing_tool:
            remove_tool_from_module('experimental.py',{
                'name':existing_tool.name,
                'tool_name':existing_tool.function_name
            })
            session.delete(existing_tool)
            session.commit()
            return {
                'status':'success',
                'message':'tool deleted successfully.'
            },status.HTTP_200_OK
        else:
            return {
                'status':'error',
                'message':'tool not found.'
            },status.HTTP_404_NOT_FOUND