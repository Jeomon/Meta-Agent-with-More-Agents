<template>
  <form @submit.prevent="submitQuery" class="text-lg max-h-32 absolute bottom-[22.5%] z-10 flex flex-row items-end gap-x-2">
    <button type="button" @click="showOptions" class="relative">
      <img class="w-4 h-4 p-4 box-content rounded-full hover:bg-slate-200/90 backdrop-blur-sm bg-slate-100/90 drop-shadow-md" src="../../assets/3-dot.svg" />
    </button>
    <div :style="{'display':isoptions?'block':'none'}" class="absolute bottom-[3.3rem] -left-7 bg-slate-200 p-2 rounded-lg shadow-md">
      <div class="flex flex-col gap-1">
        <span>Document</span>
        <span>Audio</span>
        <span>Video</span>
        <span>Image</span>
      </div>
    </div>
    <textarea
      rows="1"
      @input="heightAdjust"
      ref="textarea"
      class="backdrop-blur-sm bg-slate-100/90 focus:bg-slate-200/90 w-[50vw] drop-shadow-md py-3 px-3.5 outline-none resize-none rounded-3xl overflow-y-hidden"
      placeholder="Enter your query here"
    ></textarea>
    <button type="submit">
      <img class="w-10 h-10 p-1 box-content rounded-full hover:bg-slate-200/90 backdrop-blur-sm bg-slate-100/90 drop-shadow-md" src="../../assets/triangle.svg" />
    </button>
  </form>
</template>
<script>
import { mapGetters } from 'vuex';

export default {
  data() {
    return {
      isoptions:false,
      socket: null,
      current_message:null
    };
  },
  computed: {
    ...mapGetters(['getLastMessage']),
  },
  mounted() {
    this.heightAdjust();
    this.socket = new WebSocket('ws://localhost:8000/ws');

    // Ensure the socket connection is established before trying to send messages
    this.socket.onopen = () => {
      console.log('WebSocket connection established');
    };

    this.socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log(data);
      if(data.current_agent && !this.current_message){
        this.current_message={id: Date.now(), role: 'assistant', content: data }
        this.$store.commit('addMessage',this.current_message)
      }
      else if(data.current_agent && this.current_message){
        this.$store.commit('updateMessage', { ...this.current_message, content: data })
      }
      else if(data.output){
        this.$store.commit('updateMessage', { ...this.current_message, content: data })
        this.current_message=null
      }
    };

    this.socket.onclose = () => {
      console.log('WebSocket connection closed');
    };

    this.socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  },
  computed: {
    ...mapGetters(['getQuery']),
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
    submitQuery() {
      const content = this.$refs.textarea.value;
      if (content) {
        // Only send the message if the socket is open
        if (this.socket.readyState === WebSocket.OPEN) {
          this.socket.send(content);
          this.$store.commit('setQuery', content);
          this.$store.commit('addMessage', {id: Date.now(), role: 'user', content });
          this.$refs.textarea.value = ''; // Clear the textarea after sending
        } else {
          console.error('WebSocket is not open. Unable to send message.');
        }
      }
    },
    showOptions() {
      this.isoptions=!this.isoptions
    }
  },
};
</script>
