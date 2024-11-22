<template>
    <div class="w-full h-full p-4 ">
        <div class="flex flex-row items-center">
            <img class="w-9 h-9" src="../assets/profile.svg"/>
            <h1 class="text-4xl m-2">Profile</h1>
        </div>
        <hr>
        <form class="flex flex-col gap-2 mt-5 p-2">
            <div class="relative">
                <img class="w-36 h-36 rounded-full" src="../assets/user.png"/>
                <div class="absolute top-[0%] left-[0%] bg-slate-100 w-36 h-36 flex justify-center items-center rounded-full opacity-60">
                    <label class="cursor-pointer" for="profile">
                        Change Profile
                        <input id="profile" type="file" hidden class="text-center text-blue-500 opacity-100"/>
                    </label>
                </div>
            </div>
            <div class="flex flex-row gap-5 mt-4">
                <div class="text-lg flex flex-row gap-2">
                    <label class="font-medium" for="First name">First name:</label>
                    <input class="outline-none border-2 rounded-md border-black" type="text"/>
                </div>
                <div class="text-lg flex flex-row gap-2">
                    <label class="font-medium" for="Last name">Last name:</label>
                    <input class="outline-none border-2 rounded-md border-black" type="text"/>
                </div>
            </div>
            <div class="flex flex-row gap-5 mt-4">
                <div class="text-lg flex flex-row gap-2">
                    <label class="font-medium" for="E-mail">Email:</label>
                    <input class="outline-none border-2 rounded-md border-black" type="email"/>
                </div>
            </div>
            <div class="flex flex-col items-start gap-5 mt-4 w-full h-auto">
                <div class="text-lg flex flex-row gap-2">
                    <label class="font-medium" for="Bio">Bio:</label>
                    <textarea :rows="8" class="outline-none border-2 border-black rounded-md w-[40vw] resize-none p-1" placeholder="Enter bio here"></textarea>
                </div>
                <button class="bg-slate-300 p-2 font-medium rounded-md text-lg" type="submit">Update Profile</button>
            </div>
        </form>
    </div>
</template>
<script>
export default {
    data(){
        return {
        
        }
    }
}
</script>