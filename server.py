from fastapi import FastAPI,WebSocket,WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from api.conversation import conversation
from src.inference.groq import ChatGroq
from api.integration import integration
from src.agent.meta import MetaAgent
from api.init_database import engine
from sqlmodel import Session,select
from api.models import Agent,Tool
from api.message import message
from dotenv import load_dotenv
from sqlmodel import SQLModel
from api.agent import agent
from api.user import user
from experimental import *
from api.tool import tool
from os import environ
import uvicorn

load_dotenv()
api_key=environ.get('GROQ_API_KEY')

@asynccontextmanager
async def lifespan(_):
    SQLModel.metadata.create_all(engine)
    yield

app=FastAPI(lifespan=lifespan)
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
        agents=session.exec(select(Agent)).all()
        tools=session.exec(select(Tool)).all()
    agents=[agent.model_dump() for agent in agents]
    for agent in agents:
        agent['tools']=[eval(tool.function_name) for tool_name in agent['tools'].split(',') for tool in tools if tool.name==tool_name]
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