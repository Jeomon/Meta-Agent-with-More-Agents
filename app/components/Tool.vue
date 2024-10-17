<template>
    <div class="bg-stone-100 px-3 py-3 rounded-lg flex flex-row justify-between">
        <div class="flex flex-row items-start gap-x-2">
            <img class="w-9 h-9 rounded-lg bg-stone-200 p-1" src="../assets/tool.svg" />
            <div class="flex flex-col gap-1">
                <h1 class="text-lg font-medium">Weather Tool</h1>
                <p class="text-pretty">Retrieves the current weather information for a specific location.</p>
            </div>
        </div>
        <div>
            <img @click="toggleMenu" class="w-3.5 h-3.5 cursor-pointer relative mb-1" src="../assets/3-dot.svg" />
            <ul :style="{ display: isclicked ? 'block' : 'none' }" class="absolute bg-white rounded-md text-base shadow-md overflow-hidden">
                <li @click="editEvent" class="hover:bg-slate-100 py-1 px-2.5 cursor-pointer">Edit</li>
                <li @click="deleteEvent" class="hover:bg-slate-100 py-1 px-2.5 cursor-pointer">Delete</li>
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
            this.isclicked = !this.isclicked;
        },
        editEvent(){
            this.isclicked = !this.isclicked
            this.$emit('edit','This tool is edited')
        },
        deleteEvent(){
            this.isclicked = !this.isclicked
            this.$emit('delete','This tool is deleted')
        }
    }
}
</script>
