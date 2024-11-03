<template>
    <div class="flex flex-row items-center gap-x-1 hover:bg-slate-200 focus:bg-slate-300 p-1 rounded-lg cursor-pointer">
        <p class="truncate text-ellipsis overflow-hidden">Quantum Physics and Relativity</p>
        <div class="relative">
            <button @click="showOptions">
                <img class="w-4 h-4" src="../../assets/3-dot.svg"/>
            </button>
            <div :style="{'display':isoptions?'flex':'none'}" class="absolute top-8 -right-0 flex-col bg-slate-100 rounded-lg overflow-hidden drop-shadow-md z-10">
                <span class="hover:bg-slate-200 px-2 py-0.5 cursor-pointer">Share</span>
                <span class="hover:bg-slate-200 px-2 py-0.5 cursor-pointer">Rename</span>
                <span class="hover:bg-slate-200 px-2 py-0.5 cursor-pointer">Delete</span>
                <span class="hover:bg-slate-200 px-2 py-0.5 cursor-pointer">Archive</span>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    data(){
        return{
            isoptions:false
        }
    },
    methods:{
        showOptions(){
            this.isoptions=!this.isoptions
        }
    }
}
</script>