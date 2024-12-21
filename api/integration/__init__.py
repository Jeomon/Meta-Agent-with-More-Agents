from fastapi import APIRouter,status,Depends
from sqlmodel import Session,select
from api.init_database import engine
from api.models import User,Integration
from api.user import get_current_user
from uuid import UUID

integration=APIRouter(prefix='/api/integration',tags=['Integration'])

@integration.get('/')
def get_integrations(current_user:dict=Depends(get_current_user)):
    if current_user is None:
        return {
            'status':'error',
            'message':'You need to be authenticated to access this route.'
        },status.HTTP_401_UNAUTHORIZED
    with Session(engine) as session:
        current_user=session.exec(select(User).where(User.id==current_user.get('id'))).first()
        integrations=session.exec(select(Integration).where(Integration.user==current_user)).all()
        return {
            'status':'success',
            'integrations':integrations,
            'message':'integrations fetched successfully.'
        },status.HTTP_200_OK

@integration.post('/')
def add_integration(integration:Integration,current_user:dict=Depends(get_current_user)):
    if current_user is None:
        return {
            'status':'error',
            'message':'You need to be authenticated to access this route.'
        },status.HTTP_401_UNAUTHORIZED
    with Session(engine) as session:
        current_user=session.exec(select(User).where(User.id==current_user.get('id'))).first()
        existing_integration=session.exec(select(Integration).where(Integration.user==current_user,Integration.name==integration.name)).first()
        if existing_integration:
            return {
                'status':'error',
                'message':'Integration already exists.'
            },status.HTTP_400_BAD_REQUEST
        else:
            session.add(integration)
            session.commit()
            session.refresh(integration)
            return {
                'status':'success',
                'integration':integration.model_dump(),
                'message':'Integration added successfully.'
            },status.HTTP_201_CREATED

@integration.put('/')
def edit_integration(integration:Integration,current_user:dict=Depends(get_current_user)):
    if current_user is None:
        return {
            'status':'error',
            'message':'You need to be authenticated to access this route.'
        },status.HTTP_401_UNAUTHORIZED
    with Session(engine) as session:
        current_user=session.exec(select(User).where(User.id==current_user.get('id'))).first()
        existing_integration = session.exec(select(Integration).where(
            Integration.user == current_user,
            Integration.id == integration.id,
        )).first()
        if existing_integration:
            existing_integration.key=integration.key
            session.commit()
            session.refresh(existing_integration)
            return {
                'status':'success',
                'integration':existing_integration.model_dump(),
                'message':'Integration updated successfully.'
            },status.HTTP_200_OK
        else:
            return {
                'status':'error',
                'message':'Integration not found.'
            },status.HTTP_404_NOT_FOUND

@integration.delete('/{id}')
def delete_integration(id:UUID,current_user:dict=Depends(get_current_user)):
    if current_user is None:
        return {
            'status':'error',
            'message':'You need to be authenticated to access this route.'
        },status.HTTP_401_UNAUTHORIZED
    with Session(engine) as session:
        current_user=session.exec(select(User).where(User.id==current_user.get('id'))).first()
        existing_integration=session.exec(select(Integration).where(Integration.user==current_user,Integration.id==id)).first()
        if not existing_integration:
            return {
                'status':'error',
                'message':'Integration not found.'
            },status.HTTP_404_NOT_FOUND
        else:
            session.delete(existing_integration)
            session.commit()
            return {
                'status':'success',
                'message':'Integration deleted successfully.'
            },status.HTTP_200_OK
