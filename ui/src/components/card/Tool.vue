<template>
    <div class="flex flex-row bg-slate-200 p-2.5 rounded-lg gap-2 drop-shadow">
        <img class="w-8 h-8" src="../../assets/Tool.svg"/>
        <div class="flex flex-col gap-1">
            <h1 class="text-2xl">Weather Tool</h1>
            <p class="max-h-12 text-pretty overflow-hidden">This agent is responsible for finding weather data of a given location.</p>
        </div>
        <img @click="toggleHandler" class="w-4 h-4 cursor-pointer relative" src="../../assets/3-dot.svg"/>
        <div :style="{'display':toggleMenu?'flex':'none'}" class="absolute flex-col top-8 -right-0 bg-slate-100 rounded-lg overflow-hidden drop-shadow-md">
            <span class="hover:bg-slate-300 px-2 py-0.5 cursor-pointer">Modify</span>
            <span class="hover:bg-slate-300 px-2 py-0.5 cursor-pointer">Delete</span>
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
    methods:{
        toggleHandler(){
            this.toggleMenu=!this.toggleMenu
        }
    }
}
</script>