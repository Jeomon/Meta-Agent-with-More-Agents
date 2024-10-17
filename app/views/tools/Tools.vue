<template>
    <div class="w-full h-screen px-6 pt-10 flex flex-col gap-y-4">
        <div class="flex flex-row justify-between items-center">
            <h1 class="text-4xl font-medium">Tools</h1>
            <span @click="createTool" class="bg-slate-100 px-3 py-3 rounded-lg font-medium cursor-pointer">Add Tool</span>
        </div>
        <div class="grid grid-cols-4 gap-4 overflow-y-auto">
            <Tool @edit="editTool" @delete="deleteTool"/>
            <Tool @edit="editTool" @delete="deleteTool"/>
            <Tool @edit="editTool" @delete="deleteTool"/>
        </div>
    </div>
    <div @click="isCreate = !isCreate" :style="{ display: isCreate ? 'block' : 'none' }" class="absolute left-0 top-0 w-full h-full backdrop-blur-lg bg-opacity-50 bg-black">
        <div @click.stop class="w-[90%] h-fit bg-slate-200 mx-auto mt-[3%] rounded-md p-6">
            <h1 class="font-medium text-3xl">Create Tool</h1>
            <div class="grid grid-cols-6 gap-4 mt-4 mb-5">
                <div class="col-span-3 flex flex-col gap-2">
                    <div class="flex flex-col gap-2">
                        <label for="tool_name">Tool Name</label>
                        <input class="outline-none rounded-md h-8 p-2" type="text" name="tool_name"/>
                    </div>
                    <div class="flex flex-col gap-2">
                        <label for="tool_description">Tool Description</label>
                        <textarea rows="12" class="resize-none outline-none rounded-md p-2" type="text" name="tool_description"></textarea>
                    </div>
                </div>
                <div class="col-span-3">
                    <div class="flex flex-col gap-2">
                        <label for="tool_definition">Tool Definition</label>
                        <textarea v-model="toolDefinition" id="tool_definition" rows="15" class="outline-none rounded-md p-2.5 resize-none font-mono bg-slate-800 text-white" type="text" name="tool_definition"></textarea>
                    </div>
                </div>
            </div>
            <button type="submit" class="bg-slate-100 p-3 rounded-lg font-medium w-fit h-fit">Create Tool</button>
        </div>
    </div>
    <div @click="isEdit = !isEdit" :style="{ display: isEdit ? 'block' : 'none' }" class="absolute left-0 top-0 w-full h-full backdrop-blur-lg bg-opacity-50 bg-black">
        <div @click.stop class="w-[90%] h-fit bg-slate-200 mx-auto mt-[3%] rounded-md p-6">
            <h1 class="font-medium text-3xl">Edit Tool</h1>
            <div class="grid grid-cols-6 gap-4 mt-4 mb-5">
                <div class="col-span-3 flex flex-col gap-2">
                    <div class="flex flex-col gap-2">
                        <label for="tool_name">Tool Name</label>
                        <input class="outline-none rounded-md h-8 p-2" type="text" name="tool_name"/>
                    </div>
                    <div class="flex flex-col gap-2">
                        <label for="tool_description">Tool Description</label>
                        <textarea rows="12" class="resize-none outline-none rounded-md p-2.5 font-mono bg-slate-800 text-white" type="text" name="tool_description"></textarea>
                    </div>
                </div>
                <div class="col-span-3">
                    <div class="flex flex-col gap-2">
                        <label for="tool_definition">Tool Definition</label>
                        <textarea rows="15" class="outline-none rounded-md p-2 resize-none" type="text" name="tool_definition"></textarea>
                    </div>
                </div>
            </div>
            <button type="submit" class="bg-slate-100 p-3 rounded-lg font-medium w-fit h-fit">Edit Tool</button>
        </div>
    </div>
    <div @click="isDelete = !isDelete" :style="{ display: isDelete ? 'block' : 'none' }" class="absolute left-0 top-0 w-full h-full backdrop-blur-lg bg-opacity-50 bg-black">
        <div @click.stop class="w-[40%] h-fit  bg-slate-200 mx-auto mt-[8%] rounded-md p-5">
            <h1 class="font-medium text-3xl">Delete Tool</h1>
            <p class="my-3 text-pretty">Are you sure you want to delete this tool? This action cannot be undone, and the tool will be permanently removed from the system.</p>
            <div class=" flex flex-row gap-2 justify-center">
                <button type="submit" class="bg-red-500 p-3 rounded-lg font-medium w-fit h-fit">Delete Tool</button>
                <button type="button" @click="isDelete = !isDelete" class="bg-slate-100 p-3 rounded-lg font-medium w-fit h-fit">Cancel</button>
            </div>
        </div>
    </div>
</template>
<script>
import Tool from '@/components/Tool.vue';
export default {

    data(){
        return {
            isCreate: false,
            isEdit: false,
            isDelete: false,
            toolDefinition:''
        }
    },
    methods:{
        createTool(){
            this.isCreate = !this.isCreate
        },
        deleteTool(data){
            this.isDelete = !this.isDelete
            console.log(data);
        },
        editTool(data){
            this.isEdit = !this.isEdit
            console.log(data);
        }
    },
    components: {
        Tool
    }
}
</script>