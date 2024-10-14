<template>
    <div class="w-full h-screen px-6 pt-10 flex flex-col gap-y-4">
        <div class="flex flex-row justify-between items-center">
            <h1 class="text-4xl font-medium">Tools</h1>
            <span @click="createTool" class="bg-slate-100 px-3 py-3 rounded-lg font-medium cursor-pointer">Add Tool</span>
        </div>
        <div class="grid grid-cols-4 gap-4 overflow-y-auto">
            <Tool/>
            <Tool/>
        </div>
    </div>
    <div :style="{ display: isclicked ? 'block' : 'none' }" class="hidden absolute left-0 top-0 w-full h-full backdrop-blur-md backdrop-brightness-50">
        <div class="w-[90%] h-[90%] bg-slate-200 mx-auto mt-[3%] rounded-md p-6">
            <h1 class="font-medium text-3xl">Create Tool</h1>
            <div class="grid grid-cols-6 grid-rows-6 my-4 gap-x-5 gap-y-2 h-full">
                <div class="col-span-3 row-span-5 flex flex-col gap-2">
                    <div class="flex flex-col gap-2">
                        <label for="tool_name">Tool Name</label>
                        <input class="outline-none rounded-md h-8 p-2" type="text" name="tool_name"/>
                    </div>
                    <div class="flex flex-col gap-2">
                        <label for="tool_description">Tool Description</label>
                        <textarea rows="15" class="resize-none outline-none rounded-md p-2" type="text" name="tool_description"/>
                    </div>
                </div>
                <div class="col-span-3 row-span-5 h-full flex flex-col gap-2">
                    <label for="tool_name">Tool Definition</label>
                    <textarea rows="18" class="outline-none rounded-md p-2 resize-none" type="text" name="tool_definition"/>
                </div>
                <button type="submit" class="col-span-full row-span-1 bg-slate-100 p-3 rounded-lg font-medium w-fit h-fit">Create Tool</button>
            </div>
        </div>
    </div>
</template>
<script>
import Tool from '@/components/Tool.vue';

export default {

    data(){
        return {
            isclicked: false
        }
    },
    methods:{
        createTool(){
            this.isclicked = !this.isclicked
        }
    },
    components: {
        Tool
    }
}
</script>