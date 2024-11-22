from fastapi import APIRouter
from pydantic import BaseModel,Field
from api.models import Message,Conversation
from api.init_database import engine
from sqlmodel import Session
from datetime import datetime
from uuid import uuid4


message=APIRouter(prefix='/message')

class MessageData(BaseModel):
    role:str=Field(...,description='role of the message')
    content:str=Field(...,description='content of the message')
    conversation_id:str=Field(...,description='the conversation to which the message belongs')

@message.post('/')
def add_message(data:MessageData):
    with Session(engine) as session:
        id=str(uuid4())
        existing_conversation=session.get(Conversation,data.conversation_id)
        if existing_conversation:
            parameters={
                'id':id,
                'role':data.role,
                'content':data.content,
                'conversation':existing_conversation
            }
            message = Message(**parameters)
            session.add(message)
            session.commit()
            session.refresh(message)
            return {
                'status':'success',
                'current_message':message.model_dump(),
                'message':f'Message {id} added successfully to the current conversation.'
            }
        else:
            return {
                'status':'error',
                'message':'Conversation not found.'
            }