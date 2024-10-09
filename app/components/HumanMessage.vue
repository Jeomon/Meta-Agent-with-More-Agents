<template>
    <div class="w-full flex flex-row justify-end">
        <div class="flex flex-col w-fit max-w-[70%]">
            <div class="flex flex-row gap-1.5 py-2.5 px-3 rounded-3xl bg-slate-100">
                <img src="../assets/user.png" class="w-10 h-10">
                <p class="mt-1.5 leading-relaxed text-pretty text-base">{{ content }}</p>
            </div>
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