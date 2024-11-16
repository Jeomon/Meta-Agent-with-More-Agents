<template>
    <div class="p-1 flex justify-start items-center gap-1.5 font-medium cursor-pointer">
        <img class="w-4 h-6" src="../../assets/create.svg"/>
        <p class="text-base">New Conversation</p>
    </div>
    <hr>
    <div class="flex flex-col my-2 gap-y-1 text-base">
        <Conversation/>
        <Conversation/>
        <Conversation/>
    </div>
</template>
<script>
import Conversation from '../card/Conversation.vue';

export default {
    data(){
        return {
        }
    },
    components: {
        Conversation
    }
}
</script>