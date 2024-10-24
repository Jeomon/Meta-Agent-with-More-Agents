import { createStore } from "vuex";

const store=createStore({
    state: {
        query: '',
        messages: []
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
        }
    },
    actions:{

    },
})

export default store