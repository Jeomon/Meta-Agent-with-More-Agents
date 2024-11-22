from fastapi import APIRouter
from pydantic import BaseModel,Field
from sqlmodel import Session,select
from api.init_database import engine
from api.models import Conversation
from uuid import uuid4

conversation=APIRouter(prefix='/conversation')

@conversation.get('/')
def get_conversations():
     with Session(engine) as session:
        conversations = session.exec(select(Conversation)).all()
        return {
            'status':'success',
            'conversations':conversations,
            'message':'Conversations fetched successfully.'
        }
     
@conversation.get('/{id}')
def get_conversation(id:str):
    with Session(engine) as session:
        existing_conversation=session.get(Conversation,id)
        if existing_conversation:
            return {
                'status': 'success',
                'conversation': {
                    'id':id,
                    'title':existing_conversation.title,
                    'messages':[message.model_dump() for message in existing_conversation.messages],
                },
                'message': f'Messages of the conversation {id} fetched successfully.'
            }
        else:
            return {
                'status': 'error',
                'message': 'Conversation not found.'
            }

class ConversationData(BaseModel):
    title: str=Field(...,description='Title of the conversation')

@conversation.post('/')
def add_conversation(data:ConversationData):
    with Session(engine) as session:
        id=str(uuid4())
        conversation = Conversation(id=id,title=data.title,messages=[])
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
    return {
        'status':'success',
        'conversation':conversation.model_dump(),
        'message':'Conversation created successfully.'
    }

@conversation.patch('/{id}')
def edit_converation(id:str,data:ConversationData):
    with Session(engine) as session:
        existing_conversation=session.get(Conversation,id)
        if existing_conversation:
            existing_conversation.title=data.title
            session.commit()
            session.refresh(existing_conversation)
            return {
                'status':'success',
                'conversation':existing_conversation.model_dump(),
                'message':'Conversation edited successfully.'
            }


@conversation.delete('/{id}')
def delete_conversation(id:str):
    with Session(engine) as session:
        existing_conversation=session.get(Conversation,id)
        if existing_conversation:
            session.delete(existing_conversation)
            session.commit()
            return {
                'status': 'success',
                'message': f'Conversation {id} deleted successfully.'
            }
        else:
            return {
                'status':'error',
                'message':'Conversation not found.'
            }