from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from api.conversation import conversation
from src.inference.gemini import ChatGemini
from api.integration import integration
from src.agent.meta import MetaAgent
from api.init_database import engine
from sqlmodel import Session, select
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
import asyncio

load_dotenv()
api_key = environ.get('GOOGLE_API_KEY')

@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Server starting...')
    SQLModel.metadata.create_all(engine)
    yield
    print('Server stopping...')

app = FastAPI(title='Meta Agent with More Agents', version=1.0,
              description="The Meta Agent coordinates the process, leveraging a ReAct Agent for tool-based tasks and a Chain of Thought Agent for reasoning-based tasks. The system's flexibility.",
              lifespan=lifespan)

# Initialize the LLM model (ChatGemini)
llm = ChatGemini(model='gemini-2.0-flash-exp', api_key=api_key, temperature=0)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Asynchronous function to handle agent streaming
async def call_agent(websocket: WebSocket, query: str, agent: MetaAgent):
    try:
        chunks = agent.stream(query)  # Assuming stream yields chunks
        for chunk in chunks:
            await websocket.send_json(chunk)  # Send the chunk to WebSocket
            print(f"Sent chunk: {chunk}")
    except Exception as e:
        await websocket.send_json({"status": "error", "message": str(e)})

@app.websocket("/ws")
async def socket(websocket: WebSocket):
    # Load agents from the database
    with Session(engine) as session:
        agents = [{
            'name': agent.name,
            'description': agent.description,
            'tools': [eval(tool.function_name) for tool in agent.tools]
        } for agent in session.exec(select(Agent)).all()]
    agent = MetaAgent(agents=agents, llm=llm, verbose=True)
    # Accept the WebSocket connection
    await websocket.accept()
    while True:
        try:
            # Receive the query from the WebSocket
            query = await websocket.receive_text()
            # Start the agent processing in the background
            asyncio.create_task(call_agent(websocket, query, agent))

        except WebSocketDisconnect:
            print("WebSocket disconnected")
            break
        except Exception as e:
            print(f"Error during WebSocket communication: {e}")
            break

# Include routers
app.include_router(user)
app.include_router(conversation)
app.include_router(integration)
app.include_router(message)
app.include_router(agent)
app.include_router(tool)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
