<template>
    <div class="w-full h-full p-4">
        <div class="flex justify-between items-center">
            <h1 class="text-4xl m-2">Agents</h1>
            <span class="">Add Agent</span>
        </div>
        <hr>
        <div class="grid grid-cols-3 gap-3 mx-2 my-3">
            <Agent/>
            <Agent/>
            <Agent/>
            <Agent/>
        </div>
    </div>
</template>
<script>
import Agent from '@/components/card/Agent.vue';
export default {
    components:{
        Agent
    }
}
</script>