from langchain_core.runnables.graph import MermaidDrawMethod
from IPython.display import Image,display
from abc import ABC,abstractmethod
from src.message import AIMessage

class BaseInference(ABC):
    def __init__(self,model:str,api_key:str='',base_url:str='',temperature:float=0.5):
        self.model=model
        self.api_key=api_key
        self.base_url=base_url
        self.temperature=temperature
        self.headers={'Content-Type': 'application/json'}
    @abstractmethod
    def invoke(self,messages:list[dict])->AIMessage:
        pass

    def plot_mermaid(self):
        '''
        Mermaid plot for the agent.
        '''
        plot=self.graph.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.API)
        return display(Image(plot))