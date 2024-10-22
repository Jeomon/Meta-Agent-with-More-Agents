<template>
    <div class="w-[85%] h-full mx-auto py-5 px-10 overflow-y-scroll scroll-smooth">
        <HumanMessage/>
        <AIMessage/>
        <HumanMessage/>
        <AIMessage/>
        <HumanMessage/>
        <AIMessage/>
        <HumanMessage/>
        <AIMessage/>
        <HumanMessage/>
        <AIMessage/>
        <HumanMessage/>
        <AIMessage/>
    </div>
</template>
<script>
import AIMessage from '../message/AIMessage.vue';
import HumanMessage from '../message/HumanMessage.vue';

export default {
    data(){
        return {
            
        }
    },
    components:{
        HumanMessage,AIMessage
    }
}
</script>