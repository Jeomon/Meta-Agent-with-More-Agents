from src.tool import tool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import json
import os
load_dotenv()

class Weather(BaseModel):
    location:str=Field(...,description="The location to get the weather data for.",example=['London'])

@tool("Weather Tool",args_schema=Weather)
def weather_tool(location:str):
    '''
    Retrieves the current weather data for the given location using the OpenWeatherMap API and returns the formatted results.
    '''
    import os
    import requests
    import json
    from pydantic import BaseModel
    from typing import Optional

    api_key=os.environ.get('OPENWEATHERMAP_API_KEY')
    try:
        base_url="http://api.openweathermap.org/data/2.5/weather"
        params={
            'q':location,
            'appid':api_key,
            'units':'metric'
        }
        response=requests.get(base_url,params=params)
        weather_data=response.json()
        if weather_data['cod']!='404':
            main=weather_data['main']
            temperature=main['temp']
            humidity=main['humidity']
            pressure=main['pressure']
            weather_report="Weather in {}\nTemperature: {}°C\nHumidity: {}%\nPressure: {} hPa".format(location,temperature,humidity,pressure)
            return weather_report
        else:
            return 'City Not Found'
    except Exception as err:
        return f"Error: {err}"

