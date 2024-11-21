<template>
    <div @click="createConversationHandler" class="p-1 flex justify-start items-center gap-1.5 font-medium cursor-pointer">
        <img class="w-4 h-6" src="../../assets/create.svg"/>
        <p class="text-base">New Conversation</p>
    </div>
    <hr>
    <div v-if="getConversations.length>0" class="flex flex-col my-2 gap-y-1 text-base">
        <Conversation @click="()=>getConversation(conversation.id)" v-for="conversation in getConversations" :key="conversation.id" :conversation="conversation"/>
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
        }
    },
    computed:{
        ...mapGetters(['getConversations'])
    },
    mounted(){
        this.$store.dispatch('getConversations')
    },
    methods:{
        createConversationHandler(){
            this.$store.dispatch('addConversation','Untitled Conversation')
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