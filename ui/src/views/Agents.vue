<template>
    <div class="w-full h-full p-4 relative">
        <div class="flex justify-between items-center">
            <h1 class="text-4xl m-2">Agents</h1>
            <span @click="createAgentHandler" class="cursor-pointer p-2 bg-slate-300 rounded-md text-lg hover:bg-slate-400">Add Agent</span>
        </div>
        <hr>
        <div v-if="getAgents?.length>0" class="grid grid-cols-4 gap-4 mx-2 my-3">
            <Agent v-for="agent in getAgents" :key="agent.id" :agent="agent" :delete-agent="deleteAgentHandler"/>
        </div>
        <div v-else class="mx-2 my-3">
            <span class="">No Agents Found.</span>
        </div>
        <div @click="createAgentHandler" :style="{'display':isCreate?'block':'none'}" class="bg-slate-200/60 backdrop-blur-sm w-full h-full absolute top-0 left-0">
            <div @click.stop class="w-[60%] mx-auto bg-slate-300/60 backdrop-blur-md drop-shadow-md  mt-[5%] rounded-md px-5 pt-3 pb-1">
                <h1 class="text-4xl font-medium">Create Agent</h1>
                <hr class="w-[40%]">
                <form @submit.prevent="createAgent" class="my-4 flex flex-col gap-3">
                    <div class="flex flex-col gap-1">
                        <label role="name" for="name">Name: </label>
                        <input v-model="agent.name" class="shadow-sm rounded-md px-1 h-10 outline-none" type="text" id="name" placeholder="Enter the agent name"/>
                    </div>
                    <div class="flex flex-col gap-1">
                        <label role="description" for="description">Description: </label>
                        <textarea v-model="agent.description" rows="10" class="shadow-sm rounded-md p-1 resize-none outline-none" id="description" placeholder="Enter the agent description"></textarea>
                    </div>
                    <div class="flex flex-col gap-1">
                        <label role="tools" for="tools">Pick Tools</label>
                        <select v-model="agent.tools" class="shadow-sm w-[30%] rounded-md p-1">
                            <option selected disabled>Select the Tool</option>
                            <option v-for="tool in getTools" :key="tool.id" :value="tool.name">{{tool.name}}</option>
                            <option value="No Tool">No Tool</option>
                        </select>
                    </div>
                    <div>
                        <button class="bg-slate-200 p-2 rounded-md shadow-md" type="submit">Create Agent</button>
                    </div>
                </form>
            </div>
        </div>
        <div @click="deleteAgentHandler" :style="{'display':isDelete?'block':'none'}" class="bg-slate-200/60 backdrop-blur-sm w-full h-full absolute top-0 left-0 block">
            <div @click.stop class="w-[50%] mx-auto bg-slate-300/70 drop-shadow-md mt-[10%] rounded-md p-4">
                <h1 class="text-3xl font-medium my-1">Delete {{ agent.name }}</h1>
                <p class="my-0.5">Are you sure you want to delete this agent? This action cannot be undone. Deleting the agent will permanently remove it from your system, and any tasks or operations assigned to this agent may be affected.</p>
                <div class="flex justify-start gap-4 font-medium">
                    <button @click="deleteAgent" class="bg-red-500 p-2 rounded-md shadow-md mt-2" type="button">Delete</button>
                    <button @click="deleteAgentHandler" class="bg-slate-200 p-2 rounded-md shadow-md mt-2" type="button">Cancel</button>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import Agent from '@/components/card/Agent.vue';
import { mapGetters } from 'vuex';

export default {
    data(){
        return {
            isCreate:false,
            isDelete:false,
            agent:{
                id:null,
                name:'',
                description:'',
                tools:'Select the Tool'
            },
        }
    },
    computed:{
        ...mapGetters(['getAgents','getTools'])
    },
    mounted(){
        this.$store.dispatch('getAgents')
        this.$store.dispatch('getTools')
    },
    methods:{
        createAgentHandler(){
            this.isCreate=!this.isCreate
        },
        deleteAgentHandler(agent){
            if(!this.isDelete){
                this.agent=agent
            }
            else{
                this.agent={
                    id:null,
                    name:'',
                    description:'',
                    tools:'Select the Tool'
                }
            }
            this.isDelete=!this.isDelete
        },
        createAgent(e){
            if(this.agent){
                this.$store.dispatch('addAgent',{...this.agent})
                this.isCreate=false
                this.agent={
                    id:null,
                    name:'',
                    description:'',
                    tools:'Select the Tool'
                }
            }
        },
        deleteAgent(){
            this.$store.dispatch('deleteAgent',this.agent)
            this.agent={
                id:null,
                name:'',
                description:'',
                tools:'Select the Tool'
            }
            this.isDelete=false
        }
    },
    components:{
        Agent
    }
}
</script>