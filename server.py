from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,Field
from src.inference.groq import ChatGroq
from src.agent.meta import MetaAgent
from dotenv import load_dotenv
from os import environ

load_dotenv()
api_key=environ.get('GROQ_API_KEY1')

app=FastAPI()
llm=ChatGroq(model='llama-3.1-70b-versatile',api_key=api_key,temperature=0)
agent=MetaAgent(llm=llm,verbose=True)

origins=[
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    query: str

@app.post("/query")
async def query(request: Query):
    query=request.query
    agent_response=agent.invoke(query)
    return {
        "query": agent_response
    }