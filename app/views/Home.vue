<template>
    <div class="h-screen grid grid-cols-6 grid-rows-4">
        <div class="col-span-1 row-span-4 flex flex-col gap-3 bg-slate-200 h-full w-full">
            <h1 class="text-3xl p-2">Chat History</h1>
            <div class="flex flex-col gap-2 px-3">
                <div class="flex flex-row items-center justify-between">
                    <p class="">Quantum Computing</p>
                    <img class="w-4 h-4 cursor-pointer" src="../assets/3-dot.svg"/>
                </div>
                <div class="flex flex-row items-center justify-between">
                    <p class="">Quantum Computing</p>
                    <img class="w-4 h-4 cursor-pointer" src="../assets/3-dot.svg"/>
                </div>
            </div>
        </div>
        <div class="col-span-5 row-span-4 h-full w-full">
            <div class="grid grid-rows-11 w-full h-full">
                <div class="row-span-1 flex justify-center items-center">
                    <img src="../assets/logo.svg" alt="logo" class="w-16 h-16 py-3">
                    <h1 class="text-4xl">MAMA</h1>
                </div>
                <div class="row-span-10">
                    <div class="grid grid-cols-8 grid-rows-9 w-full h-full">
                        <div class="row-span-8 col-span-1"></div>
                        <div class="row-span-8 col-span-6 p-5 overscroll-none">
                            <div class="flex flex-col items-center bg-slate-50 mt-12 px-6 py-5 rounded-2xl" v-if="messages.length==0">
                                <h1 class="text-3xl font-medium">👋 Welcome to the Meta Agent with More Agents! 🌟</h1>
                                <div class="flex flex-col gap-3 mt-5 text-base">
                                    <p>We&#39;re excited to have you here! This project is designed to make your problem-solving experience seamless and efficient. Our <strong>Meta Agent</strong> orchestrates a team of specialized AI agents to tackle complex queries and deliver precise solutions.</p>
                                    <p>✨ <strong>What can you do here?</strong></p>
                                    <ul class="list-disc list-inside">
                                        <li>Ask any question or provide a problem statement.</li>
                                        <li>Watch as our agents break down tasks and execute them step-by-step.</li>
                                        <li>Receive insightful answers based on the combined intelligence of our agents!</li>
                                    </ul>
                                    <p>💬 <strong>How can I help you today?</strong> Feel free to ask me anything, and let&#39;s embark on this journey of intelligent automation together! 🚀</p>
                                </div>
                            </div>
                            <div v-else class="flex flex-col gap-5 h-full overflow-y-auto overflow-x-hidden scroll-smooth">
                                <component :key="message.id" v-for="message in messages" :is="message.role==='user'?'HumanMessage':'AIMessage'" :content="message.content" :agent="message.agent"/>
                            </div>
                        </div>
                        <div class="row-span-8 col-span-1"></div>
                        <form @submit="submitHandler" class="row-span-1 col-span-full flex flex-row justify-center py-2 gap-3">
                            <button type="button" class="drop-shadow-md">
                                <svg class="w-10 h-10 bg-slate-200 rounded-full drop-shadow-md fill-slate-600" xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="18.25 18.25 63.5 63.5">
                                    <path d="m50.004 18.246c-17.512 0-31.75 14.238-31.75 31.75 0 17.512 14.238 31.75 31.75 31.75 17.512 0 31.75-14.238 31.75-31.75 0-17.512-14.238-31.75-31.75-31.75zm0 4c15.348 0 27.75 12.402 27.746 27.75 0 15.348-12.398 27.758-27.746 27.758s-27.754-12.406-27.758-27.758c0-15.348 12.406-27.75 27.758-27.75zm-15.398 24.551c-1.7617 0-3.1953 1.4297-3.1953 3.1953-0.003906 0.84766 0.33203 1.6641 0.92969 2.2656 0.60156 0.60547 1.418 0.94141 2.2656 0.94531 0.85547 0.003906 1.6719-0.33594 2.2773-0.9375 0.60547-0.60156 0.94141-1.4219 0.94141-2.2734-0.003907-0.85156-0.34375-1.668-0.94531-2.2656-0.60547-0.60156-1.4219-0.93359-2.2734-0.92969zm15.359 0h0.003906c-1.7656 0-3.1953 1.4297-3.1992 3.1953-0.003906 0.84766 0.33203 1.6641 0.93359 2.2656 0.59766 0.60547 1.4141 0.94141 2.2656 0.94531s1.6719-0.33594 2.2734-0.9375c0.60547-0.60156 0.94141-1.4219 0.94141-2.2734-0.003906-0.85156-0.34375-1.668-0.94531-2.2656-0.60547-0.60156-1.4219-0.93359-2.2695-0.92969zm15.359 0c-1.7617 0-3.1914 1.4297-3.1953 3.1953-0.003906 0.84766 0.33203 1.6641 0.93359 2.2656 0.59766 0.60156 1.4141 0.94141 2.2617 0.94531 0.85547 0.003906 1.6758-0.33203 2.2773-0.9375 0.60547-0.60156 0.94531-1.4219 0.94141-2.2734 0-0.85156-0.33984-1.668-0.94531-2.2656-0.60547-0.60156-1.4219-0.9375-2.2734-0.92969z"/>
                                </svg>
                            </button>
                            <textarea v-model="query" name="query" ref="textarea" @input="autoResizeTextarea" class="antialiased drop-shadow-md w-[55%] text-wrap h-auto relative py-3.5 px-5 font-normal block box-border bottom-0 overflow-hidden bg-slate-100 resize-none rounded-[2rem] outline-none placeholder:text-slate-600" placeholder="Type your message..."></textarea>
                            <button type="submit" class="drop-shadow-md">
                                <svg class="w-10 h-10 bg-slate-200 rounded-full drop-shadow-md fill-slate-600" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" x="0px" y="0px" style="enable-background:new 0 0 24 24;" xml:space="preserve" viewBox="2.04 2.04 19.92 19.92">
                                    <g>
                                        <path d="M12,21.959c5.501,0,9.959-4.459,9.959-9.959c0-5.5-4.459-9.959-9.959-9.959C6.5,2.041,2.041,6.5,2.041,12   C2.041,17.5,6.5,21.959,12,21.959z M12,3.286c4.805,0,8.714,3.909,8.714,8.714c0,4.805-3.909,8.714-8.714,8.714   c-4.805,0-8.714-3.909-8.714-8.714C3.286,7.195,7.195,3.286,12,3.286z"/><polygon points="11.378,10.317 11.378,17.001 12.623,17.001 12.623,10.313 15.112,12.801 15.992,11.921 12.003,7.932 8.009,11.926    8.889,12.807  "/>
                                    </g>
                                </svg>
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import AIMessage from '@/components/AIMessage.vue';
import HumanMessage from '@/components/HumanMessage.vue';

