from fastapi import APIRouter
from sqlmodel import Session,select
from api.init_database import engine
from api.models import Agent

agent=APIRouter(prefix='/agent')

@agent.get('/all')
def get_agents():
    with Session(engine) as session:
        agents=session.exec(select(Agent)).all()
        return {
            'status':'success',
            'agents':agents,
            'message':'agents fetched successfully.'
        }

@agent.post('/add')
def add_agent(agent:Agent):
    with Session(engine) as session:
        existing_agent=session.get(Agent,{'name':agent.name})
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

@agent.delete('/delete/{id}')
def delete_agent(id:int):
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