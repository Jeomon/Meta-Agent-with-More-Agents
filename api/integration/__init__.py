from fastapi import APIRouter
from sqlmodel import Session,select
from api.init_database import engine
from api.models import Integration

integration=APIRouter(prefix='/integration')

@integration.get('/')
def get_integrations():
    with Session(engine) as session:
        integrations=session.exec(select(Integration)).all()
        return {
            'status':'success',
            'integrations':integrations,
            'message':'integrations fetched successfully.'
        }

@integration.post('/')
def add_integration(integration:Integration):
    with Session(engine) as session:
        existing_integration=session.get(Integration,{'name':integration.name})
        if existing_integration:
            return {
                'status':'error',
                'message':'Integration already exists.'
            }
        else:
            session.add(integration)
            session.commit()
            session.refresh(integration)
            return {
                'status':'success',
                'integration':integration.model_dump(),
                'message':'Integration added successfully.'
            }

@integration.put('/')
def edit_integration(integration:Integration):
    with Session(engine) as session:
        existing_integration = session.exec(select(Integration).where(
            Integration.id == integration.id,
            Integration.name == integration.name
        )).first()
        if existing_integration:
            existing_integration.key=integration.key
            session.commit()
            session.refresh(existing_integration)
            return {
                'status':'success',
                'integration':existing_integration.model_dump(),
                'message':'Integration updated successfully.'
            }
        else:
            return {
                'status':'error',
                'message':'Integration not found.'
            }

@integration.delete('/{id}')
def delete_integration(id:int):
    with Session(engine) as session:
        existing_integration=session.get(Integration,id)
        if not existing_integration:
            return {
                'status':'error',
                'message':'Integration not found.'
            }
        else:
            session.delete(existing_integration)
            session.commit()
            return {
                'status':'success',
                'message':'Integration deleted successfully.'
            }
