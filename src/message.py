from io import BytesIO
from abc import ABC
import requests
import base64
import re

class BaseMessage(ABC):
    def to_dict(self)->dict[str,str]:
        return {
            'role': self.role,
            'content': f'''{self.content}'''
        }
    def __repr__(self):
        class_name = self.__class__.__name__
        attributes = ", ".join(f"{key}={value}" for key, value in self.__dict__.items())
        return f"{class_name}({attributes})"

class HumanMessage(BaseMessage):
    def __init__(self,content):
        self.role='user'
        self.content=content

class AIMessage(BaseMessage):
    def __init__(self,content):
        self.role='assistant'
        self.content=content
        
class SystemMessage(BaseMessage):
    def __init__(self,content):
        self.role='system'
        self.content=content

class ImageMessage(BaseMessage):
    def __init__(self,text:str=None,image_path:str=None,image_base_64:str=None):
        self.role='user'
        if image_base_64 is not None or image_path is None:
            self.content=(text,image_base_64)
        elif image_path is not None or image_base_64 is None:
            self.content=(text,self.__image_to_base64(image_path))
        else:
            raise Exception('image_path and image_base_64 cannot be both None or both not None')
    
    def __is_url(self,image_path:str)->bool:
        url_pattern = re.compile(r'^https?://')
        return url_pattern.match(image_path) is not None

    def __is_file_path(self,image_path:str)->bool:
        file_path_pattern = re.compile(r'^([./~]|([a-zA-Z]:)|\\|//)?\.?\/?[a-zA-Z0-9._-]+(\.[a-zA-Z0-9]+)?$')
        return file_path_pattern.match(image_path) is not None

    def __image_to_base64(self,image_source: str) -> str:
        if self.__is_url(image_source):
            response = requests.get(image_source)
            bytes = BytesIO(response.content)
            image_bytes = bytes.read()
        elif self.__is_file_path(image_source):
            with open(image_source, 'rb') as image:
                image_bytes = image.read()
        else:
            raise ValueError("Invalid image source. Must be a URL or file path.")
        return base64.b64encode(image_bytes).decode('utf-8')

class ToolMessage(BaseMessage):
    def __init__(self,content:str,tool_call:str,tool_args:dict):
        self.role='assistant'
        self.content=content
        self.tool_call=tool_call
        self.tool_args=tool_args