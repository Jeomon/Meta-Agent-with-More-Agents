import { get } from "@vueuse/core";
import axios from "axios";
import { createStore } from "vuex";

const store=createStore({
    state: {
        query: '',
        messages: [],
        agents:[]
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
        createAgent(state,agent){
            state.agents.push(agent)
        },
        getAgents(state,agents){
            state.agents=agents
        }
    },
    actions:{
        async createAgent({commit},agent){
            let response=await axios.post(`agent/add`,JSON.stringify(agent))
            let data= response.data
            if (data.status=='success'){ 
                commit('createAgent',agent)
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
    }
})

export default store