<template>
    <div class="w-full h-full p-4 relative">
        <div class="flex justify-between items-center">
            <h1 class="text-4xl m-2">Integrations</h1>
            <span @click="addIntegrationHandler" class="cursor-pointer p-2 bg-slate-300 rounded-md text-lg hover:bg-slate-400">Add Integration</span>
        </div>
        <hr>
        <table class="w-[50%] rounded-lg mt-5  table-fixed">
            <thead>
                <tr class="border-b bg-white">
                    <th class="text-left py-3 px-2 font-medium">Name</th>
                    <th class="text-left py-3 px-2 font-medium">API Key</th>
                    <th class="text-left py-3 px-2 font-medium">Action</th>
                </tr>
            </thead>
            <tbody v-if="getIntegrations?.length > 0">
                <tr v-for="integration in getIntegrations" :key="integration.id" class="border-b bg-slate-50">
                    <td class="py-3 px-2">{{ integration.name }}</td>
                    <td class="py-3 px-2 font-mono flex justify-between">
                        <span>{{ maskKey(integration.key) }}</span>
                    </td>
                    <td>
                        <span class="mx-1 bg-yellow-300 p-1 rounded-md font-medium cursor-pointer" @click="editIntegration(integration.id)">Edit</span>
                        <span class="mx-1 bg-red-400 p-1 rounded-md font-medium cursor-pointer" @click="()=>deleteIntegrationHandler(integration.id,integration.name)">Delete</span>
                    </td>                
                </tr>
            </tbody>
            <tbody v-else>
                <tr class="border-b bg-slate-50">
                    <td colspan="3" class="text-left py-3 px-2 font-medium">No API Keys found...</td>
                </tr>
            </tbody>
        </table>
        <div @click="addIntegrationHandler" v-if="isCreate" class="bg-slate-200/60 backdrop-blur-sm w-full h-full absolute top-0 left-0">
            <div @click.stop class="w-[40%] mx-auto bg-slate-200 backdrop-blur-md drop-shadow-md  mt-[12%] rounded-md px-5 pt-3 pb-1">
                <h1 class="text-3xl font-medium">Add Integration</h1>
                <hr class="w-[50%]">
                <form @submit.prevent="addIntegration" class="my-4 flex flex-col gap-3">
                    <div class="flex flex-col gap-1">
                        <label for="name">API Name: </label>
                        <input v-model="integration.name" class="shadow-sm rounded-md px-1.5 h-10 outline-none" type="text" id="name" placeholder="Enter the API name" />
                    </div>
                    <div class="flex flex-col gap-1">
                        <label for="key">API Key: </label>
                        <input v-model="integration.key" class="shadow-sm rounded-md px-1.5 h-10 outline-none" type="text" id="key" placeholder="Enter the API key" />
                    </div>
                    <div>
                        <button class="bg-slate-100 p-2 rounded-md shadow-md" type="submit">Add Integration</button>
                    </div>
                </form>
            </div>
        </div>
        <div :style="{'display':isDelete?'block':'none'}" class="bg-slate-200/60 backdrop-blur-sm w-full h-full absolute top-0 left-0 block">
            <div @click.stop class="w-[50%] mx-auto bg-slate-300/70 drop-shadow-md mt-[10%] rounded-md p-4">
                <h1 class="text-3xl font-medium my-1">Delete Integration</h1>
                <p class="mb-4">
                    Are you sure you want to delete the integration "<strong>{{ integration.name }}</strong>"? 
                    This action is irreversible and will permanently remove the API key and all associated data 
                    for this integration. Please confirm your action.
                </p>
                <div class="flex justify-start gap-4 font-medium">
                    <button @click="()=>deleteIntegration(id)" class="bg-red-500 p-2 rounded-md shadow-md mt-2" type="button">Delete</button>
                    <button @click="()=>deleteIntegrationHandler(null,'')" class="bg-slate-200 p-2 rounded-md shadow-md mt-2" type="button">Cancel</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
    data() {
        return {
            id: null,
            integration: {
                name: '',
                key: ''
            },
            isCreate: false,
            isDelete: false
        };
    },
    computed: {
        ...mapGetters(['getIntegrations'])
    },
    mounted() {
        this.$store.dispatch('getIntegrations');
    },
    methods: {
        addIntegrationHandler() {
            this.isCreate = !this.isCreate;
        },
        deleteIntegrationHandler(id,name){
            this.isDelete = !this.isDelete
            if(id&&name){
                this.id=id
                this.integration.name=name
            }else{
                this.id=null
                this.integration.name=''
            }
        },
        addIntegration() {
            if (this.integration.name && this.integration.key) {
                const name = this.integration.name;
                const key = this.integration.key;
                this.$store.dispatch('addIntegration', { name, key });
                this.integration = { name: '', key: '' };
                this.isCreate = false;
            }
        },
        maskKey(key) {
            return key.slice(0, -3).replace(/./g, '*') + key.slice(-3);
        },
        editIntegration(id) {
            console.log(`Edit integration with ID: ${id}`);
            // Handle edit logic here
        },
        deleteIntegration(id) {
            this.$store.dispatch('deleteIntegration',{id})
            this.isDelete = false
        }
    }
};
</script>
