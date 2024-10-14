<template>
    <div class="bg-stone-100 px-3 py-3 rounded-lg flex flex-row justify-between">
        <div class="flex flex-row items-start gap-x-2">
            <img class="w-10 h-10 rounded-xl bg-stone-200 p-1" src="../assets/agent.svg" />
            <div class="flex flex-col gap-1">
                <h1 class="text-lg font-medium">Weather Agent</h1>
                <p class="text-pretty">This agent is responsible for providing information related to weather based on the given location.</p>
                <span class="font-medium">Tool: <p class="w-fit inline-block font-normal">Weather Tool</p></span>
            </div>
        </div>
        <div>
            <img @click="toggleMenu" class="w-3.5 h-3.5 cursor-pointer relative mb-1" src="../assets/3-dot.svg" />
            <ul :style="{ display: isclicked ? 'block' : 'none' }" class="absolute bg-white rounded-md text-base shadow-md overflow-hidden">
                <li class="hover:bg-slate-100 py-1 px-2.5 cursor-pointer">Edit</li>
                <li class="hover:bg-slate-100 py-1 px-2.5 cursor-pointer">Delete</li>
            </ul>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            isclicked: false
        }
    },
    methods: {
        toggleMenu() {
            this.isclicked = !this.isclicked; // Toggle the isclicked state
        }
    }
}
</script>
