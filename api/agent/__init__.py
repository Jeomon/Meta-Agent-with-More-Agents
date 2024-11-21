from fastapi import APIRouter
from sqlmodel import Session,select
from api.init_database import engine
from api.models import Agent,Tool
from pydantic import BaseModel,Field
from uuid import uuid4

agent=APIRouter(prefix='/agent')

@agent.get('/all')
def get_agents():
    with Session(engine) as session:
        agents=session.exec(select(Agent)).all()
        return {
            'status':'success',
            'agents':[{
                'id':agent.id,
                'name':agent.name,
                'description':agent.description,
                'tools':[tool.name for tool in agent.tools]
            } for agent in agents],
            'message':'agents fetched successfully.'
        }

class AgentData(BaseModel):
    name:str=Field(...,description='Name of the agent')
    description:str=Field(...,description='Description about the agent')
    tool_ids:list[str]=Field(description='The tools the agent does have access too.')

@agent.post('/add')
def add_agent(data:AgentData):
    with Session(engine) as session:
        existing_agent = session.exec(select(Agent).where(Agent.name == data.name)).first()
        if existing_agent:
            return {
                'status':'error',
                'message':'agent already exists.'
            }
        else:
            tools=[session.get(Tool,id) for id in data.tool_ids if session.get(Tool,id) and (id is not None)]
            agent=Agent(**{
                'id':str(uuid4()),
                'name':data.name,
                'description':data.description,
                'tools':tools
            })
            session.add(agent)
            session.commit()
            session.refresh(agent)
            return {
                'status':'success',
                'agent':{
                    'id':agent.id,
                    'name':agent.name,
                    'description':agent.description,
                    'tools':[tool.name for tool in tools]
                },
                'message':'agent added successfully.'
            }

@agent.delete('/delete/{id}')
def delete_agent(id:str):
    with Session(engine) as session:
        agent=session.get(Agent,id)
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