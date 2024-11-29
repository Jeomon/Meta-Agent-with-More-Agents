from fastapi import APIRouter
from sqlmodel import Session,select
from api.init_database import engine
from api.models import User
from pydantic import BaseModel,Field

user=APIRouter(prefix='/user')

user.get('/{id}')
def get_user(id:str):
    pass

class UserData(BaseModel):
    username:str=Field(...,description='Username of the user')
    password:str=Field(...,description='Password of the user')

user.post('/signin')
def user_signin(data:UserData):
    with Session(engine) as session:
        print(data)
        existing_user=session.exec(select(User).where(User.name==data.username).where(User.password==data.password)).first()
    if existing_user:
        return {
            'status':'success',
            'current_user':existing_user.model_dump(),
            'message':'The user has logged in successfully'
        }
    else:
        return {
            'status':'error',
            'message':'The user is not found'
        }

user.post('/signup')
def user_signup(user:User):
    pass

user.get('/signout')
def user_signout():
    pass