<template>
  <RouterView/>
</template>

<script>
export default {
  name: 'App',
  mounted(){
    this.$store.commit('isAuthenticated')
  }
}
</script>

<style>
* {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}
</style>
