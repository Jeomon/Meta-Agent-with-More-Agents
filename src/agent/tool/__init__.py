from src.agent.tool.utils import (extract_tools_from_module,
update_tool_to_module,save_tool_to_module,remove_tool_from_module,
read_markdown_file)
from langchain_core.runnables.graph import MermaidDrawMethod
from src.message import HumanMessage,SystemMessage
from src.agent.tool.state import AgentState
from langgraph.graph import StateGraph,END
from importlib import import_module,reload
from IPython.display import display,Image
from src.inference import BaseInference
from src.router import LLMRouter
from src.agent import BaseAgent
from termcolor import colored
from subprocess import run
import ast
import os

class ToolAgent(BaseAgent):
    def __init__(self,location:str='',llm:BaseInference=None,verbose=False,json=False):
        self.name='Tool Agent'
        self.location=location
        self.llm=llm
        self.verbose=verbose
        self.graph=self.create_graph()

    def create_module(self):
        if not os.path.exists(self.location):
            content='''from src.tool import tool\nfrom pydantic import BaseModel, Field\nfrom dotenv import load_dotenv\nfrom typing import *\nimport os\nload_dotenv()\n\n'''
            with open(self.location,'w',encoding='utf-8') as f:
                f.write(content)
            print(f'{self.location} has been created successfully.')

    def generate_tool(self,state:AgentState):
        system_prompt=read_markdown_file('./src/agent/tool/prompt/generate.md')
        user_prompt='**Query:**\n`{query}`'
        system_message=SystemMessage(system_prompt)
        human_message=HumanMessage(user_prompt.format(query=state.get('input')))
        tool_data=self.llm.invoke([system_message,human_message],json=True)
        try:
            ast.parse(tool_data.content.get('tool'))
            error=''
            save_tool_to_module(self.location,tool_data.content)
            if self.verbose:
                print(f'{tool_data.content.get("name")} has been saved to {self.location} successfully.')
        except Exception as e:
            error=e
            print(f'Error: {error}')
        return {**state,'tool_data':tool_data.content,'error':error}

    def update_tool(self,state:AgentState):
        tool=self.find_the_tool(state.get('input'))
        system_prompt=read_markdown_file('./src/agent/tool/prompt/update.md')
        user_prompt='Use the following inputs to guide the tool update:\n\n**Tool Definition (Existing):**\n`{tool_definition}`\n**Query (Modification Required):**\n`{query}`'
        human_message=HumanMessage(user_prompt.format(tool_definition=tool.get('tool'),query=state.get('input')))
        system_message=SystemMessage(system_prompt)
        updated_tool_data=self.llm.invoke([system_message,human_message],json=True)
        try:
            ast.parse(updated_tool_data.content.get('tool'))
            error=''
            update_tool_to_module(self.location,updated_tool_data.content)
            if self.verbose:
                print(f'Updated {updated_tool_data.content.get("name")} and saved to {self.location} successfully.')
        except Exception as e:
            error=e
            print(f'Error: {error}')
        return {**state,'tool_data':updated_tool_data.content,'error':error}
    
    def debug_tool(self,state:AgentState):
        if state.get('route')=='debug':
            error=state.get('input')
            tool_data=self.find_the_tool(error)
        elif state.get('error'):
            error=state.get('error')
            tool_data=state.get('tool_data')
        iteration=0
        max_iteration=5
        while error and iteration<max_iteration:
            system_prompt=read_markdown_file('./src/agent/tool/prompt/debug.md')
            system_message=SystemMessage(system_prompt)
            user_prompt='Use the following inputs to guide the tool debugging:\n\n**Tool Definition:**\n`{tool_definition}`\n**Error Message:**\n`{error_message}`'
            human_message=HumanMessage(user_prompt.format(tool_definition=tool_data.get('tool'),error_message=error))
            debug_tool_data=self.llm.invoke([system_message,human_message],json=True).content
            try:
                ast.parse(debug_tool_data.get('tool'))
                error=''
                update_tool_to_module(self.location,debug_tool_data.content)
                if self.verbose:
                    print(f'Fixed {debug_tool_data.get('name')} and saved to {self.location} successfully.')
            except Exception as e:
                error=e
                iteration+=1
        return {**state,'tool_data':debug_tool_data,'error':error}
    
    def delete_tool(self,state:AgentState):
        tool=self.find_the_tool(state.get('input'))
        tool_data={
            'name':tool.get('tool_name'),
            'tool_name':tool.get('func_name'),
            'tool':tool.get('tool')
        }
        remove_tool_from_module(self.location,tool_data)
        if self.verbose:
            print(f'{tool_data.get("tool_name")} has been removed from {self.location} successfully.')
        return {**state,'tool_data':tool_data}
    
    def reloader(self,state:AgentState):
        route=state.get('route').lower()
        module=import_module(self.location.split('.')[0])
        reload(module)
        tool=getattr(module,state.get('tool_data')['tool_name'])
        tool_name=state.get('tool_data')['name']
        tool_args=tool.schema if tool.schema.get('properties') else {}
        if route=='update':
            output=f'Tool Name: {tool_name}\nTool Input: {tool_args}\n Tool has been updated successfully.'
        elif route=='debug':
            output=f'Tool Name: {tool_name}\nTool Input: {tool_args}\n Tool has been debugged successfully.'
        elif route=='generate':
            output=f'Tool Name: {tool_name}\nTool Input: {tool_args}\n Tool has been generated successfully.'
        elif route=='delete':
            output=f'Tool Name: {tool_name}\nTool Input: {tool_args}\n Tool has been deleted successfully.'
        return {**state,"output":output}

    def find_the_tool(self,query:str):
        tools=extract_tools_from_module(self.location)
        specific_tool=None
        for tool in tools:
            if tool.get('tool_name') in query:
                specific_tool=tool
                break
        return specific_tool
    
    def package_installer(self,state:AgentState):
        system_prompt=read_markdown_file('./src/agent/tool/prompt/package_installer.md')
        llm_response=self.llm.invoke([SystemMessage(system_prompt.format(query=state.get('input')))],json=True)
        cmd=llm_response.content.get('command')
        process=run(cmd.split(' '),text=True,capture_output=True)
        if process.returncode!=0:
            print(process.stderr.strip())
            output='Package installation failed.'
        else:
            print(process.stdout.strip())
            output='Package installed successfully.'
        return {**state,'output':output}
    
    def router(self,state:AgentState):
        routes=[
            {
                'name':'update',
                'description':'This route is used if the query is to update or modify an existing tool implementation because of lack of information or not working as expected.'
            },
            {
                'name':'debug',
                'description':'This route is used if the query is to fix errors or bugs that encountered when the tool is executed also the required pythom libraries for the tool is missing.'
            },
            {
                'name':'generate',
                'description':'This route is used if the query is to create or generate new tool to serve the purpose.'
            },
            {
                'name': 'delete',
                'description':'This route is used if the query is to delete an existing tool because it is not working as expected and giving errors even after debugging.'
            },
            {
                'name':'package',
                'description':'This route is used if the query is to install a missing module or library, update or modify an existing library and remove packages for the tool.'
            }
        ]
        llm_router=LLMRouter(routes=routes,llm=self.llm,verbose=False)
        route=llm_router.invoke(state.get('input'))
        return {**state,'route':route}

    def controller(self,state:AgentState):
        return state.get('route')

    def sub_controller(self,state:AgentState):
        return 'debug' if state.get('error') else 'reloader'

    def create_graph(self):
        workflow=StateGraph(AgentState)

        workflow.add_node('router',self.router)
        workflow.add_node('package',self.package_installer)
        workflow.add_node('generate',self.generate_tool)
        workflow.add_node('update',self.update_tool)
        workflow.add_node('debug',self.debug_tool)
        workflow.add_node('delete',self.delete_tool)
        workflow.add_node('reloader',self.reloader)
        
        workflow.set_entry_point('router')
        workflow.add_conditional_edges('router',self.controller)
        workflow.add_conditional_edges('generate',self.sub_controller)
        workflow.add_conditional_edges('update',self.sub_controller)
        workflow.add_edge('debug','reloader')
        workflow.add_edge('package',END)
        workflow.add_edge('reloader',END)
        workflow.add_edge('delete',END)
        
        return workflow.compile(debug=False)

    def plot_mermaid(self):
        '''
        Mermaid plot for the agent.
        '''
        plot=self.graph.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.API)
        return display(Image(plot))

    def invoke(self,input:str)->dict[str,str]:
        if self.verbose:
            print(f'Entering '+colored(self.name,'black','on_white'))  
            print(colored(f'Query: {input}',color='grey',attrs=['bold']))
        state={
            'input':input,
            'route':'',
            'tool_data':{},
            'error':'',
            'output':''
        }
        self.create_module()
        llm_response=self.graph.invoke(state)
        tool_data=llm_response.get('tool_data')
        route=llm_response.get('route')
        output=llm_response.get('output')
        return {
            'route':route,
            'func_name': tool_data.get('tool_name'),
            'tool_name': tool_data.get('name'),
            'tool': tool_data.get('tool'),
            'output':output
        }
    
    def stream(self, input: str):
        pass