from src.message import AIMessage,BaseMessage,SystemMessage,ImageMessage,HumanMessage,ToolMessage
from tenacity import retry,stop_after_attempt,retry_if_exception_type
from requests import RequestException,HTTPError,ConnectionError
from src.inference import BaseInference
from httpx import Client,AsyncClient
from typing import Generator
from typing import Literal
from json import loads
import requests
import base64
from uuid import uuid4

class ChatGroq(BaseInference):
    @retry(stop=stop_after_attempt(3),retry=retry_if_exception_type(RequestException))
    def invoke(self, messages: list[BaseMessage],json:bool=False)->AIMessage:
        self.headers.update({'Authorization': f'Bearer {self.api_key}'})
        headers=self.headers
        temperature=self.temperature
        url=self.base_url or "https://api.groq.com/openai/v1/chat/completions"
        contents=[]
        for message in messages:
            if isinstance(message,(SystemMessage,HumanMessage,AIMessage)):
                contents.append(message.to_dict())
            if isinstance(message,ImageMessage):
                text,image=message.content
                contents.append([
                    {
                        'role':'user',
                        'content':[
                            {
                                'type':'text',
                                'text':text
                            },
                            {
                                'type':'image_url',
                                'image_url':{
                                    'url':image
                                }
                            }
                        ]
                    }
                ])

        payload={
            "model": self.model,
            "messages": contents,
            "temperature": temperature,
            "stream":False,
        }
        if json:
            payload["response_format"]={
                "type": "json_object"
            }
        if self.tools:
            payload["tools"]=[{
                'type':'function',
                'function':{
                    'name':tool.name,
                    'description':tool.description,
                    'parameters':tool.schema
                }
            } for tool in self.tools]
        try:
            with Client() as client:
                response=client.post(url=url,json=payload,headers=headers)
            json_object=response.json()
            # print(json_object)
            if json_object.get('error'):
                raise HTTPError(json_object['error']['message'])
            else:
                message=json_object['choices'][0]['message']
                if json:
                    return AIMessage(loads(message.get('content')))
                if message.get('content'):
                    return AIMessage(message.get('content'))
                else:
                    tool_call=message.get('tool_calls')[0]['function']
                    return ToolMessage(id=str(uuid4()),name=tool_call['name'],args=tool_call['arguments']) 
        except HTTPError as err:
            err_object=loads(err.response.text)
            print(f'\nError: {err_object["error"]["message"]}\nStatus Code: {err.response.status_code}')
        except ConnectionError as err:
            print(err)
        exit()
    
    @retry(stop=stop_after_attempt(3),retry=retry_if_exception_type(RequestException))
    def stream(self, messages: list[BaseMessage],json=False)->Generator[str,None,None]:
        self.headers.update({'Authorization': f'Bearer {self.api_key}'})
        headers=self.headers
        temperature=self.temperature
        url=self.base_url or "https://api.groq.com/openai/v1/chat/completions"
        messages=[message.to_dict() for message in messages]
        payload={
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "response_format": {
                "type": "json_object" if json else "text"
            },
            "stream":True,
        }
        try:
            response=requests.post(url=url,json=payload,headers=headers)
            response.raise_for_status()
            chunks=response.iter_lines(decode_unicode=True)
            for chunk in chunks:
                chunk=chunk.replace('data: ','')
                if chunk and chunk!='[DONE]':
                    delta=loads(chunk)['choices'][0]['delta']
                    yield delta.get('content','')
        except HTTPError as err:
            err_object=loads(err.response.text)
            print(f'\nError: {err_object["error"]["message"]}\nStatus Code: {err.response.status_code}')
        except ConnectionError as err:
            print(err)
        exit()
    
    def available_models(self):
        url='https://api.groq.com/openai/v1/models'
        self.headers.update({'Authorization': f'Bearer {self.api_key}'})
        headers=self.headers
        response=requests.get(url=url,headers=headers)
        response.raise_for_status()
        models=response.json()
        return [model['id'] for model in models['data'] if model['active']]

class AudioGroq(BaseInference):
    def __init__(self,mode:Literal['transcriptions','translations']='transcriptions', model: str = '', api_key: str = '', base_url: str = '', temperature: float = 0.5):
        self.mode=mode
        super().__init__(model, api_key, base_url, temperature)
    def invoke(self,file:str='', language:str='en', json:bool=False)->AIMessage:
        headers={'Authorization': f'Bearer {self.api_key}'}
        temperature=self.temperature
        url=self.base_url or f"https://api.groq.com/openai/v1/audio/{self.mode}"
        payload={
            "model": self.model,
            "temperature": temperature,
            "response_format": {
                "type": "json_object" if json else "text"
            },
            "language": language
        }
        files={
            'file': self.__read_audio(file)
        }
        try:
            with Client() as client:
                response=client.post(url=url,json=payload,files=files,headers=headers)
            response.raise_for_status()
            if json:
                content=loads(response.text)['text']
            else:
                content=response.text
            return AIMessage(content)
        except HTTPError as err:
            err_object=loads(err.response.text)
            print(f'\nError: {err_object["error"]["message"]}\nStatus Code: {err.response.status_code}')
        except ConnectionError as err:
            print(err)
        exit()
    
    def __read_audio(file_name:str):
        with open(file_name,'rb') as f:
            audio_data=f.read()
        return base64.b64encode(audio_data).decode('utf-8')
    
    def available_models(self):
        url='https://api.groq.com/openai/v1/models'
        self.headers.update({'Authorization': f'Bearer {self.api_key}'})
        headers=self.headers
        response=requests.get(url=url,headers=headers)
        response.raise_for_status()
        models=response.json()
        return [model['id'] for model in models['data'] if model['active']]
