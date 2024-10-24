<template>
    <div class="grid grid-cols-12 w-full h-screen">
        <div class="col-span-2 bg-slate-300 flex justify-center items-center relative">
            <RouterLink :to="{name: 'home'}" class="absolute top-0 left-0 p-2 text-lg bg-slate-200 rounded-md">Home</RouterLink>
            <MenuPanel/>
            <img class="w-8 h-8 rotate-180 absolute z-30 -right-3.5 top-[50%] bg-slate-500 rounded-full" src="../assets/arrow.svg"/>
        </div>
        <div class="col-span-10 bg-slate-100">
            <RouterView name="content"/>
        </div>
    </div>
</template>
<script>
import MenuPanel from '@/components/panel/MenuPanel.vue';

export default {
    components: {
        MenuPanel
    }
}
</script>