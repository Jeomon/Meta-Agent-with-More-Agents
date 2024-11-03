<template>
    <h1 class="text-3xl my-1">History</h1>
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