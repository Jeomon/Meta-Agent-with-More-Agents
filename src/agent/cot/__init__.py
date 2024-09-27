from src.agent.cot.utils import extract_llm_response,read_markdown_file
from langchain_core.runnables.graph import MermaidDrawMethod
from src.message import SystemMessage,HumanMessage
from src.agent.cot.state import AgentState
from IPython.display import display,Image
from src.inference import BaseInference
from langgraph.graph import StateGraph
from src.agent import BaseAgent
from termcolor import colored
from time import sleep

class COTAgent(BaseAgent):
    def __init__(self,name:str='',description:str='',instructions:list[str]=[],llm:BaseInference=None,max_iteration=10,json=False,verbose=False):
        self.name=name
        self.description=description
        self.instructions=self.get_instructions(instructions)
        self.llm=llm
        self.max_iteration=max_iteration
        self.graph=self.create_graph()
        self.verbose=verbose
        self.iteration=0
        self.system_prompt=read_markdown_file('./src/agent/cot/prompt.md')

    def get_instructions(self,instructions):
        return '\n'.join([f'{i+1}. {instruction}' for i,instruction in enumerate(instructions)])

    def reason(self,state:AgentState):
        if self.max_iteration>self.iteration:
            if self.iteration%2!=0:
                sleep(60) #To prevent from hitting the API rate limit
            llm_response=self.llm.invoke(state['messages'])
            # print(llm_response.content)
            agent_data=extract_llm_response(llm_response.content)
        else:
            agent_data={
                'Thought':'I reached the iteration limit',
                'Answer':'Iteration limit reached'
            }
        if self.verbose:
            if agent_data.get('Observation'):
                print(colored(f'Thought: {agent_data.get('Thought')}',color='green',attrs=['bold']))
                print(colored(f'Observation: {agent_data.get("Observation")}',color='cyan',attrs=['bold']))
        return {**state, 'messages':[HumanMessage(llm_response.content)],'agent_data':agent_data}
    
    def reflection(self,state:AgentState):
        agent_data=state['agent_data']
        if self.verbose:
            if agent_data.get('Reflection'):
                print(colored(f'Thought: {agent_data.get('Thought')}',color='green',attrs=['bold']))
                print(colored(f'Reflection: {agent_data.get("Reflection")}',color='magenta',attrs=['bold']))
        return {**state, 'agent_data':agent_data}

    def controller(self,state:AgentState):
        if self.max_iteration>self.iteration:
            self.iteration+=1
            return state['agent_data']['Route'].lower()
        else:
            return 'answer'

    def final(self,state:AgentState):
        agent_data=state['agent_data']
        if self.verbose:
            if state['agent_data']['Final Answer']:
                print(colored(f'Thought: {agent_data.get('Thought')}',color='green',attrs=['bold']))
                print(colored(f'Answer: {agent_data.get("Final Answer")}',color='blue',attrs=['bold']))
        return {**state, 'output':agent_data.get("Final Answer")}
    
    def create_graph(self):
        graph=StateGraph(AgentState)
        graph.add_node('reason',self.reason)
        graph.add_node('answer',self.final)
        graph.add_node('reflection',self.reflection)
        graph.set_entry_point('reason')
        graph.add_conditional_edges('reason',self.controller)
        graph.add_edge('reflection','reason')
        graph.set_finish_point('answer')

        return graph.compile(debug=False)

    def plot_mermaid(self):
        '''
        Mermaid plot for the agent.
        '''
        plot=self.graph.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.API)
        return display(Image(plot))

    def invoke(self, input: str):
        if self.verbose:
            print(f'Entering '+colored(self.name,'black','on_white'))  
        parameters={
            'name':self.name,
            'description':self.description,
            'instructions':self.instructions,
        }
        system_prompt=self.system_prompt.format(**parameters) 
        user_prompt=f'Query: {input}' 
        state={
            'input':input,
            'messages':[SystemMessage(system_prompt),HumanMessage(user_prompt)],
            'output':'',
        }
        graph_response=self.graph.invoke(state)
        return graph_response['output']

    def stream(self, input: str):
        pass