from fastapi import APIRouter,status,Depends
from sqlmodel import Session,select
from api.init_database import engine
from api.models import Agent,Tool,User
from pydantic import BaseModel,Field
from api.user import get_current_user

agent=APIRouter(prefix='/agent',tags=['Agent'])

@agent.get('/all')
def get_agents(current_user:dict=Depends(get_current_user)):
    with Session(engine) as session:
        if current_user is None:
            return {
                'status':'error',
                'message':'You need to be authenticated to access this route.'
            },status.HTTP_401_UNAUTHORIZED
        current_user=User(**current_user)
        agents=session.exec(select(Agent).where(Agent.user==current_user)).all()
        return {
            'status':'success',
            'agents':[agent.model_dump(include={'tools':{'model':Tool}}) for agent in agents],
            'message':'agents fetched successfully.'
        },status.HTTP_200_OK 

class AgentData(BaseModel):
    name:str=Field(...,description='Name of the agent')
    description:str=Field(...,description='Description about the agent')
    tool_ids:list[str]=Field(description='The tools the agent does have access too.')

@agent.post('/add')
def add_agent(data:AgentData,current_user:dict=Depends(get_current_user)):
    with Session(engine) as session:
        if current_user is None:
            return {
                'status':'error',
                'message':'You need to be authenticated to access this route.'
            },status.HTTP_401_UNAUTHORIZED
        current_user=User(**current_user)
        existing_agent = session.exec(select(Agent).where(Agent.user == current_user,Agent.name == data.name)).first()
        if existing_agent:
            return {
                'status':'error',
                'message':'agent already exists.'
            },status.HTTP_400_BAD_REQUEST
        else:
            tools=[session.get(Tool,id) for id in data.tool_ids if id is not None]
            agent=Agent(**{
                'name':data.name,
                'description':data.description,
                'tools':tools,
                'user':current_user
            })
            session.add(agent)
            session.commit()
            session.refresh(agent)
            return {
                'status':'success',
                'agent':agent.model_dump(include={'tools':{'model':Tool}}),
                'message':'agent added successfully.'
            },status.HTTP_201_CREATED

@agent.delete('/delete/{id}')
def delete_agent(id:str,current_user:dict=Depends(get_current_user)):
    with Session(engine) as session:
        if current_user is None:
            return {
                'status':'error',
                'message':'You need to be authenticated to access this route.'
            },status.HTTP_401_UNAUTHORIZED
        current_user=User(**current_user)
        existing_agent=session.exec(select(Agent).where(Agent.user==current_user,Agent.id==id)).first()
        if existing_agent:
            session.delete(existing_agent)
            session.commit()
            return {
                'status':'success',
                'message':'agent deleted successfully.'
            },status.HTTP_200_OK
        else:
            return {
                'status':'error',
                'message':'agent not found.'
            },status.HTTP_404_NOT_FOUND