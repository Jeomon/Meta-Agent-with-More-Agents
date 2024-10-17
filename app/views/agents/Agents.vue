<template>
    <div class="w-full h-screen px-6 pt-10 flex flex-col gap-y-4">
        <div class="flex flex-row justify-between items-center">
            <h1 class="text-4xl font-medium">Agents</h1>
            <span @click="createAgent" class="bg-slate-100 px-3 py-3 rounded-lg font-medium cursor-pointer">Add Agent</span>
        </div>
        <div class="grid grid-cols-3 gap-4 overflow-y-auto">
            <Agent @edit="editAgent" @delete="deleteAgent"/>
            <Agent @edit="editAgent" @delete="deleteAgent"/>
            <Agent @edit="editAgent" @delete="deleteAgent"/>
        </div>
    </div>
    <div @click="isCreate = !isCreate" :style="{ display: isCreate ? 'block' : 'none' }" class="absolute left-0 top-0 w-full h-full backdrop-blur-lg bg-opacity-50 bg-black">
        <div @click.stop class="w-[90%] h-fit bg-slate-200 mx-auto mt-[3%] rounded-md p-6">
            <h1 class="font-medium text-3xl">Create Agent</h1>
            <div class="flex flex-col gap-4 my-4">
                <div class="flex flex-col gap-2">
                    <label for="tool_name">Agent Name</label>
                    <input class="outline-none rounded-md h-8 p-2 w-[30%]" type="text" name="tool_name"/>
                </div>
                <div class="flex flex-col gap-2">
                    <label for="tool_description">Agent Description</label>
                    <textarea rows="10" class="resize-none outline-none rounded-md p-2" type="text" name="tool_description"/>
                </div>
                <div class="flex flex-col gap-2 w-fit">
                    <label for="tool_description">Tool</label>
                    <select class="p-1.5 rounded-md">
                        <option selected disabled>Select Tool</option>
                        <option>No Tool</option>
                        <option>Weather Tool</option>
                        <option>Stock Tool</option>
                    </select>
                </div>
                <button type="submit" class="bg-slate-100 p-3 rounded-lg font-medium w-fit h-fit">Create Tool</button>
            </div>
        </div>
    </div>
    <div @click="isEdit = !isEdit" :style="{ display: isEdit ? 'block' : 'none' }" class="absolute left-0 top-0 w-full h-full backdrop-blur-lg bg-opacity-50 bg-black">
        <div @click.stop class="w-[90%] h-fit bg-slate-200 mx-auto mt-[3%] rounded-md p-5">
            <h1 class="font-medium text-3xl">Edit Agent</h1>
            <div class="flex flex-col gap-4 my-4">
                <div class="flex flex-col gap-2">
                    <label for="tool_name">Agent Name</label>
                    <input class="outline-none rounded-md h-8 p-2 w-[30%]" type="text" name="tool_name"/>
                </div>
                <div class="flex flex-col gap-2">
                    <label for="tool_description">Agent Description</label>
                    <textarea rows="10" class="resize-none outline-none rounded-md p-2" type="text" name="tool_description"></textarea>
                </div>
                <div class="flex flex-col gap-2 w-fit">
                    <label for="tool_description">Tool</label>
                    <select class="p-1.5 rounded-md">
                        <option selected disabled>Select Tool</option>
                        <option>No Tool</option>
                        <option>Weather Tool</option>
                        <option>Stock Tool</option>
                    </select>
                </div>
                <button type="submit" class="bg-slate-100 p-3 rounded-lg font-medium w-fit h-fit">Create Tool</button>
            </div>
        </div>
    </div>
    <div @click="isDelete = !isDelete" :style="{ display: isDelete ? 'block' : 'none' }" class="absolute left-0 top-0 w-full h-full backdrop-blur-lg bg-opacity-50 bg-black">
        <div @click.stop class="w-[40%] h-fit  bg-slate-200 mx-auto mt-[8%] rounded-md p-5">
            <h1 class="font-medium text-3xl">Delete Agent</h1>
            <p class="my-3 text-pretty">Are you sure you want to delete this agent? This action cannot be undone, and the agent will be permanently removed along with any associated data.</p>
            <div class=" flex flex-row gap-2 justify-center">
                <button type="submit" class="bg-red-500 p-3 rounded-lg font-medium w-fit h-fit">Delete Tool</button>
                <button type="button" @click="isDelete = !isDelete" class="bg-slate-100 p-3 rounded-lg font-medium w-fit h-fit">Cancel</button>
            </div>
        </div>
    </div>
</template>
<script>
import Agent from '@/components/Agent.vue';

export default {

    data(){
        return {
            isCreate: false,
            isEdit: false,
            isDelete: false
        }
    },
    methods:{
        createAgent(){
            this.isCreate = !this.isCreate
        },
        deleteAgent(data){
            this.isDelete = !this.isDelete
            console.log(data);
        },
        editAgent(data){
            this.isEdit = !this.isEdit
            console.log(data);
        }
    },
    components: {
        Agent
    }
}
</script>