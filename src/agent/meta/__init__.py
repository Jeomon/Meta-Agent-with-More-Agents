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

class MetaAgent(BaseAgent):
    def __init__(self,llm:BaseInference=None,tools:list=[],max_iteration=10,json=False,verbose=False):
        self.name='Meta Agent'
        self.llm=llm
        self.max_iteration=max_iteration
        self.iteration=0
        self.tools=tools
        self.graph=self.create_graph()
        self.verbose=verbose
        self.system_prompt=read_markdown_file('./src/agent/meta/prompt.md')

    def meta_expert(self,state:AgentState):
        llm_response=self.llm.invoke(state['messages'])
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
            content=f'Final Answer: {answer}'
            print_stmt=colored(content,color='cyan',attrs=['bold'])
        if self.verbose:
            print(print_stmt)
        return {**state,'agent_data':agent_data,'messages':[HumanMessage(content)]}

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
        return {**state, 'output':output}
    
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

    def invoke(self, input: str)->str:    
        if self.verbose:
            print(f'Entering '+colored(self.name,'black','on_white'))  
        state={
            'input':input,
            'messages':[SystemMessage(self.system_prompt),HumanMessage(f'User Query: {input}')],
            'output':'',
        }
        graph_response=self.graph.invoke(state)
        print('='*100)
        return graph_response['output']

    def stream(self, input: str):
        pass