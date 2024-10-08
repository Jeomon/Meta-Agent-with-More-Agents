from src.tool import tool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
load_dotenv()

class WeatherAPI(BaseModel):
    location:str=Field(...,description="The location to fetch the weather data for.",example=['London'])

@tool("Weather API Tool",args_schema=WeatherAPI)
def weather_api_tool(location:str):
    '''
    Fetches the current weather data for a given location using the OpenWeatherMap API and returns the formatted results.
    '''
    import os
    import requests
    import json
    from pydantic import BaseModel

    api_key=os.environ.get('OPENWEATHERMAP_API_KEY')
    try:
        base_url=f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'
        response=requests.get(base_url)
        response.raise_for_status()
        data=response.json()
        weather_data={
            'location':location,
            'temperature':data['main']['temp'],
            'humidity':data['main']['humidity'],
            'conditions':data['weather'][0]['description']
        }
        return json.dumps(weather_data,indent=4)
    except requests.exceptions.HTTPError as errh:
        return f'HTTP Error: {errh}'
    except requests.exceptions.ConnectionError as errc:
        return f'Error Connecting: {errc}'
    except requests.exceptions.Timeout as errt:
        return f'Timeout Error: {errt}'
    except requests.exceptions.RequestException as err:
        return f'Something went wrong: {err}'

