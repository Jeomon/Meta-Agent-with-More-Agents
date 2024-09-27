from src.agent.meta import MetaAgent
from src.inference.groq import ChatGroq
from os import environ
from dotenv import load_dotenv
from experimental import *

load_dotenv()

api_key=environ.get('GROQ_API_KEY')
llm=ChatGroq('llama-3.1-70b-versatile',api_key,temperature=0)
agent=MetaAgent(llm=llm,tools=[web_search_tool,file_writer_tool],verbose=True)
input=input("Enter a query: ")
agent_response=agent.invoke(input)
print(agent_response)