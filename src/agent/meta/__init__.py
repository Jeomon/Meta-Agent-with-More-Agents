from src.agent.meta.utils import extract_from_xml,read_markdown_file
from langchain_core.runnables.graph import MermaidDrawMethod
from src.message import SystemMessage,HumanMessage
from src.agent.meta.state import AgentState
from langgraph.graph import StateGraph,END
from IPython.display import display,Image
from src.inference import BaseInference
from src.agent.react import ReactAgent
from src.agent.cot import COTAgent
from src.agent import BaseAgent
from termcolor import colored
from typing import Generator

class MetaAgent(BaseAgent):
    def __init__(self,llm:BaseInference=None,agents:list[dict]=[],tools:list=[],max_iteration=10,verbose=False):
        self.name='Meta Agent'
        self.description='This agent orchestrates the problem-solving process by breaking down queries into sub-tasks and assigning each to the most suitable agent.'
        self.llm=llm
        self.max_iteration=max_iteration
        self.iteration=0
        self.agents=[f'Name: {agent["name"]}\nDescription: {agent["description"]}\nTools: {','.join([tool.name for tool in agent["tools"]])}' for agent in agents]
        self.tools=tools or [tool for agent in agents for tool in agent['tools']]
        self.tool_names=[tool.name for tool in tools]
        self.system_prompt=read_markdown_file('./src/agent/meta/prompt.md')
        self.graph=self.create_graph()
        self.verbose=verbose

    def meta_expert(self,state:AgentState):
        llm_response=self.llm.invoke(state['messages'])
        # print(llm_response.content)
        agent_data=extract_from_xml(llm_response.content)
        name=agent_data.get('Agent Name')
        description=agent_data.get('Agent Description')
        tasks=agent_data.get('Tasks')
        tool=agent_data.get('Tool')
        answer=agent_data.get('Answer')
        if not answer:
            content=f'Agent Name: {name}\nDescription: {description}\nTasks: {tasks}\nTool: {tool}'
            print_stmt=colored(content,color='yellow',attrs=['bold'])
        else:
            content=answer
            print_stmt=colored(f'Final Answer: {content}',color='cyan',attrs=['bold'])
        if self.verbose:
            print(print_stmt)
        return {**state,'current_agent':name,'agent_data':agent_data,'messages':[HumanMessage(content)]}

    def react_expert(self,state:AgentState):
        agent_data=state.get('agent_data')
        name=agent_data.get('Agent Name')
        query=agent_data.get('Agent Query')
        description=agent_data.get('Agent Description')
        instructions=agent_data.get('Tasks')
        # tool=agent_data.get('Tool')
        agent=ReactAgent(name=name,description=description,instructions=instructions,tools=self.tools,llm=self.llm,verbose=self.verbose)
        if self.iteration==1:
            agent_response=agent.invoke(f'Query: {query}')
        else:
            previous_agent_message=state['messages'][-2] #Message before the meta agent.
            agent_response=agent.invoke(f'Query: {query}\nInformation: {previous_agent_message.content}')
        return {**state, 'messages':[HumanMessage(f'Name: {name}\nResponse: {agent_response}')],'agent_data':None}

    def cot_expert(self,state:AgentState):
        agent_data=state.get('agent_data')
        name=agent_data.get('Agent Name')
        query=agent_data.get('Agent Query')
        description=agent_data.get('Agent Description')
        instructions=agent_data.get('Tasks')
        agent=COTAgent(name=name,description=description,instructions=instructions,llm=self.llm,verbose=self.verbose)
        if self.iteration==1:
            agent_response=agent.invoke(f'Query: {query}')
        else:
            previous_agent_message=state['messages'][-2] #Message before the meta agent.
            agent_response=agent.invoke(f'Query: {query}\nInformation: {previous_agent_message.content}')
        return {**state, 'messages':[HumanMessage(f'Name: {name}\nResponse: {agent_response}')],'agent_data':None}

    def final(self,state:AgentState):
        if self.max_iteration>self.iteration:
            output=state['messages'][-1].content
        else:
            output='Iteration limit reached'
        return {**state, 'output':output,'current_agent':''}
    
    def controller(self,state:AgentState):
        if self.max_iteration>self.iteration:
            self.iteration+=1
            agent_data=state.get('agent_data')
            if agent_data.get('Answer'):
                return 'Answer'
            elif agent_data.get('Tool'):
                return 'React'
            else:
                return 'COT'
        else:
            return 'Answer'

    def create_graph(self):
        graph=StateGraph(AgentState)
        graph.add_node('Meta',self.meta_expert)
        graph.add_node('React',self.react_expert)
        graph.add_node('COT',self.cot_expert)
        graph.add_node('Answer',self.final)

        graph.set_entry_point('Meta')
        graph.add_conditional_edges('Meta',self.controller)
        graph.add_edge('React','Meta')
        graph.add_edge('COT','Meta')
        graph.add_edge('Answer',END)

        return graph.compile(debug=False)
    
    def plot_mermaid(self):
        '''
        Mermaid plot for the agent.
        '''
        plot=self.graph.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.API)
        return display(Image(plot))

    def invoke(self, input: str)->str|Generator:    
        if self.verbose:
            print(f'Entering '+colored(self.name,'black','on_white'))
        system_prompt=self.system_prompt.format(agents='\n\n'.join(self.agents),tool_names=self.tool_names)
        user_prompt=f'User Query: {input}'
        state={
            'input':input,
            'messages':[SystemMessage(system_prompt),HumanMessage(user_prompt)],
            'agent_data':{},
            'current_agent':self.name,
            'output':'',
        }
        response=self.graph.invoke(state)
        print('='*100)
        return response['output']

    def stream(self, input: str):
        if self.verbose:
            print(f'Entering '+colored(self.name,'black','on_white'))
        system_prompt=self.system_prompt.format(agents='\n\n'.join(self.agents),tool_names=self.tool_names)
        user_prompt=f'User Query: {input}'
        state={
            'input':input,
            'messages':[SystemMessage(system_prompt),HumanMessage(user_prompt)],
            'agent_data':{},
            'current_agent':self.name,
            'output':'',
        }
        return self.graph.stream(state,stream_mode='values',output_keys=['output'])