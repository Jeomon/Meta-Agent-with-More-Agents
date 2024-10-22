<template>
    <div class="flex flex-col justify-start gap-1 my-2">
        <p class="text-lg/2">Calling Weather Agent</p>
        <div class="flex flex-row gap-x-2 bg-slate-100/80 w-fit max-w-[40%] p-2.5 rounded-2xl items-center relative shadow-md">
            <img class="w-10 h-10 rounded-full self-start" src="../../assets/groq.png"/>
            <p class="text-lg/3">Hi, How are you</p>
            <div class="flex flex-row gap-x-2 w-fit justify-center absolute -bottom-6 -right-1">
                <img class="w-4 h-4" src="../../assets/like.svg"/>
                <img class="w-4 h-4" src="../../assets/dislike.svg"/>
                <img class="w-4 h-4" src="../../assets/refresh.svg"/>
                <img class="w-4 h-4" src="../../assets/3-dot.svg"/>
            </div>
        </div>
    </div>
</template>