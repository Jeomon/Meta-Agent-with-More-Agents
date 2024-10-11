from src.tool import tool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
load_dotenv()

class Weather(BaseModel):
    location: str = Field(..., description='The location for which the weather information is to be retrieved.', example=['London'])

@tool('Weather Tool', args_schema=Weather)
def weather_tool(location: str):
    """
    Retrieves the current weather information for a specific location.
    """
    import requests
    import os
    import json
    api_key = os.environ.get('OPENWEATHERMAP_API_KEY')
    try:
        base_url = 'http://api.openweathermap.org/data/2.5/weather'
        params = {'q': location, 'appid': api_key, 'units': 'metric'}
        response = requests.get(base_url, params=params)
        weather_data = response.json()
        weather_info = f'Current weather in {location}: {weather_data['weather'][0]['description']}.\nTemperature: {weather_data['main']['temp']}°C.\nHumidity: {weather_data['main']['humidity']}%'
        return weather_info
    except Exception as err:
        return f'Error: {err}'

