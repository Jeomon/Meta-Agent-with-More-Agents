<template>
    <div class="w-[85%] h-full mx-auto py-5 px-10 overflow-y-auto scroll-smooth">
        <component v-for="message in getMessages" :key="message.id" :is="message.role=='user'?'HumanMessage':'AIMessage'" :content="message.content"/>
    </div>
</template>
<script>
import { mapGetters } from 'vuex';
import AIMessage from '../message/AIMessage.vue';
import HumanMessage from '../message/HumanMessage.vue';

export default {
    data(){
        return {
            
        }
    },
    computed:{
        ...mapGetters(['getMessages'])
    },
    components:{
        HumanMessage,AIMessage
    }
}
</script>