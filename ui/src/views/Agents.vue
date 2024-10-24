<template>
    <div class="w-full h-full p-4 relative">
        <div class="flex justify-between items-center">
            <h1 class="text-4xl m-2">Agents</h1>
            <span @click="createAgentHandler" class="cursor-pointer p-2 bg-slate-300 rounded-md text-lg hover:bg-slate-400">Add Agent</span>
        </div>
        <hr>
        <div class="grid grid-cols-4 gap-4 mx-2 my-3">
            <Agent/>
            <Agent/>
            <Agent/>
            <Agent/>
        </div>
        <div @click="createAgentHandler" :style="{'display':isCreate?'block':'none'}" class="bg-slate-200/60 backdrop-blur-sm w-full h-full absolute top-0 left-0">
            <div @click.stop class="w-[60%] mx-auto bg-slate-300/60 backdrop-blur-md drop-shadow-md  mt-[5%] rounded-md px-5 pt-3 pb-1">
                <h1 class="text-4xl font-medium">Create Agent</h1>
                <hr class="w-[40%]">
                <form @submit.prevent="" class="my-4 flex flex-col gap-3">
                    <div class="flex flex-col gap-1">
                        <label role="name" for="name">Name: </label>
                        <input class="shadow-sm rounded-md px-1 h-10 outline-none" type="text" id="name" placeholder="Enter the agent name"/>
                    </div>
                    <div class="flex flex-col gap-1">
                        <label role="description" for="name">Description: </label>
                        <textarea rows="10" class="shadow-sm rounded-md p-1 resize-none outline-none" id="description" placeholder="Enter the agent description"></textarea>
                    </div>
                    <div class="flex flex-col gap-1">
                        <label role="tools" for="tools">Pick Tools</label>
                        <select class="shadow-sm w-[30%] rounded-md p-1">
                            <option selected disabled>Select the Tool</option>
                            <option>Weather Tool</option>
                            <option>Stock Tool</option>
                        </select>
                    </div>
                    <div>
                        <button class="bg-slate-200 p-2 rounded-md shadow-md" type="submit">Create Agent</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>
<script>
import Agent from '@/components/card/Agent.vue';
export default {
    data(){
        return {
            isCreate:false
        }
    },
    methods:{
        createAgentHandler(){
            this.isCreate=!this.isCreate
        }
    },
    components:{
        Agent
    }
}
</script>