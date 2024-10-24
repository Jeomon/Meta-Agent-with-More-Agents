from fastapi import FastAPI,WebSocket,WebSocketDisconnect
from experimental import *
from fastapi.middleware.cors import CORSMiddleware
from src.inference.groq import ChatGroq
from src.agent.meta import MetaAgent
from dotenv import load_dotenv
from os import environ
import uvicorn

load_dotenv()
api_key=environ.get('GROQ_API_KEY1')
app=FastAPI()
llm=ChatGroq(model='llama-3.1-70b-versatile',api_key=api_key,temperature=0)
agents=[
    {
        'name': 'Weather Agent',
        'description': 'This agent is responsible for providing information related to weather based on the given location.',
        'tools': [weather_tool]
    },
    {
        'name': 'Stock Agent',
        'description': 'This agent will provide current price of the given stock.',
        'tools': [stock_price_tool]
    }
]
agent=MetaAgent(agents=agents,llm=llm,verbose=True)

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

if __name__=='__main__':
    uvicorn.run(app,host='0.0.0.0',port=8000)