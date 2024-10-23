<template>
    <div class="w-full h-full p-4">
        <h1 class="text-4xl m-2">Tools</h1>
        <hr>
        <div class="grid grid-cols-4 gap-3 mx-2 my-3">
            <Tool/>
            <Tool/>
            <Tool/>
            <Tool/>
        </div>
    </div>
</template>
<script>
import Tool from '@/components/card/Tool.vue';

export default {
    components: {
        Tool
    }
}
</script>