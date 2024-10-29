<template>
    <div class="w-full h-full p-4 relative">
        <div class="flex justify-between items-center">
            <h1 class="text-4xl m-2">Tools</h1>
            <span @click="createToolHandler" class="cursor-pointer p-2 bg-slate-300 rounded-md text-lg hover:bg-slate-400">Add Tool</span>
        </div>
        <hr>
        <div class="grid grid-cols-4 gap-4 mx-2 my-3">
        </div>
        <div @click="createToolHandler" :style="{'display':isCreate?'block':'none'}" class="bg-slate-200/60 backdrop-blur-sm w-full h-full absolute top-0 left-0">
            <div @click.stop class="w-[80%] mx-auto bg-slate-300/60 backdrop-blur-md drop-shadow-md  mt-[4%] rounded-md px-5 pt-3 pb-1">
                <h1 class="text-4xl font-medium">Create Tool</h1>
                <hr class="w-[40%]">
                <div class="my-4 flex flex-col gap-x-2 gap-y-1">
                    <div class="col-span-3 flex flex-col gap-3">
                        <div class="flex flex-col gap-1">
                            <form @submit.prevent="generateTool" class="flex flex-row gap-2 w-full">
                                <input v-model="query" class="shadow-sm rounded-md px-1.5 h-10 outline-none w-[85%]" type="text" id="name" placeholder="Ask Tool Agent to generate..."/>
                                <button class="bg-slate-200 p-2 rounded-md shadow-md w-[15%]" type="submit">Generate Tool</button>
                            </form>
                        </div>
                        <form @submit.prevent="" class="flex flex-col gap-2">
                            <div class="flex flex-col gap-1">
                                <label role="tool definition" for="tool definition">Tool Definition: </label>
                                <Codemirror :style="{ height: '55vh', overflow: 'auto',borderRadius: '10px',outline: 'none'}" class="p-2 resize-none outline-none bg-slate-700 text-white" :extensions="extensions" :indent-with-tab="true" :tab-size="2" v-model="toolDefinition" rows="14" id="editor" placeholder="Enter the Tool Definition"/>
                            </div>
                            <div>
                                <button class="bg-slate-200 p-2 rounded-md shadow-md mt-2" type="submit">Create Tool</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import Tool from '@/components/card/Tool.vue';
import { Codemirror } from 'vue-codemirror';
import { python } from '@codemirror/lang-python';
import {ayuLight} from 'thememirror';

import axios from 'axios';

export default {
    data(){
        return {
            query:'',
            toolDefinition:'',
            isCreate:false,
            extensions: [python(),ayuLight]
        }
    },
    mounted(){

    },
    methods:{
        createToolHandler(){
            this.isCreate=!this.isCreate
        },
        async generateTool(){
            if(this.query.length>0){
                let response=await axios.post('tool/generate',{
                    'query':this.query
                })
                let data= response.data
                this.toolDefinition=data.tool_definition
            }
            this.query=''
        }
    },
    components: {
        Tool,Codemirror
    }
}
</script>