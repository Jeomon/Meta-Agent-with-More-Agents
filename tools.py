from src.tool import tool
from pydantic import BaseModel,Field
from random import randint
from os.path import join
from subprocess import run
from duckduckgo_search import DDGS
import requests

class Terminal(BaseModel):
    cmd:str=Field(...,description="The command to be executed.")

@tool('Terminal Tool',Terminal)
def terminal_tool(cmd):
    '''This Tool is used to execute shell commands only.'''
    process=run(cmd,text=True,shell=True,capture_output=True)
    if process.returncode!=0:
        return process.stderr.strip()
    else:
        return process.stdout.strip()

class Weather(BaseModel):
    location:str=Field(...,description="The location for the weather.")

@tool('Weather Tool',Weather)
def weather_tool(location):
    '''This Tool is used to give weather for a location.'''
    return f"{location} is at {randint(20,40)} deg celsius"

class Random(BaseModel):
    pass

@tool('Random Number Tool',Random)
def random_gen_tool():
    '''This Tool is used to generate random numbers only.'''
    return f"Random Number: {randint(0,100)}"

class Save(BaseModel):
    file_path:str=Field(...,description='file path of the file without filename.')
    filename:str=Field(...,description='filename of the file.')
    content:str=Field(...,description='the content that wanted to be saved.')

@tool("Save Tool",args_schema=Save)
def save_tool(file_path,filename,content)->str:
    '''
    This tool is used to save the contents to a file.
    The content parameter takes only multiline text.
    '''
    with open(join(file_path,filename),'w') as f:
        f.write(f'''{content}''')
    return f"Saved {filename} in {file_path} successfully."

class Search(BaseModel):
    query:str=Field(...,description="The query to be searched.")

@tool("Search Tool",args_schema=Search)
def search_tool(query:str):
    '''
    Searches for articles related to the given query using DDGS (DuckDuckGo Search) and returns the formatted results.
    '''
    ddgs=DDGS()
    results=ddgs.text(query,max_results=5)
    return '\n'.join([f"Title: {result['title']}\nContent: {result['body']}\nSource: {result['href']}" for result in results])
    #information=[] 
    # for result in results:
    #     url=result['href']
    #     response=requests.get(f'https://r.jina.ai/{url}')
    #     information.append(response.text)
    # return '\n'.join(information)

class News(BaseModel):
    company_name:str=Field(...,description="The name of the company to fetch news updates for.",example=['NVIDIA'])
    num_articles:int=Field(...,description="The number of news articles to be returned.",example=[5])

@tool("News Tool",args_schema=News)
def news_tool(company_name:str,num_articles:int)->str:
    '''
    Fetches news updates for the given company and returns the formatted results.
    '''
    import requests
    import json
    import os
    api_key=os.environ.get('NEWS_API_KEY')
    try:
        url=f'https://newsapi.org/v2/everything?q={company_name}&apiKey={api_key}&pageSize={num_articles}'
        response=requests.get(url)
        data=response.json()
        articles=data['articles']
        formatted_results=''
        for article in articles:
            formatted_results+=f"{article['title']}\n{article['description']}\n\n"
        return formatted_results
    except Exception as err:
        return f"Error: {err}"