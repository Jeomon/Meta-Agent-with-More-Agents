from src.inference.groq import ChatGroq
from src.agent.meta import MetaAgent
from dotenv import load_dotenv
from os import environ

load_dotenv()
api_key=environ.get('GROQ_API_KEY1')

query=input('Enter the query: ')
llm=ChatGroq(model='llama-3.1-70b-versatile',api_key=api_key,temperature=0)
agent=MetaAgent(llm=llm,verbose=True)
chunks=agent.stream(query)
for chunk in chunks:
    meta=chunk.get('Meta')
    answer=chunk.get('Answer')
    if meta:
        print(meta.get('current_agent'))
    if answer:
        print(answer.get('output'))