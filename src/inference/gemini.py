from src.message import AIMessage,BaseMessage,HumanMessage,ImageMessage,ToolMessage
from requests import post,get,RequestException,HTTPError,ConnectionError
from tenacity import retry,stop_after_attempt,retry_if_exception_type
from src.inference import BaseInference
from requests import post,get
from json import loads
from uuid import uuid4

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
                contents.append({
                    'role':'user',
                    'parts':[{
                        'text':message.content
                    }]
                })
            elif isinstance(message,AIMessage):
                contents.append({
                    'role':'model',
                    'parts':[{
                        'text':message.content
                    }]
                })
            elif isinstance(message,ImageMessage):
                text,image=message.content
                contents.append({
                        'role':'user',
                        'parts':[{
                            'text':text
                    },
                    {
                        'inline_data':{
                            'mime_type':'image/jpeg',
                            'data': image
                        }
                    }]
                })
            else:
                system_instruct={
                    'parts':{
                        'text': message.content
                    }
                }

        payload={
            'contents': contents,
            'generationConfig':{
                'temperature': temperature,
                'responseMimeType':'application/json' if json else 'text/plain'
            }
        }
        if self.tools:
            payload['tools']=[
                {
                    'function_declarations':[
                        {
                            'name': tool.name,
                            'description': tool.description,
                            'parameters': tool.schema
                        }
                    for tool in self.tools]
                }
            ]
        if system_instruct:
            payload['system_instruction']=system_instruct
        try:
            response=post(url=url,headers=headers,json=payload,params=params)
            json_obj=response.json()
            # print(json_obj)
            if json_obj.get('error'):
                raise Exception(json_obj['error']['message'])
           
            else:
                message=json_obj['candidates'][0]['content']['parts'][0]
                if json:
                    return AIMessage(loads(message['text']))
                if message.get('text'):
                    return AIMessage(message['text'])
                else:
                    tool_call=message['functionCall']
                    return ToolMessage(id=str(uuid4()),name=tool_call['name'],args=tool_call['args'])
        except HTTPError as err:
            print(f'Error: {err.response.text}, Status Code: {err.response.status_code}')
        except ConnectionError as err:
            print(err)
        exit()
    
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