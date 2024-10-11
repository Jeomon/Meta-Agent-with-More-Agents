<template>
    <div class="grid grid-cols-12 h-screen bg-slate-100">
        <div class="col-span-2 flex flex-col items-center my-auto h-fit font-medium text-xl">
            <RouterLink class="py-5" :to="{name:'profile'}">Profile</RouterLink>
            <RouterLink class="py-5" :to="{name:'agents'}">Agents</RouterLink>
            <RouterLink class="py-5" :to="{name:'tools'}">Tools</RouterLink>
            <RouterLink class="py-5" :to="{name:'integrations'}">Integrations</RouterLink>
            <RouterLink class="py-5" :to="{name:'about'}">About</RouterLink>
        </div>
        <div class="col-span-10 bg-slate-50">
            <RouterView/>
        </div>
    </div>
</template>