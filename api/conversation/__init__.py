from api.models import Conversation,Message,User
from fastapi import APIRouter,status,Depends
from pydantic import BaseModel,Field
from sqlmodel import Session,select
from api.init_database import engine
from api.user import get_current_user

conversation=APIRouter(prefix='/api/conversation',tags=['Conversation'])

@conversation.get('/')
def get_conversations(current_user:dict=Depends(get_current_user)):
     if current_user is None:
        return {
            'status':'error',
            'message':'You need to be authenticated to access this route.'
        },status.HTTP_401_UNAUTHORIZED
     with Session(engine) as session:
        current_user=User(**current_user)
        conversations=session.exec(select(Conversation).where(Conversation.user==current_user)).all()
        return {
            'status':'success',
            'conversations':conversations,
            'message':'Conversations fetched successfully.'
        },status.HTTP_200_OK
     
@conversation.get('/{id}')
def get_conversation(id:str,current_user:dict=Depends(get_current_user)):
    if current_user is None:
        return {
            'status':'error',
            'message':'You need to be authenticated to access this route.'
        },status.HTTP_401_UNAUTHORIZED
    current_user=User(**current_user)
    with Session(engine) as session:
        existing_conversation=session.exec(select(Conversation).where(Conversation.user==current_user).where(Conversation.id==id)).first()
        if existing_conversation:
            return {
                'status': 'success',
                'conversation': existing_conversation.model_dump(include={'messages':{'model':Message}}),
                'message': f'Messages of the conversation {id} fetched successfully.'
            },status.HTTP_200_OK
        else:
            return {
                'status': 'error',
                'message': 'Conversation not found.'
            },status.HTTP_404_NOT_FOUND

class ConversationData(BaseModel):
    title: str=Field(...,description='Title of the conversation')

@conversation.post('/')
def add_conversation(data:ConversationData,current_user:dict=Depends(get_current_user)):
    if current_user is None:
        return {
            'status':'error',
            'message':'You need to be authenticated to access this route.'
        },status.HTTP_401_UNAUTHORIZED
    current_user=User(**current_user)
    with Session(engine) as session:
        conversation = Conversation(title=data.title,messages=[],user=current_user)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
    return {
        'status':'success',
        'conversation':conversation.model_dump(),
        'message':'Conversation created successfully.'
    },status.HTTP_201_CREATED

@conversation.patch('/{id}')
def edit_converation(id:str,data:ConversationData,current_user:dict=Depends(get_current_user)):
    if current_user is None:
        return {
            'status':'error',
            'message':'You need to be authenticated to access this route.'
        },status.HTTP_401_UNAUTHORIZED
    current_user=User(**current_user)
    with Session(engine) as session:
        existing_conversation=session.exec(select(Conversation).where(Conversation.user==current_user,Conversation.id==id)).first()
        if existing_conversation:
            existing_conversation.title=data.title
            session.commit()
            session.refresh(existing_conversation)
            return {
                'status':'success',
                'conversation':existing_conversation.model_dump(),
                'message':'Conversation edited successfully.'
            },status.HTTP_200_OK
        else:
            return {
                'status':'error',
                'message':'Conversation not found.'
            },status.HTTP_404_NOT_FOUND


@conversation.delete('/{id}')
def delete_conversation(id:str,current_user:dict=Depends(get_current_user)):
    if current_user is None:
        return {
            'status':'error',
            'message':'You need to be authenticated to access this route.'
        },status.HTTP_401_UNAUTHORIZED
    current_user=User(**current_user)
    with Session(engine) as session:
        existing_conversation=session.exec(select(Conversation).where(Conversation.user==current_user,Conversation.id==id)).first()
        if existing_conversation:
            session.delete(existing_conversation)
            session.commit()
            return {
                'status': 'success',
                'message': f'Conversation {id} deleted successfully.'
            },status.HTTP_200_OK
        else:
            return {
                'status':'error',
                'message':'Conversation not found.'
            },status.HTTP_404_NOT_FOUND