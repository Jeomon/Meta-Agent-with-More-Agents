<template>
    <div class="w-full flex flex-col justify-start">
        <div class="flex flex-col w-fit max-w-[70%] gap-1">
            <span class="font-medium text-sm">{{ agent }}</span>
            <div class="flex flex-row gap-2 py-2.5 px-3 rounded-3xl bg-slate-50">
                <img src="../assets/groq.png" class="w-10 h-10 rounded-full">
                <p class="mt-1.5 leading-relaxed text-pretty text-base">{{ content }}</p>
            </div>
            <span v-if="content!='Loading...'" class="flex flex-row gap-3 mt-2 mr-1 justify-end items-center">
                <img class="w-4 h-4 cursor-pointer" src="../assets/copy.svg"/>
                <img class="w-4 h-4 cursor-pointer" src="../assets/like.svg"/>
                <img class="w-4 h-4 cursor-pointer" src="../assets/dislike.svg"/>
                <img class="w-4 h-4 cursor-pointer" src="../assets/refresh.svg"/>
                <img class="w-3.5 h-3.5 cursor-pointer" src="../assets/3-dot.svg"/>
            </span>
        </div>
    </div>
</template>
<script>
export default {
    props : {
        content:String,
        agent:String
    }
}
</script>