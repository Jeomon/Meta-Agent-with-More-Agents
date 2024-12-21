<template>
    <div class="bg-slate-100 w-full h-screen">
        <div class="flex flex-row gap-0.5 absolute left-0 right-0 w-fit translate-y-1/2 mx-auto bg-slate-200 rounded-md drop-shadow-md overflow-hidden">
            <form @submit.prevent="loginHandler" class="flex flex-col gap-2 justify-center py-2 px-4">
                <h2 class="text-3xl font-semibold mt-2">Sign In</h2>
                <div class="flex flex-col gap-1.5 mt-1">
                    <label for="email">Username</label>
                    <input v-model="userCredential.username" class="outline-none rounded-md p-1"type="text"/>
                </div>
                <div class="flex flex-col gap-1.5 mt-0.5">
                    <label for="email">Password</label>
                    <input v-model="userCredential.password" class="outline-none rounded-md p-1"type="password"/>
                </div>
                <div class="flex justify-center items-end gap-2 my-2">
                    <button class="bg-slate-100 hover:bg-slate-300 w-fit p-1.5 rounded-md drop-shadow-md font-medium">Login</button>
                    <p class="text-smnd mb-1">Don't have an account? <RouterLink class="text-blue-600 font-medium" :to="{name:'signup'}">Sign Up</RouterLink></p>
                </div>
            </form>
        </div>
    </div>
</template>
<script>
    export default {
        data(){
            return {
                userCredential:{
                    username:'',
                    password:''
                }
            }
        },
        methods:{
            loginHandler(){
                let username=this.userCredential.username.trim()
                let password=this.userCredential.password.trim()
                let redirect=this.$route.query?.redirect
                if(username&&password){
                    this.$store.dispatch('signinUser',{username,password,redirect})
                }
            }
        }
    }
</script>