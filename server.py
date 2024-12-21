from fastapi import FastAPI,WebSocket,WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from api.conversation import conversation
from src.inference.groq import ChatGroq
from api.integration import integration
from src.agent.meta import MetaAgent
from api.init_database import engine
from sqlmodel import Session,select
from api.message import message
from dotenv import load_dotenv
from sqlmodel import SQLModel
from api.models import Agent
from api.agent import agent
from api.user import user
from experimental import *
from api.tool import tool
from os import environ
import uvicorn

load_dotenv()
api_key=environ.get('GROQ_API_KEY')

@asynccontextmanager
async def lifespan(app:FastAPI):
    print('Server starting...')
    SQLModel.metadata.create_all(engine)
    yield
    print('Server stopping...')

app=FastAPI(title='Meta Agent with More Agents',version=1.0,
description="The Meta Agent coordinates the process, leveraging a ReAct Agent for tool-based tasks and a Chain of Thought Agent for reasoning-based tasks. The system's flexibility.",
lifespan=lifespan)

llm=ChatGroq(model='llama-3.1-70b-versatile',api_key=api_key,temperature=0)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.websocket("/ws")
async def socket(websocket:WebSocket):
    with Session(engine) as session:
        agents=[{
            'name':agent.name,
            'description':agent.description,
            'tools':[eval(tool.function_name)
                for tool in agent.tools]}
                for agent in session.exec(select(Agent)).all()]
    agent=MetaAgent(agents=agents,llm=llm,verbose=True)
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

app.include_router(user)
app.include_router(conversation)
app.include_router(integration)
app.include_router(message)
app.include_router(agent)
app.include_router(tool)

if __name__=='__main__':
    uvicorn.run(app,host='0.0.0.0',port=8000)