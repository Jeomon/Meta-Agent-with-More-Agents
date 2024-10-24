<template>
    <div class="w-[85%] h-[89%] mx-auto py-5 px-10 overflow-y-auto scroll-smooth" ref="messageContainer">
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