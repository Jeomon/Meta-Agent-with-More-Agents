<template>
    <form @submit.prevent="sendQuery" class="text-lg max-h-32 absolute bottom-[22.5%] z-10 flex flex-row items-end gap-x-2">
        <button type="button">
          <img class="w-4 h-4 p-4 box-content rounded-full hover:bg-slate-200/90 backdrop-blur-sm bg-slate-100/90 drop-shadow-md" src="../../assets/3-dot.svg"/>
        </button>
        <textarea rows="1" @input="heightAdjust" ref="textarea" class="backdrop-blur-sm bg-slate-100/90 focus:bg-slate-200/90 w-[50vw] drop-shadow-md py-3 px-3.5 outline-none resize-none rounded-3xl overflow-y-hidden" placeholder="Enter your query here"></textarea>
        <button type="submit">
          <img class="w-10 h-10 p-1 box-content rounded-full hover:bg-slate-200/90 backdrop-blur-sm bg-slate-100/90 drop-shadow-md" src="../../assets/triangle.svg"/>
        </button>
    </form>
</template>
<script>
export default {
  mounted(){
    this.heightAdjust()
  },
  methods: {
    heightAdjust() {
      const textarea = this.$refs.textarea;
      if (textarea) {
        textarea.style.height = '60%';
        const newHeight = Math.min(textarea.scrollHeight, 256); // Max height of 256px (32 * 8px)
        textarea.style.height = `${newHeight}px`;
      }
    },
    sendQuery() {
      const query = this.$refs.textarea.value;
      if (query) {

      }
    },
  }
}
</script>