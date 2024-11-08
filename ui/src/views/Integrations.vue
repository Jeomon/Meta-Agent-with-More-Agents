<template>
    <div class="w-full h-full p-4 relative">
        <div class="flex justify-between items-center">
            <h1 class="text-4xl m-2">Integrations</h1>
            <span @click="addIntegrationHandler" class="cursor-pointer p-2 bg-slate-300 rounded-md text-lg hover:bg-slate-400">Add Integration</span>
        </div>
        <hr>
        <table class="w-[45%] rounded-lg mt-5  table-fixed">
            <thead>
                <tr class="border-b bg-white">
                    <th class="text-left py-3 px-2 font-medium">Name</th>
                    <th class="text-left py-3 px-2 font-medium">API Key</th>
                </tr>
            </thead>
            <tbody v-if="getIntegrations?.length>0">
                <tr v-for="integration in getIntegrations" class="border-b bg-slate-50">
                    <td class="py-3 px-4">{{ integration.name }}</td>
                    <td class="py-3 px-4 font-mono flex justify-between">
                        <span>{{ integration.key }}</span>
                        <img class="w-4 h-4 cursor-pointer" src="../assets/3-dot.svg"/>
                    </td>
                </tr>
            </tbody>
            <tbody v-else>
                <tr class="border-b bg-slate-50">
                    <td colspan="2" class="text-left py-3 px-2 font-medium">No API Keys found...</td>
                </tr>
            </tbody>
        </table>
        <div @click="addIntegrationHandler" :style="{'display':isCreate?'block':'none'}" class="bg-slate-200/60 backdrop-blur-sm w-full h-full absolute top-0 left-0">
            <div @click.stop class="w-[40%] mx-auto bg-slate-300/60 backdrop-blur-md drop-shadow-md  mt-[12%] rounded-md px-5 pt-3 pb-1">
                <h1 class="text-3xl font-medium">Add Integration</h1>
                <hr class="w-[50%]">
                <form @submit.prevent="addIntegration" class="my-4 flex flex-col gap-3">
                    <div class="flex flex-col gap-1">
                        <label role="name" for="name">API Name: </label>
                        <input v-model="integration.name" class="shadow-sm rounded-md px-1.5 h-10 outline-none" type="text" id="name" placeholder="Enter the API name"/>
                    </div>
                    <div class="flex flex-col gap-1">
                        <label role="key" for="name">API Key: </label>
                        <input v-model="integration.key" class="shadow-sm rounded-md px-1.5 h-10 outline-none" type="text" id="key" placeholder="Enter the API key"/>
                    </div>
                    <div>
                        <button class="bg-slate-200 p-2 rounded-md shadow-md" type="submit">Add Integration</button>
                    </div>
                </form>
            </div>
        </div>
        <!-- TODO: DELETE Integration -->
        <div class="w-full h-[93%] px-2 py-5 overflow-y-auto">
            
        </div>
    </div>
</template>
<script>
import { mapGetters } from 'vuex';

export default {
    data(){
        return {
            integration:{
                name:'',
                key:''
            },
            isCreate:false
        }
    },
    computed:{
        ...mapGetters(['getIntegrations'])
    },
    mounted(){
        this.$store.dispatch('getIntegrations')
    },
    methods:{
        addIntegrationHandler(){
            this.isCreate=!this.isCreate
        },
        addIntegration(){
            if(this.integration.name&&this.integration.key){
                let name=this.integration.name
                let key=this.integration.key
                this.$store.dispatch('addIntegration',{name,key})
                this.integration={
                    name:'',
                    key:''
                }
                this.isCreate=false
            }
        }
    }
}
</script>