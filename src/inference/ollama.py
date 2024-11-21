from tenacity import retry,stop_after_attempt,retry_if_exception_type
from requests import post,get,RequestException,HTTPError
from src.message import AIMessage,BaseMessage,ToolMessage
from src.inference import BaseInference
from typing import Generator
from json import loads
from uuid import uuid4

class ChatOllama(BaseInference):
    @retry(stop=stop_after_attempt(3),retry=retry_if_exception_type(RequestException))
    def invoke(self,messages: list[BaseMessage],json=False)->AIMessage:
        headers=self.headers
        temperature=self.temperature
        url=self.base_url or "http://localhost:11434/api/chat"
        payload={
            "model": self.model,
            "messages": [message.to_dict() for message in messages],
            "options":{
                "temperature": temperature,
            },
            "format":'json' if json else '',
            "stream":False
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
            response=post(url=url,json=payload,headers=headers)
            response.raise_for_status()
            json_object=response.json()
            message=json_object['choices'][0]['message']
            if json:
                return AIMessage(loads(message.get('content')))
            if message.get('content'):
                return AIMessage(message.get('content'))
            else:
                tool_call=message.get('tool_calls')[0]['function']
                return ToolMessage(id=str(uuid4()),name=tool_call['name'],args=tool_call['arguments']) 
        except HTTPError as err:
            print(f'Error: {err.response.text}, Status Code: {err.response.status_code}')
    
    def stream(self,messages: list[BaseMessage],json=False)->Generator[str,None,None]:
        headers=self.headers
        temperature=self.temperature
        url=self.base_url or "http://localhost:11434/api/chat"
        payload={
            "model": self.model,
            "messages": [message.to_dict() for message in messages],
            "options":{
                "temperature": temperature,
            },
            "format":'json' if json else '',
            "stream":True
        }
        try:
            response=post(url=url,json=payload,headers=headers,stream=True)
            response.raise_for_status()
            chunks=response.iter_lines(decode_unicode=True)
            return (loads(chunk)['message']['content'] for chunk in chunks)
        except HTTPError as err:
            print(f'Error: {err.response.text}, Status Code: {err.response.status_code}')
        except ConnectionError as err:
            print(err)
        exit()
    
    def available_models(self):
        url='http://localhost:11434/api/tags'
        headers=self.headers
        response=get(url=url,headers=headers)
        response.raise_for_status()
        models=response.json()
        return [model['name'] for model in models['models']]
        
class Ollama(BaseInference):
    def invoke(self, query:str,json=False)->AIMessage:
        headers=self.headers
        temperature=self.temperature
        url=self.base_url or "http://localhost:11434/api/generate"
        payload={
            "model": self.model,
            "prompt": query,
            "options":{
                "temperature": temperature,
            },
            "format":'json' if json else '',
            "stream":False
        }
        try:
            response=post(url=url,json=payload,headers=headers)
            response.raise_for_status()
            json_obj=response.json()
            return AIMessage(json_obj['response'])
        except HTTPError as err:
            print(f'Error: {err.response.text}, Status Code: {err.response.status_code}')

    def stream(self,query:str,json=False)->Generator[str,None,None]:
        headers=self.headers
        temperature=self.temperature
        url=self.base_url or "http://localhost:11434/api/generate"
        payload={
            "model": self.model,
            "prompt": query,
            "options":{
                "temperature": temperature,
            },
            "format":'json' if json else '',
            "stream":True
        }
        try:
            response=post(url=url,json=payload,headers=headers,stream=True)
            response.raise_for_status()
            chunks=response.iter_lines(decode_unicode=True)
            return (loads(chunk)['response'] for chunk in chunks)
        except HTTPError as err:
            print(f'Error: {err.response.text}, Status Code: {err.response.status_code}')
        except ConnectionError as err:
            print(err)
        exit()
    
    def available_models(self):
        url='http://localhost:11434/api/tags'
        headers=self.headers
        response=get(url=url,headers=headers)
        response.raise_for_status()
        models=response.json()
        return [model['name'] for model in models['models']]
