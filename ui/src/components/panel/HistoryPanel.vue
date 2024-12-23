<template>
    <div @click="createConversationHandler" class="p-1 flex justify-start items-center gap-1.5 font-medium cursor-pointer">
        <img class="w-4 h-6" src="../../assets/create.svg"/>
        <p class="text-base">New Conversation</p>
    </div>
    <hr>
    <div v-if="getConversations.length>0" class="flex flex-col my-2 gap-y-1 text-base">
        <Conversation :class="{'hidden':conversation.length==0}" @click="()=>getConversation(conversation.id)" v-for="conversation in getConversations" :key="conversation.id" :conversation="conversation"/>
    </div>
    <div v-else class="flex flex-row items-center justify-center h-[75%]">
        <span class="text-lg italic">No conversations found...</span>
    </div>
</template>
<script>
import { mapGetters } from 'vuex';
import Conversation from '../card/Conversation.vue';

export default {
    data(){
        return {
            newConversation:null
        }
    },
    computed:{
        ...mapGetters(['getConversations','getMessages'])
    },
    async mounted(){
        let conversations =await this.$store.dispatch('getConversations')
        console.log(conversations);
        this.newConversation=conversations.find(conversation => conversation.length==0)
    },
    methods:{
        async createConversationHandler(){
            if(this.getConversations.every(conversation => conversation.length > 0)){
                this.newConversation=await this.$store.dispatch('addConversation','Untitled Conversation')
            }
            else{                  
                let id=this.newConversation.id
                let title=this.newConversation.title
                this.$store.commit('getConversation',{id,title})
            }
            this.$store.commit('getMessages',[])
        },
        getConversation(conversation_id){
            this.$store.dispatch('getConversation',conversation_id)
        }
    },
    components: {
        Conversation
    }
}
</script>