from fastapi import FastAPI,WebSocket,WebSocketDisconnect
from sqlmodel import SQLModel, Field, create_engine, Session,select
from database import create_db_and_tables,engine
from fastapi.middleware.cors import CORSMiddleware
from src.inference.groq import ChatGroq
from src.agent.meta import MetaAgent
from src.tool.generate import generate
from models import Agent,Tool,Query
from dotenv import load_dotenv
from experimental import *
from os import environ
import uvicorn

load_dotenv()
api_key=environ.get('GROQ_API_KEY1')

app=FastAPI(on_startup=[lambda:create_db_and_tables()])
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
        stmt=select(Agent).where(Agent.name==agent.name)
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
@app.get('/tool/add')
def add_tool(tool:Tool):
    with Session(engine) as session:
        stmt=select(Tool).where(Tool.name==tool.name)
        existing_tool=session.exec(stmt).first()
        if existing_tool:
            return {
                'status':'error',
                'message':'tool already exists.'
            }
        else:
            session.add(tool)
            session.commit()
            return {
                'status':'success',
                'message':'tool added successfully.'
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

if __name__=='__main__':
    uvicorn.run(app,host='0.0.0.0',port=8000)