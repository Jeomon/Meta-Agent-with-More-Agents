import axios from "axios";
import { createStore } from "vuex";

const store=createStore({
    state: {
        conversation:{},
        messages: [],
        conversations:[],
        agents:[],
        tools:[],
        integrations:[]
    },
    getters:{
        getConversation(state){
            return state.conversation
        },
        getConversations(state){
            return state.conversations
        },
        getMessages(state) {
            return state.messages
        },
        getAgents(state) {
            return state.agents
        },
        getTools(state) {
            return state.tools
        },
        getIntegrations(state){
            return state.integrations
        }
    },
    mutations:{
        addMessage(state, message) {
            state.messages.push(message)
        },
        updateMessage(state, {id, content}) {
            const message = state.messages.find(message => message.id === id)
            if (message) {
                message.content = content
            }
        },
        getMessages(state,messages){
            state.messages=messages
        },
        addAgent(state,agent){
            state.agents.push(agent)
        },
        getAgents(state,agents){
            state.agents=agents
        },
        deleteAgent(state,id){
            state.agents=state.agents.filter(agent=>agent.id!=id)
        },
        addTool(state,tool){
            state.tools.push(tool)
        },
        deleteTool(state,id){
            state.tools=state.tools.filter(tool=>tool.id!=id)
        },
        getTools(state,tools){
            state.tools=tools
        },
        getIntegrations(state,integrations){
            state.integrations=integrations
        },
        addIntegration(state,integration){
            state.integrations.push(integration)
        },
        editIntegration(state,{id,name,key}){
            let integration=state.integrations.find(integration=>integration.id==id)
            state.integrations=state.integrations.filter(integration=>integration.id!=id)
            integration.key=key
            state.integrations.push(integration)
        },
        deleteIntegration(state,id){
            state.integrations=state.integrations.filter(integration=>integration.id!=id)
        },
        getConversations(state,conversations){
            state.conversations=conversations
        },
        addConversation(state,conversation){
            state.conversations.push(conversation)
        },
        getConversation(state,{id,title,messages}){
            state.conversation={id,title}
            state.messages=messages
        },
        deleteConversation(state,id){
            state.conversations=state.conversations.filter(conversation=>conversation.id!=id)
        }
    },
    actions:{
        async addAgent({commit},{name,description,tools}){
            let response=await axios.post(`agent/add`,JSON.stringify({name,description,tools}))
            let data= response.data
            if (data.status=='success'){ 
                commit('createAgent',data.agent)
            }
            console.log(data.message)
        },
        async getAgents({commit}){
            let response=await axios.get(`agent/all`)
            let data= response.data
            if (data.status=='success'){ 
                let agents=data.agents
                commit('getAgents',agents)
            }
            console.log(data.message)
        },
        async deleteAgent({commit},{id}){
            let response=await axios.delete(`agent/delete/${id}`)
            let data= response.data
            if (data.status=='success'){
                commit('deleteAgent',id)
            }
            console.log(data.message)
        },
        async getTools({commit}){
            let response=await axios.get(`tool/all`)
            let data= response.data
            if (data.status=='success'){
                let tools=data.tools
                commit('getTools',tools)
            }
            console.log(data.message)
        },
        async deleteTool({commit},{id}){
            let response=await axios.delete(`tool/delete/${id}`)
            let data= response.data
            if (data.status=='success'){
                commit('deleteTool',id)
            }
            console.log(data.message)
        },
        async addTool({commit},definition){
            let response=await axios.post(`tool/add`,JSON.stringify(definition))
            let data= response.data
            if (data.status=='success'){ 
                let tool=data.tool
                commit('addTool',tool)
            }
            console.log(data.message)
        },
        async getIntegrations({commit}){
            let response=await axios.get(`integration`)
            let data= response.data
            if (data.status=='success'){ 
                let integrations=data.integrations
                commit('getIntegrations',integrations)
            }
            console.log(data.message)
        },
        async addIntegration({commit},integration){
            let response=await axios.post(`integration`,JSON.stringify(integration))
            let data=response.data
            if (data.status=='success'){ 
                let integration=data.integration
                commit('addIntegration',integration)
            }
            console.log(data.message)
        },
        async editIntegration({commit},integration){
            let response=await axios.put(`integration`,integration)
            let data=response.data
            if (data.status=='success'){
                let integration=data.integration
                commit('editIntegration',integration)
            }
            console.log(data.message);
        },
        async deleteIntegration({commit},{id}){
            let response=await axios.delete(`integration/${id}`)
            let data= response.data
            if (data.status=='success'){
                commit('deleteIntegration',id)
            }
            console.log(data.message);
        },
        async getConversations({commit}){
            let response=await axios.get(`conversation`)
            let data=response.data
            if(data.status=='success'){
                let conversations=data.conversations
                commit('getConversations',conversations)
            }
            console.log(data.message);
        },
        async getConversation({commit},conversation_id){
            let response=await axios.get(`conversation/${conversation_id}`)
            let data=response.data
            if(data.status=='success'){
                let conversation=data.conversation
                commit('getConversation',conversation)
            }
            console.log(data.message);
        },
        async addConversation({commit},title){
            let response=await axios.post(`conversation`,JSON.stringify({
                'title':title
            }))
            let data=response.data
            if(data.status=='success'){
                let conversation=data.conversation
                commit('addConversation',conversation)
            }
            console.log(data.message);
        },
        async deleteConversation({commit},id){
            let response=await axios.delete(`conversation/${id}`)
            let data=response.data
            if(data.status=='success'){
                commit('deleteConversation',id)
            }
            console.log(data.message);
        },
        async addMessage({commit},message){
            let response=await axios.post(`message`,JSON.stringify(message))
            let data=response.data
            if(data.status=='success'){
                let message=data.current_message
                commit('addMessage',message)
            }
            console.log(data.message);
        },
        
    }
})

export default store