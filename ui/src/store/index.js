import axios from "axios";
import { createStore } from "vuex";

const store=createStore({
    state: {
        query: '',
        messages: [],
        agents:[],
        tools:[]
    },
    getters:{
        getQuery(state) {
            return state.query
        },
        getMessages(state) {
            return state.messages
        },
        getLastMessage(state) {
            return state.messages[state.messages.length - 1]
        },
        getAgents(state) {
            return state.agents
        },
        getTools(state) {
            return state.tools
        }
    },
    mutations:{
        setQuery(state, query) {
            state.query = query;
        },
        addMessage(state, message) {
            state.messages.push(message)
        },
        updateMessage(state, {id, content}) {
            const message = state.messages.find(m => m.id === id)
            if (message) {
                message.content = content
            }
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
        }
    }
})

export default store