from src.tool import tool_to_ast,save_tool_to_module,remove_tool_from_module
from src.inference.groq import ChatGroq
from src.tool.generate import generate
from fastapi import APIRouter
from pydantic import BaseModel,Field
from sqlmodel import Session,select
from api.init_database import engine
from api.models import Tool
from dotenv import load_dotenv
from os import environ
from uuid import uuid4

load_dotenv()

api_key=environ.get('GROQ_API_KEY')
llm=ChatGroq(model='llama-3.1-70b-versatile',api_key=api_key,temperature=0)

tool=APIRouter(prefix='/tool')

@tool.get('/all')
def get_tools():
    with Session(engine) as session:
        tools=session.exec(select(Tool)).all()
        return {
            'status':'success',
            'tools':tools,
            'message':'tools fetched successfully.'
        }

class ToolDefinition(BaseModel):
    tool_definition: str=Field(...,description="The definition of the tool.")

@tool.post('/add')
def add_tool(tool:ToolDefinition):
    tool_data=tool_to_ast(tool.tool_definition)
    if not tool_data.get('error'):
        tool_name=tool_data.get('tool_name')
        func_name=tool_data.get('func_name')
        description=tool_data.get('description')
        tool_definition=tool_data.get('tool')
        with Session(engine) as session:
            existing_tool = session.exec(select(Tool).where(Tool.name == tool_name)).first()
            if existing_tool:
                return {
                    'status':'error',
                    'message':'tool already exists.'
                }
            else:
                tool=Tool(**{
                    'id':str(uuid4()),
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
                }
    else:
        return {
            'status':'error',
            'message':tool_data.get('error')
        }

class Query(BaseModel):
    query: str=Field(...,description="The query to be searched.")

@tool.post('/generate')
def generate_tool(data:Query):
    tool_response=generate(data.query,llm)
    tool_name=tool_response.get('name')
    func_name=tool_response.get('tool_name')
    tool_definition=tool_response.get('tool')
    return {
        'status':'success',
        'tool_name':tool_name,
        'func_name':func_name,
        'tool_definition':tool_definition
    }
@tool.delete('/delete/{id}')
def delete_tool(id:str):
    with Session(engine) as session:
        tool=session.get(Tool,id)
        if tool:
            remove_tool_from_module('experimental.py',{
                'name':tool.name,
                'tool_name':tool.function_name
            })
            session.delete(tool)
            session.commit()
            return {
                'status':'success',
                'message':'tool deleted successfully.'
            }
        else:
            return {
                'status':'error',
                'message':'tool not found.'
            }