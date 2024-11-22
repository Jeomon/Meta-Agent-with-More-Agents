<template>
    <div class="flex flex-row bg-slate-200 p-2.5 rounded-lg gap-2 drop-shadow relative">
        <img class="w-8 h-8" src="../../assets/agent.svg"/>
        <div class="flex flex-col gap-0.5">
            <h1 class="text-xl font-medium">{{ agent.name }}</h1>
            <p class="max-h-12 text-pretty overflow-hidden text-ellipsis">{{ agent.description }}</p>
            <p>Tools: {{ tools }}</p>
        </div>
        <img @click="toggleHandler" class="w-4 h-4 cursor-pointer absolute right-1" src="../../assets/3-dot.svg"/>
        <div :style="{'display':toggleMenu?'flex':'none'}" class="absolute flex-col top-8 -right-0 bg-slate-100 rounded-lg overflow-hidden drop-shadow-md">
            <span class="hover:bg-slate-300 px-2 py-0.5 cursor-pointer">Modify</span>
            <span @click="()=>{deleteAgent(agent);toggleMenu=false}" class="hover:bg-slate-300 px-2 py-0.5 cursor-pointer">Delete</span>
        </div>
    </div>
</template>
<script>
export default {
    data(){
        return {
            toggleMenu:false
        }
    },
    computed:{
        tools(){
            return this.agent.tools?.join(', ')
        }
    },
    props:{
        agent: {
            type: Object, 
            required: true
        },
        deleteAgent: {
            type: Function, 
            required: true
        }
    },
    methods:{
        toggleHandler(){
            this.toggleMenu=!this.toggleMenu
        }
    }
}
</script>