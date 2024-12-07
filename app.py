from src.inference.groq import ChatGroq
from src.inference.mistral import ChatMistral
from src.agent.meta import MetaAgent
from dotenv import load_dotenv
from os import environ
from experimental import weather_tool

load_dotenv()
api_key=environ.get('GROQ_API_KEY')

query=input('Enter the query: ')
llm=ChatGroq(model='llama-3.3-70b-versatile',api_key=api_key,temperature=0)
agents=[
    {
        'name': 'Weather Agent',
        'description': 'This agent is responsible for providing information related to weather based on the given location.',
        'tools': [weather_tool]
    },
]
agent=MetaAgent(agents=agents,llm=llm,verbose=True)
# agent_response=agent.invoke(query)
# print(agent_response)

for chunk in agent.stream(query):
    print(chunk)