from tenacity import retry,stop_after_attempt,retry_if_exception_type
from requests import post,RequestException,HTTPError,ConnectionError
from src.message import AIMessage,BaseMessage
from src.inference import BaseInference
from termcolor import colored
from typing import Generator
from json import loads

class ChatGroq(BaseInference):
    # @retry(stop=stop_after_attempt(3),retry=retry_if_exception_type(RequestException))
    def invoke(self, messages: list[BaseMessage],json:bool=False)->AIMessage:
        self.headers.update({'Authorization': f'Bearer {self.api_key}'})
        headers=self.headers
        temperature=self.temperature
        url=self.base_url or "https://api.groq.com/openai/v1/chat/completions"
        messages=[message.to_dict() for message in messages]
        payload={
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream":False,
        }
        if json:
            payload["response_format"]={
                "type": "json_object"
            }
        try:
            response=post(url=url,json=payload,headers=headers)
            response.raise_for_status()
            json_object=response.json()
            # print(json_object)
            if json_object.get('error'):
                raise Exception(json_object['error']['message'])
            if json:
                content=loads(json_object['choices'][0]['message']['content'])
            else:
                content=json_object['choices'][0]['message']['content']
            return AIMessage(content)
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
            "stream":True,
        }
        if json:
            payload["response_format"]={
                "type": "json_object"
            }
        try:
            response=post(url=url,json=payload,headers=headers)
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