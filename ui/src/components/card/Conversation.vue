<template>
    <div :class="['flex','flex-row','items-center',isEdit?'justify-around px-0.5':'justify-between px-1','gap-1.5','hover:bg-slate-200',{'bg-slate-200':isEdit||isOptions},'py-1.5','rounded-lg','cursor-pointer']">
        <p v-if="!isEdit" class="truncate text-ellipsis overflow-hidden">{{ conversation.title }}</p>
        <input v-model="title" v-else type="text" class="rounded-md outline-none p-0.5">
        <div v-if="!isEdit" class="relative">
            <button @click.stop="showOptions">
                <img class="w-4 h-4" src="../../assets/3-dot.svg"/>
            </button>
            <div :style="{'display':isOptions?'flex':'none'}" class="absolute top-5 -right-0 flex-col bg-slate-100 rounded-lg overflow-hidden drop-shadow-md z-10">
                <span class="hover:bg-slate-200 px-2 py-0.5 cursor-pointer">Share</span>
                <span @click.stop="()=>{isEdit=!isEdit;isOptions=false}" class="hover:bg-slate-200 px-2 py-0.5 cursor-pointer">Rename</span>
                <span @click.stop="()=>deleteConversation(conversation)" class="hover:bg-slate-200 px-2 py-0.5 cursor-pointer">Delete</span>
                <span class="hover:bg-slate-200 px-2 py-0.5 cursor-pointer">Archive</span>
            </div>
        </div>
        <div class="flex flex-row gap-1.5 items-center" v-else>
            <img @click="()=>editConversation(conversation)" class="w-4 h-4 cursor-pointer" src="../../assets/tick.svg"/>
            <img @click.stop="()=>{isEdit=false}" class="w-3 h-3 cursor-pointer" src="../../assets/cross.svg"/>
        </div>
    </div>
</template>
<script>
export default {
    data(){
        return{
            title:'',
            isOptions:false,
            isEdit:false
        }
    },
    props:{
        conversation:Object
    },
    methods:{
        showOptions(){
            this.isOptions=!this.isOptions
        },
        editConversation(conversation){
            if(this.title){
                this.$store.dispatch('editConversation',{'id':conversation.id,'title':this.title})
                this.isEdit=false
            }
        },
        deleteConversation(conversation){
            this.$store.dispatch('deleteConversation',conversation.id)
        }
    }
}
</script>