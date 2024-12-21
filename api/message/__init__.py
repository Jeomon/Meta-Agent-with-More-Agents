from fastapi import APIRouter,status,Depends
from pydantic import BaseModel,Field
from api.init_database import engine
from api.models import Conversation,User,Message
from api.user import get_current_user
from sqlmodel import Session,select


message=APIRouter(prefix='/api/message',tags=['Message'])

class MessageData(BaseModel):
    role:str=Field(...,description='role of the message')
    content:str=Field(...,description='content of the message')
    conversation_id:str=Field(...,description='the conversation to which the message belongs')

@message.post('/')
def add_message(data:MessageData,current_user:dict=Depends(get_current_user)):
    if current_user is None:
        return {
            'status':'error',
            'message':'You need to be authenticated to access this route.'
        },status.HTTP_401_UNAUTHORIZED
    with Session(engine) as session:
        current_user=session.exec(select(User).where(User.id==current_user.get('id'))).first()
        existing_conversation=session.exec(select(Conversation).where(Conversation.user==current_user,Conversation.id==data.conversation_id)).first()
        if existing_conversation:
            message = Message(**{
                'role':data.role,
                'content':data.content,
                'conversation':existing_conversation
            })
            session.add(message)
            session.commit()
            session.refresh(message)
            return {
                'status':'success',
                'current_message':message.model_dump(),
                'message':f'Message {message.id} added successfully to the current conversation.'
            },status.HTTP_201_CREATED
        else:
            return {
                'status':'error',
                'message':'Conversation not found.'
            },status.HTTP_404_NOT_FOUND