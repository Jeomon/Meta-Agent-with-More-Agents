from src.tool import extract_tools_from_module,tool_to_ast,save_tool_to_module,remove_tool_from_module
from sqlmodel import SQLModel, Field, create_engine, Session,select
from fastapi import FastAPI,WebSocket,WebSocketDisconnect
from database import create_db_and_tables,engine
from fastapi.middleware.cors import CORSMiddleware
from models import Agent,Tool,Query,ToolDefinition
from contextlib import asynccontextmanager
from src.inference.groq import ChatGroq
from src.agent.meta import MetaAgent
from src.tool.generate import generate
from dotenv import load_dotenv
from experimental import *
from os import environ
import uvicorn
import ast

load_dotenv()
api_key=environ.get('GROQ_API_KEY1')

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app=FastAPI(lifespan=lifespan)
llm=ChatGroq(model='llama-3.1-70b-versatile',api_key=api_key,temperature=0)
agent=MetaAgent(agents=[],llm=llm,verbose=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.websocket("/ws")
async def socket(websocket:WebSocket):
    await websocket.accept()
    while True:
        try:
            data=await websocket.receive_text()
            chunks=agent.stream(data)
            for chunk in chunks:
                await websocket.send_json(chunk)
                print(chunk)
        except WebSocketDisconnect:
            break

@app.get('/agent/all')
def get_agents():
    with Session(engine) as session:
        agents=session.exec(select(Agent)).all()
        return {
            'status':'success',
            'agents':agents,
            'message':'agents fetched successfully.'
        }

@app.post('/agent/add')
def add_agent(agent:Agent):
    with Session(engine) as session:
        stmt=select(Agent).where(Agent.name.lower()==agent.name.lower())
        existing_agent=session.exec(stmt).first()
        if existing_agent:
            return {
                'status':'error',
                'message':'agent already exists.'
            }
        else:
            session.add(agent)
            session.commit()
            return {
                'status':'success',
                'message':'agent added successfully.'
            }

@app.get('/tool/all')
def get_tools():
    with Session(engine) as session:
        tools=session.exec(select(Tool)).all()
        return {
            'status':'success',
            'tools':tools,
            'message':'tools fetched successfully.'
        }

@app.post('/tool/add')
def add_tool(tool:ToolDefinition):
    tool_data=tool_to_ast(tool.tool_definition)
    if not tool_data.get('error'):
        tool_name=tool_data.get('tool_name')
        func_name=tool_data.get('func_name')
        description=tool_data.get('description')
        tool_definition=tool_data.get('tool')
        with Session(engine) as session:
            stmt=select(Tool).where(Tool.name==tool_name)
            existing_tool=session.exec(stmt).first()
            if existing_tool:
                return {
                    'status':'error',
                    'message':'tool already exists.'
                }
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
                }
    else:
        return {
            'status':'error',
            'message':tool_data.get('error')
        }
    
@app.post('/tool/generate')
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
@app.delete('/tool/delete/{id}')
def delete_tool(id:int):
    with Session(engine) as session:
        stmt=select(Tool).where(Tool.id==id)
        tool=session.exec(stmt).first()
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

if __name__=='__main__':
    uvicorn.run(app,host='0.0.0.0',port=8000)