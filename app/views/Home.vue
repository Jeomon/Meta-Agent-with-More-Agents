<template>
    <div class="h-screen grid grid-cols-6 grid-rows-4">
        <div class="col-span-1 row-span-4 flex flex-col gap-3 bg-slate-200 h-full w-full">
            <h1 class="text-3xl p-2">Chat history</h1>
            <div class="flex flex-col gap-2 px-3">
                <p>Hello</p>
                <p>Hello</p>
                <p>Hello</p>
                <p>Hello</p>
                <p>Hello</p>
                <p>Hello</p>
                <p>Hello</p>
                <p>Hello</p>
            </div>
        </div>
        <div class="col-span-5 row-span-4 h-full w-full">
            <div class="grid grid-rows-11 w-full h-full">
                <div class="row-span-1 flex justify-center items-center">
                    <img src="../assets/logo.svg" alt="logo" class="w-16 h-16 py-3">
                    <h1 class="text-4xl">MAMA</h1>
                </div>
                <div class="row-span-10">
                    <div class="grid grid-cols-12 grid-rows-9 w-full h-full">
                        <div class="row-span-8 col-span-1"></div>
                        <div class="row-span-8 col-span-10 p-5 flex flex-col gap-4 overflow-y-auto overflow-x-hidden scroll-smooth overscroll-none">
                            <div class="w-full flex flex-row justify-end">
                                <div class="flex flex-row items-start gap-1.5 p-2 rounded-3xl bg-slate-200 w-fit max-w-[70%]">
                                    <img src="../assets/ollama.png" class="w-10 h-10">
                                    <p class="mt-1">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Praesentium ipsa quod numquam corporis neque expedita animi consequatur amet, qui est nostrum optio aliquid quaerat ab harum illo sit iure labore.</p>
                                </div>
                            </div>
                            <div class="w-full flex flex-row justify-start">
                                <div class="flex flex-row justify-start items-start gap-1.5 p-2 rounded-3xl bg-slate-100 w-fit max-w-[70%]">
                                    <img src="../assets/ollama.png" class="w-10 h-10">
                                    <p class="mt-1">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minus qui accusamus, voluptas nihil dolorem ab cupiditate, voluptatibus natus tempore blanditiis itaque cumque ipsum non, neque unde facere aliquam a ad.</p>
                                </div>
                            </div>
                        </div>
                        <div class="row-span-8 col-span-1"></div>
                        <div class="row-span-1 col-span-full flex flex-row justify-center py-2 gap-3">
                            <textarea ref="textarea" @input="autoResizeTextarea" class="relative p-3 font-normal block box-border bottom-0 w-[60%] h-auto overflow-hidden text-balance border-[2.5px] border-black bg-white resize-none rounded-[2rem] outline-none placeholder:text-slate-600" placeholder="Type your message..."></textarea>
                            <button>
                                <svg class="w-12 h-12" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" x="0px" y="0px" style="enable-background:new 0 0 24 24;" xml:space="preserve" viewBox="2.04 2.04 19.92 19.92">
                                    <g>
                                        <path d="M12,21.959c5.501,0,9.959-4.459,9.959-9.959c0-5.5-4.459-9.959-9.959-9.959C6.5,2.041,2.041,6.5,2.041,12   C2.041,17.5,6.5,21.959,12,21.959z M12,3.286c4.805,0,8.714,3.909,8.714,8.714c0,4.805-3.909,8.714-8.714,8.714   c-4.805,0-8.714-3.909-8.714-8.714C3.286,7.195,7.195,3.286,12,3.286z"/><polygon points="11.378,10.317 11.378,17.001 12.623,17.001 12.623,10.313 15.112,12.801 15.992,11.921 12.003,7.932 8.009,11.926    8.889,12.807  "/>
                                    </g>
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
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
