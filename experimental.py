from src.tool import tool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
load_dotenv()

class WebSearch(BaseModel):
    query:str=Field(...,description="The topic to be searched.",example=['health is wealth'])

@tool("Web Search Tool",args_schema=WebSearch)
def web_search_tool(query:str):
    '''
    Searches for articles related to the given topic using DDGS (DuckDuckGo Search) and returns the formatted results.
    '''
    from duckduckgo_search import DDGS
    import os
    api_key=os.environ.get('DDGS_API_KEY')
    try:
        ddgs=DDGS()
        results=ddgs.text(query,max_results=5)
        return '\n'.join([f"{result['title']}\n{result['body']}" for result in results])
    except Exception as err:
        return f"Error: {err}"

class FileWriter(BaseModel):
    file_name:str=Field(...,description="The name of the file to be written.",example=['health.txt'])
    text:str=Field(...,description="The text to be written to the file.",example=['Hello, World!'])

@tool("File Writer Tool",args_schema=FileWriter)
def file_writer_tool(file_name:str,text:str)->str:
    """
    Writes the provided text to a file in the current working directory.
    """
    try:
        with open(file_name,"w") as file:
            file.write(text)
        return f"Text successfully written to {file_name}."
    except Exception as err:
        return f"Error: {err}"

class Weather(BaseModel):
    location:str=Field(...,description="The location to fetch the weather data for.",example=['London'])

@tool("Weather Tool",args_schema=Weather)
def weather_tool(location:str):
    """
    Fetches the current weather data for a given location using OpenWeatherMap API and returns the formatted results.
    """
    import os
    import requests
    import json
    from pydantic import BaseModel

    api_key=os.environ.get('OPENWEATHERMAP_API_KEY')
    try:
        base_url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'
        response = requests.get(base_url)
        weather_data = response.json()
        if weather_data['cod'] == '404':
            return f'Error: City {location} not found'
        elif weather_data['cod'] == '401':
            return f'Error: Invalid API key'
        else:
            main = weather_data['main']
            temperature = main['temp']
            humidity = main['humidity']
            pressure = main['pressure']
            weather_report = weather_data['weather']
            return f'City: {location}\nTemperature: {temperature}°C\nHumidity: {humidity}%\nPressure: {pressure} hPa\nWeather Report: {weather_report[0]["description"]}'
    except Exception as err:
        return f'Error: {err}'