const {v4:uuidv4}=require('uuid')

export default {
    data(){
        return {
            messages: [],
            query: '',
            initialHeight: 0,
            socket: null // Add a socket property
        }
    },
    mounted() {
        this.initialHeight = this.$refs.textarea.scrollHeight;
        this.initWebSocket(); // Initialize WebSocket on mount
    },
    methods: {
        autoResizeTextarea() {
            const textarea = this.$refs.textarea;
            textarea.style.height = 'auto';
            const newHeight = textarea.scrollHeight;
            textarea.style.height = newHeight + 'px';
            textarea.style.bottom = newHeight - this.initialHeight + 'px';
        },
        initWebSocket() {
            this.socket = new WebSocket('ws://localhost:8000/ws');

            this.socket.onopen = () => {
                console.log('Socket connected');
            };
            this.socket.onmessage = (event) => {
                // When a message is received from the server
                let response = JSON.parse(event.data);
                // console.log('Received:', response);
                let last_message=this.messages[this.messages.length-1]
                if(last_message.role=='assistant'){
                    if(response.agent){
                        last_message.agent=`Calling ${response.agent}`
                        last_message.content='Loading...'
                    }else if (response.output){
                        last_message.agent=''
                        last_message.content=response.output
                    }
                }else{
                    this.messages.push({
                        'id': uuidv4(),
                        'role': 'assistant',
                        'content': response?.output? response.output: 'Loading...',
                        'agent': response?.agent? `Calling ${response?.agent}`: ''
                    });
                }
            };

            this.socket.onclose = () => {
                console.log('Socket closed');
                this.initWebSocket();
            };

            this.socket.onerror = (error) => {
                console.error('WebSocket error:', error);
            };
        },
        async submitHandler(e) {
            e.preventDefault();
            let query = this.query.trim();
            if (query) {
                this.messages.push({
                    'id': uuidv4(),
                    'role': 'user',
                    'content': query
                });
                this.query = '';
                this.sendQuery(query);
            }
        },
        sendQuery(query) {
            if (this.socket.readyState === WebSocket.OPEN) {
                this.socket.send(query);
            } else {
                console.log('Socket not connected');
                this.socket.send(query);
            }
        }
    },
    components: {
        AIMessage, HumanMessage
    }
}
</script>