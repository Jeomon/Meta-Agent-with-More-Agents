from src.tool import tool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
load_dotenv()

class NewsSearch(BaseModel):
    query:str=Field(...,description="The query to be searched.",example=['AI models'])

@tool("News Search Tool",args_schema=NewsSearch)
def news_search_tool(query:str):
    '''
    Searches for recent news articles and press releases about AI models and returns the formatted results.
    '''
    import requests
    import json
    from datetime import datetime

    api_key=os.environ.get('NEWS_API_KEY')
    url=f'https://newsapi.org/v2/everything?q={query}&apiKey={api_key}&language=en&sortBy=relevancy'
    try:
        response=requests.get(url)
        data=response.json()
        articles=data['articles']
        formatted_results=[]
        for article in articles:
            published_at=datetime.strptime(article['publishedAt'],'%Y-%m-%dT%H:%M:%SZ')
            formatted_results.append({
                'title':article['title'],
                'description':article['description'],
                'published_at':published_at.strftime('%Y-%m-%d %H:%M:%S'),
                'url':article['url'],
                'source':article['source']['name']
            })
        return json.dumps(formatted_results,indent=4)
    except Exception as err:
        return f"Error: {err}"

