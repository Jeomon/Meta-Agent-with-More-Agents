from src.tool import tool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import json
import os

class Weather(BaseModel):
    location:str=Field(...,description="The location to get the weather for.",example=['London'])

@tool("Weather Tool",args_schema=Weather)
def weather_tool(location:str):
    '''
    Gets the current weather data for the given location using OpenWeatherMap API and returns the formatted results.
    '''
    import os
    import requests
    import json
    from pydantic import BaseModel
    from typing import Optional

    api_key=os.environ.get('OPENWEATHERMAP_API_KEY')
    try:
        response=requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric')
        data=response.json()
        if data['cod']!='404':
            main=data['main']
            weather=data['weather']
            weather_data={
                'location':location,
                'temperature':main['temp'],
                'humidity':main['humidity'],
                'weather_description':weather[0]['description'],
                'weather_icon':weather[0]['icon']
            }
            return json.dumps(weather_data,indent=4)
        else:
            return f'Error: Location not found. Please try again with a different location.'
    except Exception as err:
        return f'Error: {err}'

