from src.inference.groq import ChatGroq
from src.inference.mistral import ChatMistral
from src.agent.meta import MetaAgent
from dotenv import load_dotenv
from os import environ
from experimental import weather_tool,stock_price_tool

load_dotenv()
# api_key=environ.get('GROQ_API_KEY1')
api_key=environ.get('MISTRAL_API_KEY')

query=input('Enter the query: ')
# llm=ChatGroq(model='llama-3.1-70b-versatile',api_key=api_key,temperature=0)
llm=ChatMistral(model='open-mistral-nemo',api_key=api_key,temperature=0)
agents=[
    {
        'name': 'Weather Agent',
        'description': 'This agent is responsible for providing information related to weather based on the given location.',
        'tools': [weather_tool]
    },
    {
        'name': 'Stock Agent',
        'description': 'This agent will provide current price of the given stock.',
        'tools': [stock_price_tool]
    }
]
agent=MetaAgent(agents=agents,llm=llm,verbose=True)
agent_response=agent.invoke(query)
print(agent_response)