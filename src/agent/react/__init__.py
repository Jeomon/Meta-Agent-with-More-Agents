from src.agent.react.utils import extract_llm_response,read_markdown_file
from src.message import AIMessage,HumanMessage,SystemMessage
from langchain_core.runnables.graph import MermaidDrawMethod
from src.tool.prebuilt import user_interface_tool
from src.agent.react.state import AgentState
from importlib import reload,import_module
from IPython.display import display,Image
from src.inference import BaseInference
from langgraph.graph import StateGraph
from src.agent.tool import ToolAgent
from src.agent import BaseAgent
from termcolor import colored
from platform import system
from getpass import getuser
from os import getcwd
import json

class ReactAgent(BaseAgent):
    def __init__(self,name:str='',description:str='',instructions:list[str]=[],tools:list=[],llm:BaseInference=None,max_iterations=10,dynamic_tools_file:str='experimental.py',json=False,verbose=False):
        self.name=name
        self.description=description
        self.instructions=self.get_instructions(instructions)
        self.system_prompt=read_markdown_file('./src/agent/react/prompt.md')
        self.max_iterations=max_iterations
        self.tool_names=[]
        self.tools_description=[]
        self.tools={}
        self.iteration=0
        self.dynamic_tools_file=dynamic_tools_file
        self.dynamic_tools_module=import_module(dynamic_tools_file.split('.')[0])
        self.llm=llm
        self.verbose=verbose
        self.graph=self.create_graph()
        self.add_tools_to_toolbox([user_interface_tool,*tools])

    def reason(self,state:AgentState):
        message=self.llm.invoke(state['messages'])
        response=extract_llm_response(message.content)
        # print(message.content)
        thought=response.get('Thought')
        if self.verbose:
            print(colored(f'Thought: {thought}',color='green',attrs=['bold']))
        return {**state,'messages':[message]}

    def get_instructions(self,instructions):
        return '\n'.join([f'{i+1}. {instruction}' for i,instruction in enumerate(instructions)])

    def add_tools_to_toolbox(self,tools):
        for tool in tools:
            self.tool_names.append(tool.name)
            self.tools_description.append(json.dumps({
                'Tool Name': tool.name,
                'Tool Input': tool.schema if tool.schema.get('properties') else {},
                'Tool Description': tool.description
            },indent=2))
            self.tools[tool.name]=tool

    def update_tool_in_toolbox(self,tool):
        for index,tool_name in enumerate(self.tool_names):
            if tool_name==tool.name:
                self.tools_description[index]=json.dumps({
                    'Tool Name': tool.name,
                    'Tool Input': tool.schema if tool.schema.get('properties') else {},
                    'Tool Description': tool.description
                },indent=2)
                self.tools[tool.name]=tool
                break
    
    def remove_tool_from_toolbox(self,_tool_name):
        for index,tool_name in enumerate(self.tool_names):
            if tool_name==_tool_name:
                self.tool_names.pop(index)
                self.tools_description.pop(index)
                self.tools.pop(_tool_name)
                break

    def action(self,state:AgentState):
        message=(state['messages'][-1])
        response=extract_llm_response(message.content)
        thought=response.get('Thought')
        action_name=response.get('Action Name')
        action_input=response.get('Action Input')
        route=response.get('Route')
        if self.verbose:
            print(colored(f'Action Name: {action_name}',color='cyan',attrs=['bold']))
            print(colored(f'Action Input: {json.dumps(action_input,indent=2)}',color='cyan',attrs=['bold']))
        if action_name not in self.tool_names:
            observation="This tool is not available in the tool box."
        else:
            tool=self.tools[action_name]
            try:
                observation=tool(**action_input)
            except Exception as e:
                observation=str(e)
        if self.verbose:
            print(colored(f'Observation: {observation}',color='magenta',attrs=['bold']))
        state['messages'].pop()
        messages=[
            AIMessage(f'<Thought>{thought}</Thought>\n<Action Name>{action_name}</Action Name>\n<Action Input>{json.dumps(action_input,indent=2)}</Action Input>\n<Route>{route}</Route>'),
            HumanMessage(f'<Observation>{observation}</Observation>')]
        return {**state,'messages':messages}

    def tool_agent(self,state:AgentState):
        message=(state['messages'][-1])
        response=extract_llm_response(message.content)
        query=response.get('Query')
        generator=ToolAgent(location=self.dynamic_tools_file,llm=self.llm,verbose=self.verbose,json=True)
        tool_info=generator.invoke(query)
        tool_name=tool_info.get('tool_name')
        func_name=tool_info.get('func_name')
        output=tool_info.get('output')
        route=tool_info.get('route')
        reload(self.dynamic_tools_module)
        if route=='delete':
            self.remove_tool_from_toolbox(tool_name)
            content=f'{output} Now the tool is removed from the tool box.'        
        else:
            try:
                tool=getattr(self.dynamic_tools_module,func_name)
            except Exception as e:
                print(e)
            if route=='generate':
                self.add_tools_to_toolbox([tool])
            if route=='update':
                self.update_tool_in_toolbox(tool)
            if route=='debug':
                self.update_tool_in_toolbox(tool)
            content=f'{output} Now the tool is available in the tool box and ready for use.'
        
        if self.verbose:
            print(colored(content,color='cyan',attrs=['bold']))
        return {**state,'messages':[HumanMessage(content)]}

    def final(self,state:AgentState):
        if self.max_iterations>self.iteration:
            message=state['messages'][-1]
            response=extract_llm_response(message.content)
            final_answer=response.get('Final Answer')
        else:
            final_answer="The maximum number of iterations has been reached."
        if self.verbose:
            print(colored(f'Answer: {final_answer}',color='blue',attrs=['bold']))
        return {**state,'output':final_answer}
    
    def controller(self,state:AgentState):
        if self.max_iterations>self.iteration:
            self.iteration+=1
            message=(state['messages'][-1])
            response=extract_llm_response(message.content)
            return response.get('Route').lower()
        else:
            return 'final'

    def create_graph(self):
        workflow=StateGraph(AgentState)

        workflow.add_node('reason',self.reason)
        workflow.add_node('action',self.action)
        workflow.add_node('final',self.final)
        workflow.add_node('tool',self.tool_agent)

        workflow.set_entry_point('reason')
        workflow.add_conditional_edges('reason',self.controller)
        workflow.add_edge('tool','reason')
        workflow.add_edge('action','reason')
        workflow.set_finish_point('final')

        return workflow.compile(debug=False)

    def plot_mermaid(self):
        '''
        Mermaid plot for the agent.
        '''
        plot=self.graph.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.API)
        return display(Image(plot))

    def invoke(self,input:str)->str:
        if self.verbose:
            print(f'Entering '+colored(self.name,'black','on_white'))
        parameters={
            'name':self.name,
            'description':self.description,
            'instructions':self.instructions,
            'tools':f'[{',\n'.join(self.tools_description)}]',
            'tool_names':self.tool_names
        }
        system_prompt=self.system_prompt.format(**parameters)
        user_prompt=f"Question:{input}\n Operating System:{system()}\nUser:{getuser()}\nCWD:{getcwd()}"
        state={
            'input':input,
            'messages':[SystemMessage(system_prompt),HumanMessage(user_prompt)],
            'output':'',
        }
        response=self.graph.invoke(state)
        return response['output']

    def stream(self, input: str):
        if self.verbose:
            print(f'Entering {self.name}')
        parameters={
            'name':self.name,
            'description':self.description,
            'instructions':self.instructions,
            'tools':f'[{',\n'.join(self.tools_description)}]',
            'tool_names':self.tool_names
        }
        system_prompt=self.system_prompt.format(**parameters)
        user_prompt=f"Question:{input}\n Operating System:{system()}\nUser:{getuser()}\nCWD:{getcwd()}"
        state={
            'input':input,
            'messages':[SystemMessage(system_prompt),HumanMessage(user_prompt)],
            'output':'',
        }
        events=self.graph.stream(state)
        for event in events:
            for value in event.values():
                if value['output']:
                    yield value['output']