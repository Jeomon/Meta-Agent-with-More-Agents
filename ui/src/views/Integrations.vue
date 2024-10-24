<template>
    <div class="w-full h-full p-4 relative">
        <div class="flex justify-between items-center">
            <h1 class="text-4xl m-2">Integrations</h1>
            <span @click="addAPIKeyHandler" class="cursor-pointer p-2 bg-slate-300 rounded-md text-lg hover:bg-slate-400">Add API Key</span>
        </div>
        <hr>
        <div @click="addAPIKeyHandler" :style="{'display':isCreate?'block':'none'}" class="bg-slate-200/60 backdrop-blur-sm w-full h-full absolute top-0 left-0">
            <div @click.stop class="w-[40%] mx-auto bg-slate-300/60 backdrop-blur-md drop-shadow-md  mt-[12%] rounded-md px-5 pt-3 pb-1">
                <h1 class="text-3xl font-medium">Add API Key</h1>
                <hr class="w-[50%]">
                <form @submit.prevent="" class="my-4 flex flex-col gap-3">
                    <div class="flex flex-col gap-1">
                        <label role="name" for="name">API Name: </label>
                        <input class="shadow-sm rounded-md px-1.5 h-10 outline-none" type="text" id="name" placeholder="Enter the API name"/>
                    </div>
                    <div class="flex flex-col gap-1">
                        <label role="key" for="name">API Key: </label>
                        <input class="shadow-sm rounded-md px-1.5 h-10 outline-none" type="text" id="key" placeholder="Enter the API key"/>
                    </div>
                    <div>
                        <button class="bg-slate-200 p-2 rounded-md shadow-md" type="submit">Add API Key</button>
                    </div>
                </form>
            </div>
        </div>
        <div class="w-full h-[93%] px-2 py-5 overflow-y-auto">
            
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
        addAPIKeyHandler(){
            this.isCreate=!this.isCreate
        }
    },
    components:{
        Agent
    }
}
</script>