from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,Field
from src.inference.groq import ChatGroq
from src.agent.meta import MetaAgent
from dotenv import load_dotenv
from fastapi import FastAPI,WebSocket
from os import environ
from uuid import uuid4

load_dotenv()
api_key=environ.get('GROQ_API_KEY1')

app=FastAPI()
llm=ChatGroq(model='llama-3.1-70b-versatile',api_key=api_key,temperature=0)
agent=MetaAgent(llm=llm,verbose=True)

origins=[
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket:WebSocket):
    await websocket.accept()
    try:
        while True:
            data=await websocket.receive_text()
            agent_response= agent.invoke(data)
            await websocket.send_text(agent_response)
    except Exception as e:
        print(e)
    finally:
        await websocket.close()

@app.post('/tool/create')
def tool_create():
    pass

@app.post('/tool/update')
def tool_update():
    pass

@app.post('/tool/delete')
def tool_delete():
    pass