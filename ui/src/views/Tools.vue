<template>
    <div class="w-full h-full p-4 relative">
        <div class="flex justify-between items-center">
            <div class="flex flex-row items-center">
                <img class="w-9 h-9" src="../assets/tool.svg"/>
                <h1 class="text-4xl m-2">Tools</h1>
            </div>
            <span @click="createToolHandler" class="cursor-pointer p-2 bg-slate-300 rounded-md text-lg hover:bg-slate-400">Add Tool</span>
        </div>
        <hr>
        <div v-if="getTools?.length>0" class="grid grid-cols-4 gap-4 mx-2 mt-5">
            <Tool v-for="tool in getTools" :key="tool.id" :tool="tool" :delete-tool="deleteToolHandler"/>
        </div>
        <div v-else class="mx-2 my-3">
            <span class="">No Tools Found.</span>
        </div>
        <div @click="createToolHandler" :style="{'display':isCreate?'block':'none'}" class="bg-slate-200/60 backdrop-blur-sm w-full h-full absolute top-0 left-0">
            <div @click.stop class="w-[80%] mx-auto bg-slate-300/60 drop-shadow-md  mt-[4%] rounded-md px-5 pt-3 pb-1">
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
                        <form @submit.prevent="createTool" class="flex flex-col gap-2">
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
        <div @click="deleteToolHandler" :style="{'display':isDelete?'block':'none'}" class="bg-slate-200/60 backdrop-blur-sm w-full h-full absolute top-0 left-0 block">
            <div @click.stop class="w-[50%] mx-auto bg-slate-300/70 drop-shadow-md mt-[10%] rounded-md p-4">
                <h1 class="text-3xl font-medium my-1">Delete {{ tool.name }}</h1>
                <p class="my-0.5">Are you sure you want to delete this tool? This action cannot be undone. Deleting the tool will remove it permanently from your system, and any dependencies or tasks associated with it may be affected.</p>
                <div class="flex justify-start gap-4 font-medium">
                    <button @click="deleteTool" class="bg-red-500 p-2 rounded-md shadow-md mt-2" type="button">Delete</button>
                    <button @click="deleteToolHandler" class="bg-slate-200 p-2 rounded-md shadow-md mt-2" type="button">Cancel</button>
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
import { mapGetters } from 'vuex';

export default {
    data(){
        return {
            tool:{
                id:null,
                name:'',
            },
            query:'',
            toolDefinition:'',
            isCreate:false,
            isDelete:false,
            extensions: [python(),ayuLight]
        }
    },
    computed:{
        ...mapGetters(['getTools'])
    },
    mounted(){
        this.$store.dispatch('getTools')
    },
    methods:{
        createToolHandler(){
            this.isCreate=!this.isCreate
        },
        deleteToolHandler(id,name){
            if(!this.isDelete){
                this.tool={
                    id,
                    name
                }
            }
            else{
                this.tool={
                    id:null,
                    name:''
                }
            }
            this.isDelete=!this.isDelete
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
        },
        async createTool(){ 
            if(this.toolDefinition.length>0){
                this.$store.dispatch('addTool',{
                    'tool_definition':this.toolDefinition
                })
                this.toolDefinition=''
                this.isCreate=false
            }
        },
        async deleteTool(){
            this.$store.dispatch('deleteTool',this.tool)
            this.tool={
                id:null,
                name:''
            }
            this.isDelete=false
        }

    },
    components: {
        Tool,Codemirror
    }
}
</script>