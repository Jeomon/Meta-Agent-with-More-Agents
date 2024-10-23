<template>
    <div class="flex flex-col gap-5 text-2xl">
        <RouterLink :to="{name:'profile'}">Profile</RouterLink>
        <RouterLink :to="{name:'agents'}">Agents</RouterLink>
        <RouterLink :to="{name:'tools'}">Tools</RouterLink>
        <RouterLink :to="{name:'integrations'}">Integrations</RouterLink>
        <RouterLink :to="{name:'about'}">About</RouterLink>
    </div>
</template>
<script>
export default {

}
</script>