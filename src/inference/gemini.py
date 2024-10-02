from requests import post,get,RequestException,HTTPError,ConnectionError
from tenacity import retry,stop_after_attempt,retry_if_exception_type
from src.message import AIMessage,BaseMessage,HumanMessage,ImageMessage
from src.inference import BaseInference
from requests import post,get
from json import loads
from io import BytesIO
import base64
import re

class ChatGemini(BaseInference):
    @retry(stop=stop_after_attempt(3),retry=retry_if_exception_type(RequestException))
    def invoke(self, messages: list[BaseMessage],json=False) -> AIMessage:
        headers=self.headers
        temperature=self.temperature
        url=self.base_url or f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        params={'key':self.api_key}
        contents=[]
        system_instruct=None
        for message in messages:
            if isinstance(message,HumanMessage):
                role='user'
            elif isinstance(message,AIMessage):
                role='model'
            else:
                role=''
                system_instruct={
                    'parts':{
                        'text': message.content
                    }
                }
            if role in ['user','model']:
                contents.append({
                    'role':role,
                    'parts':[{
                        'text':message.content
                    }]
                })
        payload={
            'contents': contents,
            'generationConfig':{
                'temperature': temperature,
                'responseMimeType':'application/json' if json else 'text/plain'
            }
        }
        if system_instruct:
            payload['system_instruction']=system_instruct
        try:
            response=post(url=url,headers=headers,json=payload,params=params)
            json_obj=response.json()
            # print(json_obj)
            if json_obj.get('error'):
                raise Exception(json_obj['error']['message'])
            if json:
                content=loads(json_obj['candidates'][0]['content']['parts'][0]['text'])
            else:
                content=json_obj['candidates'][0]['content']['parts'][0]['text']
            return AIMessage(content)
        except HTTPError as err:
            print(f'Error: {err.response.text}, Status Code: {err.response.status_code}')
        except ConnectionError as err:
            print(err)
        exit()
    
class Gemini(BaseInference):
    @retry(stop=stop_after_attempt(3),retry=retry_if_exception_type(RequestException))
    def invoke(self, query:str='',image_path:str='',json=False) -> AIMessage:
        headers=self.headers
        temperature=self.temperature
        url=self.base_url or f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        params={'key':self.api_key}
        payload={
            'contents':[{
                'parts':[{
                    'text':query
                }]
            }],
            'generationConfig':{
                'temperature': temperature,
                'responseMimeType':'application/json' if json else 'text/plain'
            }
        }
        if image_path:
            image_data={
                'inline_data':{
                    'mime_type':'image/jpeg',
                    'data': self.__image_to_base64(image_path)
                }
            }
            payload['contents'][0]['parts'].append(image_data)
        try:
            response=post(url,headers=headers,json=payload,params=params)
            json_obj=response.json()
            if json:
                content=loads(json_obj['candidates'][0]['content']['parts'][0]['text'])
            else:
                content=json_obj['candidates'][0]['content']['parts'][0]['text']
            return AIMessage(content)
        except HTTPError as err:
            print(f'Error: {err.response.text}, Status Code: {err.response.status_code}')
            exit()

    def __is_url(self,image_path:str)->bool:
        url_pattern = re.compile(r'^https?://')
        return url_pattern.match(image_path) is not None

    def __is_file_path(self,image_path:str)->bool:
        file_path_pattern = re.compile(r'^([./~]|([a-zA-Z]:)|\\|//)?\.?\/?[a-zA-Z0-9._-]+(\.[a-zA-Z0-9]+)?$')
        return file_path_pattern.match(image_path) is not None

    def __image_to_base64(self,image_source: str) -> str:
        if self.__is_url(image_source):
            response = get(image_source)
            bytes = BytesIO(response.content)
            image_bytes = bytes.read()
        elif self.__is_file_path(image_source):
            with open(image_source, 'rb') as image:
                image_bytes = image.read()
        else:
            raise ValueError("Invalid image source. Must be a URL or file path.")
        return base64.b64encode(image_bytes).decode('utf-8')
    
    @retry(stop=stop_after_attempt(3),retry=retry_if_exception_type(RequestException))
    def stream(self, query:str):
        headers=self.headers
        temperature=self.temperature
        url=self.base_url or f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
    
    def available_models(self):
        url='https://generativelanguage.googleapis.com/v1beta/models'
        headers=self.headers
        params={'key':self.api_key}
        try:
            response=get(url=url,headers=headers,params=params)
            response.raise_for_status()
            json_obj=response.json()
            models=json_obj['models']
        except HTTPError as err:
            print(f'Error: {err.response.text}, Status Code: {err.response.status_code}')
            exit()
        except ConnectionError as err:
            print(err)
            exit()
        return [model['displayName'] for model in models]