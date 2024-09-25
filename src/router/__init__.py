from src.message import HumanMessage,SystemMessage
from src.router.utils import read_markdown_file
from src.inference import BaseInference
from json import dumps

class LLMRouter:
    def __init__(self,routes:list[dict]=[],llm:BaseInference=None,verbose=False):
        self.system_prompt=read_markdown_file('./src/router/prompt.md')
        self.routes=dumps(routes,indent=2)
        self.llm=llm
        self.verbose=verbose
    
    def invoke(self,query:str)->dict:
        messages=[SystemMessage(self.system_prompt.format(routes=self.routes)),HumanMessage(query)]
        response=self.llm.invoke(messages,json=True)
        route=response.content.get('route')
        if self.verbose:
            print(f"Going to {route.upper()} route")
        return route
