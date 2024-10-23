<template>
    <div class="absolute right-0 p-4">
        <div class="relative">
            <img @click="toggleMenuHandler" src="../../assets/user.png" alt="profile image" class="w-11 h-11 rounded-full cursor-pointer">
            <div :style="{'display': toggleMenu ? 'flex' : 'none'}" class="backdrop-blur-md bg-slate-100/90 flex-col rounded-md gap-y-3 p-3 absolute top-12 right-0 text-left w-[16vw] text-base drop-shadow-lg z-20">
                <RouterLink :to="{name:'agents'}" class="flex flex-row gap-2.5 items-center">
                    <img class="w-6 h-6" src="../../assets/agent.svg"/>
                    <p>Agents</p>
                </RouterLink>
                <RouterLink :to="{name:'tools'}" class="flex flex-row gap-2.5 items-center">
                    <img class="w-6 h-6" src="../../assets/tool.svg"/>
                    <p>Tools</p>
                </RouterLink>
                <RouterLink :to="{name:'settings'}" class="flex flex-row gap-2.5 items-center">
                    <img class="w-6 h-6" src="../../assets/settings.svg"/>
                    <p>Settings</p>
                </RouterLink>
                <hr class="bg-slate-100">
                <RouterLink class="flex flex-row gap-2.5 items-center">
                    <img class="w-6 h-6" src="../../assets/logout.svg"/>
                    <p>Log out</p>
                </RouterLink>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    data(){
        return {
            toggleMenu:false
        }
    },
    methods:{
        toggleMenuHandler(){
            this.toggleMenu = !this.toggleMenu
        }
    }
}
</script>