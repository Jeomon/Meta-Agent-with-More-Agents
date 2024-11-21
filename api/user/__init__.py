from fastapi import APIRouter
from sqlmodel import Session,select
from api.init_database import engine
from api.models import User

user=APIRouter(prefix='/user')

