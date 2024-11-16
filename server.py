from src.tool import tool_to_ast,save_tool_to_module,remove_tool_from_module
from fastapi import FastAPI,WebSocket,WebSocketDisconnect
from models import Agent,Tool,Integration,Conversation
from fastapi.middleware.cors import CORSMiddleware
from database import create_db_and_tables,engine
from contextlib import asynccontextmanager
from src.inference.groq import ChatGroq
from src.agent.meta import MetaAgent
from src.tool.generate import generate
from sqlmodel import Session,select
from dotenv import load_dotenv
from experimental import *
from os import environ
import uvicorn

load_dotenv()
api_key=environ.get('GROQ_API_KEY')

@asynccontextmanager
async def lifespan(_):
    create_db_and_tables()
    
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
        session.close()
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
                'agent':agent.model_dump(),
                'message':'agent added successfully.'
            }

@app.delete('/agent/delete/{id}')
def delete_agent(id:int):
    with Session(engine) as session:
        stmt=select(Agent).where(Agent.id==id)
        agent=session.exec(stmt).first()
        if agent:
            session.delete(agent)
            session.commit()
            return {
                'status':'success',
                'message':'agent deleted successfully.'
            }
        else:
            return {
                'status':'error',
                'message':'agent not found.'
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

class ToolDefinition(BaseModel):
    tool_definition: str=Field(...,description="The definition of the tool.")

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

class Query(BaseModel):
    query: str=Field(...,description="The query to be searched.")

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
        
@app.get('/integration')
def get_integrations():
    with Session(engine) as session:
        integrations=session.exec(select(Integration)).all()
        return {
            'status':'success',
            'integrations':integrations,
            'message':'integrations fetched successfully.'
        }

@app.post('/integration')
def add_integration(integration:Integration):
    with Session(engine) as session:
        stmt=select(Integration).where(Integration.name==integration.name)
        existing_integration=session.exec(stmt).first()
        if existing_integration:
            return {
                'status':'error',
                'message':'Integration already exists.'
            }
        else:
            session.add(integration)
            session.commit()
            session.refresh(integration)
            return {
                'status':'success',
                'integration':integration.model_dump(),
                'message':'Integration added successfully.'
            }

@app.put('/integration')
def edit_integration(integration:Integration):
    with Session(engine) as session:
        stmt=select(Integration).where((Integration.id==integration.id)&(Integration.name==integration.name))
        existing_integration=session.exec(stmt).first()
        if existing_integration:
            existing_integration.key=integration.key
            session.commit()
            session.refresh(existing_integration)
            return {
                'status':'success',
                'integration':existing_integration.model_dump(),
                'message':'Integration updated successfully.'
            }
        else:
            return {
                'status':'error',
                'message':'Integration not found.'
            }

@app.delete('/integration/{id}')
def delete_integration(id:int):
    with Session(engine) as session:
        existing_integration=session.exec(select(Integration).where(Integration.id==id)).first()
        if not existing_integration:
            return {
                'status':'error',
                'message':'Integration not found.'
            }
        else:
            session.delete(existing_integration)
            session.commit()
            return {
                'status':'success',
                'message':'Integration deleted successfully.'
            }

@app.get('/conversation/{session_id}')
def get_session(session_id:str):
     with Session(engine) as session:
        conversation = session.exec(select(Conversation).where(Conversation.id == session_id)).first()
        if conversation:
            messages = [
                {
                    "id": message.id,
                    "role": message.role,
                    "content": message.content,
                    "timestamp": message.timestamp
                }
                for message in conversation.messages
            ]

            return {
                "status": "success",
                "session_id": session_id,
                "title": conversation.title,
                "messages": messages,
                "message": "Conversation fetched successfully."
            }
        else:
            return {
                "status": "error",
                "message": "Conversation not found."
            }

@app.get('/conversation')
def get_conversation():
     with Session(engine) as session:
        conversation = session.exec(select(Conversation)).all()
        return {
            'status':'success',
            'conversation':conversation.model_dump(),
            'message':'Conversations fetched successfully.'
        }


if __name__=='__main__':
    uvicorn.run(app,host='0.0.0.0',port=8000)