<template>
    <div class="w-[85%] h-[89%] mx-auto py-5 px-10 overflow-y-auto scroll-smooth" ref="messageContainer">
        <div v-if="!getMessages||getMessages.length==0" class="flex flex-col items-center mt-[38vh]">
            <h1 class="text-4xl font-normal">Hi, How can I help you?</h1>
        </div>
        <div v-else>
            <component v-for="message in getMessages" :key="message.id" :is="message.role=='user'?'HumanMessage':'AIMessage'" :content="message.content"/>
        </div>
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
    mounted() {
        // Scroll to bottom initially when the component is mounted
        this.scrollToBottom();
    },
    computed:{
        ...mapGetters(['getMessages'])
    },
    watch: {
        // Watch the getMessages array for changes
        getMessages() {
            this.scrollToBottom();
        }
    },
    methods: {
        scrollToBottom() {
            // Ensure DOM is updated before scrolling
            this.$nextTick(() => {
                const container = this.$refs.messageContainer;
                container.scrollTop = container.scrollHeight;
            });
        }
    },
    components:{
        HumanMessage,AIMessage
    }
}
</script>