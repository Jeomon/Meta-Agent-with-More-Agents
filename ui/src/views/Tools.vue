<template>
    <div class="w-full h-full p-4 relative">
        <div class="flex justify-between items-center">
            <h1 class="text-4xl m-2">Tools</h1>
            <span @click="createToolHandler" class="cursor-pointer p-2 bg-slate-300 rounded-md text-lg hover:bg-slate-400">Add Tool</span>
        </div>
        <hr>
        <div class="grid grid-cols-4 gap-4 mx-2 my-3">
            <Tool/>
            <Tool/>
            <Tool/>
            <Tool/>
        </div>
        <div @click="createToolHandler" :style="{'display':isCreate?'block':'none'}" class="bg-slate-200/60 backdrop-blur-sm w-full h-full absolute top-0 left-0">
            <div @click.stop class="w-[70%] mx-auto bg-slate-300/60 backdrop-blur-md drop-shadow-md  mt-[4%] rounded-md px-5 pt-3 pb-1">
                <h1 class="text-4xl font-medium">Create Tool</h1>
                <hr class="w-[40%]">
                <div class="my-4 flex flex-col gap-x-2 gap-y-1">
                    <form @submit.prevent="" class="col-span-3 flex flex-col gap-3">
                        <div class="flex flex-col gap-1">
                            <label role="name" for="name">Query Tool Agent: </label>
                            <form @submit.prevent.stop="" class="flex flex-row gap-2">
                                <input class="shadow-sm rounded-md px-1.5 h-10 outline-none w-[85%]" type="text" id="name" placeholder="Enter the purpose of the tool"/>
                                <button class="bg-slate-200 p-2 rounded-md shadow-md" type="submit">Generate Tool</button>
                            </form>
                        </div>
                        <div class="flex flex-col gap-1">
                            <label role="tool definition" for="tool definition">Tool Definition: </label>
                            <textarea rows="14" class="shadow-sm rounded-md p-2 resize-none outline-none bg-slate-700 text-white" id="description" placeholder="Enter the Tool Definition"></textarea>
                        </div>
                        <div>
                            <button class="bg-slate-200 p-2 rounded-md shadow-md" type="submit">Create Tool</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import Tool from '@/components/card/Tool.vue';

export default {
    data(){
        return {
            isCreate:false
        }
    },
    methods:{
        createToolHandler(){
            this.isCreate=!this.isCreate
        }
    },
    components:{
        Tool
    }
}
</script>