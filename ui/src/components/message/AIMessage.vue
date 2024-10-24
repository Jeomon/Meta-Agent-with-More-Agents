<template>
    <div class="flex flex-col justify-start gap-1 my-3 max-w-[60%]">
        <p class="text-lg/2" v-if="getCurrentAgent">Calling {{getCurrentAgent}}</p>
        <div class="flex flex-row gap-x-2 bg-slate-100/80 w-fit p-3 rounded-2xl items-center relative shadow-md">
            <img class="w-10 h-10 rounded-full self-start" src="../../assets/ollama.png"/>
            <p class="text-base leading-snug text-wrap" v-if="getOutput">{{getOutput}}</p>
            <p class="text-base leading-snug" v-else>Waiting for response</p>
            <div class="flex flex-row gap-x-2 justify-center absolute -bottom-6 -right-1">
                <img class="w-4 h-4" src="../../assets/like.svg"/>
                <img class="w-4 h-4" src="../../assets/dislike.svg"/>
                <img class="w-4 h-4" src="../../assets/refresh.svg"/>
                <img class="w-4 h-4" src="../../assets/3-dot.svg"/>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    props:{
        content: Object,
    },
    computed:{
        getCurrentAgent(){
            return this.content.current_agent||''
        },
        getOutput(){
            return this.content.output||''
        }
    }
}
</script>