<template>
    <button>
        <svg class="w-9 h-9 drop-shadow-md" xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="18.25 18.25 63.5 63.5">
            <path d="m50.004 18.246c-17.512 0-31.75 14.238-31.75 31.75 0 17.512 14.238 31.75 31.75 31.75 17.512 0 31.75-14.238 31.75-31.75 0-17.512-14.238-31.75-31.75-31.75zm0 4c15.348 0 27.75 12.402 27.746 27.75 0 15.348-12.398 27.758-27.746 27.758s-27.754-12.406-27.758-27.758c0-15.348 12.406-27.75 27.758-27.75zm-15.398 24.551c-1.7617 0-3.1953 1.4297-3.1953 3.1953-0.003906 0.84766 0.33203 1.6641 0.92969 2.2656 0.60156 0.60547 1.418 0.94141 2.2656 0.94531 0.85547 0.003906 1.6719-0.33594 2.2773-0.9375 0.60547-0.60156 0.94141-1.4219 0.94141-2.2734-0.003907-0.85156-0.34375-1.668-0.94531-2.2656-0.60547-0.60156-1.4219-0.93359-2.2734-0.92969zm15.359 0h0.003906c-1.7656 0-3.1953 1.4297-3.1992 3.1953-0.003906 0.84766 0.33203 1.6641 0.93359 2.2656 0.59766 0.60547 1.4141 0.94141 2.2656 0.94531s1.6719-0.33594 2.2734-0.9375c0.60547-0.60156 0.94141-1.4219 0.94141-2.2734-0.003906-0.85156-0.34375-1.668-0.94531-2.2656-0.60547-0.60156-1.4219-0.93359-2.2695-0.92969zm15.359 0c-1.7617 0-3.1914 1.4297-3.1953 3.1953-0.003906 0.84766 0.33203 1.6641 0.93359 2.2656 0.59766 0.60156 1.4141 0.94141 2.2617 0.94531 0.85547 0.003906 1.6758-0.33203 2.2773-0.9375 0.60547-0.60156 0.94531-1.4219 0.94141-2.2734 0-0.85156-0.33984-1.668-0.94531-2.2656-0.60547-0.60156-1.4219-0.9375-2.2734-0.92969z"/>
        </svg>
    </button>
    <textarea name="query" ref="textarea" @input="autoResizeTextarea" class="antialiased drop-shadow-md w-[55%] text-wrap h-auto relative py-3 px-5 font-normal block box-border bottom-0 overflow-hidden border-[2.5px] border-black bg-white resize-none rounded-[2rem] outline-none placeholder:text-slate-600" placeholder="Type your message..."></textarea>
    <button type="submit">
        <svg class="w-9 h-9 drop-shadow-md" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" x="0px" y="0px" style="enable-background:new 0 0 24 24;" xml:space="preserve" viewBox="2.04 2.04 19.92 19.92">
            <g>
                <path d="M12,21.959c5.501,0,9.959-4.459,9.959-9.959c0-5.5-4.459-9.959-9.959-9.959C6.5,2.041,2.041,6.5,2.041,12   C2.041,17.5,6.5,21.959,12,21.959z M12,3.286c4.805,0,8.714,3.909,8.714,8.714c0,4.805-3.909,8.714-8.714,8.714   c-4.805,0-8.714-3.909-8.714-8.714C3.286,7.195,7.195,3.286,12,3.286z"/><polygon points="11.378,10.317 11.378,17.001 12.623,17.001 12.623,10.313 15.112,12.801 15.992,11.921 12.003,7.932 8.009,11.926    8.889,12.807  "/>
            </g>
        </svg>
    </button>
</template>
<script>

export default {
    data() {
        return {
            initialHeight: 0 // Store initial height for upward translation
        }
    },
    mounted() {
        // Save the initial height of the textarea after it's mounted
        this.initialHeight = this.$refs.textarea.scrollHeight;
    },
    methods: {
        autoResizeTextarea() {
            const textarea = this.$refs.textarea;

            // Reset height to auto first
            textarea.style.height = 'auto';

            // Calculate the new height based on content
            const newHeight = textarea.scrollHeight;

            // Set the new height
            textarea.style.height = newHeight+5 + 'px';

            textarea.style.bottom=newHeight-this.initialHeight+'px'
        }
    }
}
</script>
