<template>
    <div class="flex flex-col text-2xl w-full">
        <RouterLink class="hover:bg-slate-200 px-10 py-3 decoration-4 underline-offset-4 hover:underline decoration-slate-500 focus:bg-slate-200":to="{name:'profile'}">Profile</RouterLink>
        <RouterLink class="hover:bg-slate-200 px-10 py-3 decoration-4 underline-offset-4 hover:underline decoration-slate-500 focus:bg-slate-200":to="{name:'agents'}">Agents</RouterLink>
        <RouterLink class="hover:bg-slate-200 px-10 py-3 decoration-4 underline-offset-4 hover:underline decoration-slate-500 focus:bg-slate-200":to="{name:'tools'}">Tools</RouterLink>
        <RouterLink class="hover:bg-slate-200 px-10 py-3 decoration-4 underline-offset-4 hover:underline decoration-slate-500 focus:bg-slate-200":to="{name:'integrations'}">Integrations</RouterLink>
        <RouterLink class="hover:bg-slate-200 px-10 py-3 decoration-4 underline-offset-4 hover:underline decoration-slate-500 focus:bg-slate-200":to="{name:'about'}">About</RouterLink>
    </div>
</template>
<script>
export default {

}
</script>