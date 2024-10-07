<template>
    <div class="h-screen grid grid-cols-6 grid-rows-4">
        <div class="col-span-1 row-span-4 flex flex-col gap-3 bg-slate-200 h-full w-full">
            <h1 class="text-3xl p-2">Chat History</h1>
            <div class="flex flex-col gap-2 px-3">
                <div class="flex flex-row items-center justify-between">
                    <p class="">Quantum Computing</p>
                    <img class="w-4 h-4 cursor-pointer" src="../assets/3-dot.svg"/>
                </div>
                <div class="flex flex-row items-center justify-between">
                    <p class="">Quantum Computing</p>
                    <img class="w-4 h-4 cursor-pointer" src="../assets/3-dot.svg"/>
                </div>
            </div>
        </div>
        <div class="col-span-5 row-span-4 h-full w-full">
            <div class="grid grid-rows-11 w-full h-full">
                <div class="row-span-1 flex justify-center items-center">
                    <img src="../assets/logo.svg" alt="logo" class="w-16 h-16 py-3">
                    <h1 class="text-4xl">ChatBook</h1>
                </div>
                <div class="row-span-10">
                    <div class="grid grid-cols-12 grid-rows-9 w-full h-full">
                        <div class="row-span-8 col-span-1"></div>
                        <div class="row-span-8 col-span-10 p-5 flex flex-col gap-4 overflow-y-auto overflow-x-hidden scroll-smooth overscroll-none">
                            <HumanMessage/>
                            <AIMessage/>
                        </div>
                        <div class="row-span-8 col-span-1"></div>
                        <form @submit="submitHandler" class="row-span-1 col-span-full flex flex-row justify-center py-2 gap-3">
                            <QueryPanel/>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import AIMessage from '@/components/AIMessage.vue';
import HumanMessage from '@/components/HumanMessage.vue';
import QueryPanel from '@/components/QueryPanel.vue';
import axios from 'axios';

export default {
    methods:{
        async submitHandler(e){
            e.preventDefault();
            let query=e.target.querySelector('textarea').value;
            if(query){
                let response=await axios.post('/query',{
                    'query':query
                })
                let data=await response.data;
                console.log(data);
                
            }
        }
    },
    components:{
        AIMessage,HumanMessage,QueryPanel
    }
}
</script>
