<template>
  <div class="grid grid-cols-11 grid-rows-8 w-full h-screen bg-white">
    <div class="col-span-2 row-span-8 bg-slate-100 p-2 relative">
      <HistoryPanel/>
      <img class="w-8 h-8 cursor-pointer rotate-180 absolute -right-3.5 top-[50%] bg-slate-500 rounded-full" src="../assets/arrow.svg"/>
    </div>
    <div class="col-span-9 row-span-7 bg-transparent relative h-screen">
      <LogoPanel/>
      <UserPanel/>
      <ChatPanel/>
    </div>
    <div class="col-span-9 row-span-1 relative flex justify-center bg-transparent">
      <QueryPanel/>
    </div>
  </div>
</template>
  
<script>
import ChatPanel from '../components/panel/ChatPanel.vue';
import HistoryPanel from '../components/panel/HistoryPanel.vue';
import LogoPanel from '../components/panel/LogoPanel.vue';
import QueryPanel from '../components/panel/QueryPanel.vue';
import UserPanel from '../components/panel/UserPanel.vue';
  
export default {
    components: {
      QueryPanel,UserPanel,HistoryPanel,ChatPanel,LogoPanel
    }
}
</script>