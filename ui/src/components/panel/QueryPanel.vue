<template>
  <form @submit.prevent="submitQuery" class="text-lg max-h-32 absolute bottom-[22.5%] z-10 flex flex-row items-end gap-x-2">
    <textarea ref="textarea" v-model.trim="query" rows="1" @input="heightAdjust" class="backdrop-blur-sm bg-slate-100/90 focus:bg-slate-200/90 w-[50vw] drop-shadow-md py-3 px-3.5 outline-none resize-none rounded-3xl" placeholder="Message MAMA"></textarea>
    <button type="submit" class="backdrop-blur-sm drop-shadow-md rounded-full hover:bg-slate-200/90 bg-slate-100/90 focus:bg-slate-200/90">
      <img class="w-10 h-10 p-1 box-content" src="../../assets/triangle.svg" />
    </button>
  </form>
</template>
<script>
import { mapGetters } from 'vuex';
export default {
  data() {
    return {
      currentConversation:null,
      socket: null,
      query:''
    };
  },
  computed: {
    ...mapGetters(['getConversation','getConversations'])
  },
  async mounted() {
    this.heightAdjust();
    this.socket = new WebSocket('ws://localhost:8000/ws');
    let conversations =await this.$store.dispatch('getConversations')
    this.currentConversation=conversations.find(conversation => conversation.length==0)
    if(!this.currentConversation){
      this.$store.commit('getMessages',[])
    }

    // Ensure the socket connection is established before trying to send messages
    this.socket.onopen = () => {
      console.log('WebSocket connection established');
    };

    this.socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if(data.output){
        this.$store.dispatch('addMessage',{role: 'assistant', content: data.output, conversation_id:this.currentConversation.id});
      }
    };

    this.socket.onclose = () => {
      console.log('WebSocket connection closed');
    };

    this.socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  },
  computed:{
    ...mapGetters(['getConversation','getMessages','getConversations'])
  },
  methods: {
    heightAdjust() {
      const textarea = this.$refs.textarea;
      if (textarea) {
        textarea.style.height = '60%';
        const newHeight = Math.min(textarea.scrollHeight, 140); // Max height of 256px (32 * 8px)
        textarea.style.height = `${newHeight}px`;
      }
    },
    async submitQuery() {;
      if (this.query.length>0) {
        if(!this.currentConversation){
          this.currentConversation=this.getConversation
        }
        // Only send the message if the socket is open
        if (this.socket.readyState === WebSocket.OPEN) {
            if (!this.currentConversation.id){
              this.currentConversation=await this.$store.dispatch('addConversation',this.query)
            }
            else if (this.currentConversation.id&&this.getMessages.length==0){
              this.$store.dispatch('editConversation',{'id':this.currentConversation.id,'title':this.query})
            }
            await this.$store.dispatch('addMessage',{role: 'user', content: this.query, conversation_id:this.currentConversation.id});
            await this.socket.send(this.query);
            this.query = ''; // Clear the textarea after sending
        }
        else {
          console.error('WebSocket is not open. Unable to send message.');
        }
      }
    }
  }
};
</script>
