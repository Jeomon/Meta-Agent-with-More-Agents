<template>
    <div class="flex flex-row justify-end my-2">
        <div class="flex flex-row gap-x-2 bg-slate-200/70 w-fit max-w-[40%] p-2.5 rounded-2xl items-center relative shadow-md">
            <img class="w-10 h-10 self-start rounded-full" src="../../assets/user.png"/>
            <p class="text-base">{{ content }}</p>
            <div class="flex flex-row gap-x-2 w-fit justify-center absolute -bottom-6 -right-1">
                <img class="w-4 h-4" src="../../assets/edit.svg"/>
                <img class="w-4 h-4" src="../../assets/3-dot.svg"/>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    props:{
        content: String
    }
}
</script>