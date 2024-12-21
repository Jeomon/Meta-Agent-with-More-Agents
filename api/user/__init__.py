from fastapi import APIRouter,status,Body,Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session,select
from api.init_database import engine
from api.models import User
from pydantic import BaseModel,Field
from passlib.context import CryptContext
from jwt import decode,encode
from typing import Annotated
from uuid import UUID
import os

user=APIRouter(prefix='/api/user',tags=['User'])
password_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='api/user/signin')
secret_key=os.getenv('SECRET_KEY')

class TokenData(BaseModel):
    access_token:str
    token_type:str

class UserData(BaseModel):
    username:str=Field(...,description='Username of the user')
    password:str=Field(...,description='Password of the user')

def authenticate_user(username:str,password:str):
    with Session(engine) as session:
        user=session.exec(select(User).where(User.email==username)).first()
        if not user:
            return None
        if not password_context.verify(password,user.password):
            return None
        return user

def get_current_user(token:Annotated[str,Depends(oauth2_scheme)])->dict|None:
    payload=decode(token,key=secret_key,algorithms=['HS256'])
    user_id=payload.get('id')
    if user_id is None:
        return None
    with Session(engine) as session:
        user=session.get(User,UUID(user_id))
        if not user:
            return None
        return user.model_dump()


@user.post('/signin')
def user_signin(credentials:Annotated[UserData,Body()]):
    user=authenticate_user(credentials.username,credentials.password)
    if not user:
        return {
            'status':'error',
            'message':'The username or password is incorrect.'
        },status.HTTP_401_UNAUTHORIZED
    else:
        access_token=encode({"id":str(user.id)},secret_key,algorithm='HS256')
        token_data=TokenData(access_token=access_token,token_type='Bearer')
        return {
            'status':'success',
            'token':token_data.model_dump(),
            'message':'The user has been logged in successfully.'
        },status.HTTP_200_OK

@user.post('/signup')
def user_signup(user:User):
    with Session(engine) as session:
        exising_user=session.exec(select(User).where(User.email==user.email)).first()
        if exising_user:
            return {
                'status':'error',
                'message':'The user already exists.'
            },status.HTTP_400_BAD_REQUEST
        else:
            user.password=password_context.hash(user.password)
            session.add(user)
            session.commit()
            session.refresh(user)
            return {
                'status':'success',
                'user':user,
                'message':'The user has been added successfully.'
            },status.HTTP_201_CREATED

@user.get('/signout')
def user_signout(current_user:dict=Depends(get_current_user)):
    if current_user is None:
        return {
            'status':'error',
            'message':'You need to be authenticated to access this route.'
        },status.HTTP_401_UNAUTHORIZED
    return {
        'status':'success',
        'message':'The user has been logged out successfully.'
    },status.HTTP_200_OK

