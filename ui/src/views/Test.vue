<template>
    <div class="min-h-screen flex">
      <!-- Left Sidebar -->
      <div class="w-72 bg-gray-50 border-r border-gray-200 p-4 flex flex-col">
        <button @click="createNewConversation" class="flex items-center mb-4 text-gray-700 hover:text-gray-900">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 4v16m-8-8h16" />
          </svg>
          New Conversation
        </button>
        <div class="flex-grow overflow-y-auto">
          <ul v-if="conversations.length > 0" class="w-full">
            <li v-for="(conversation, index) in conversations" :key="index" class="mb-2 relative group">
              <button class="w-full text-left p-2 rounded hover:bg-gray-200 flex justify-between items-center">
                <span>{{ conversation.title }}</span>
                <div class="relative">
                  <button @click.stop="toggleConversationMenu(index)" class="p-1 text-gray-400 hover:text-gray-600 opacity-0 group-hover:opacity-100 transition-opacity">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
                    </svg>
                  </button>
                  <div v-if="activeConversationMenu === index" class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-10">
                    <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                      </svg>
                      Rename
                    </a>
                    <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M15 8a3 3 0 10-2.977-2.63l-4.94 2.47a3 3 0 100 4.319l4.94 2.47a3 3 0 10.895-1.789l-4.94-2.47a3.027 3.027 0 000-.74l4.94-2.47C13.456 7.68 14.19 8 15 8z" />
                      </svg>
                      Share
                    </a>
                    <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                      </svg>
                      Delete
                    </a>
                    <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M4 3a2 2 0 100 4h12a2 2 0 100-4H4z" />
                        <path fill-rule="evenodd" d="M3 8h14v7a2 2 0 01-2 2H5a2 2 0 01-2-2V8zm5 3a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1z" clip-rule="evenodd" />
                      </svg>
                      Archive
                    </a>
                  </div>
                </div>
              </button>
            </li>
          </ul>
          <p v-else class="text-gray-500 italic text-center">No conversations found...</p>
        </div>
      </div>
  
      <!-- Main Content -->
      <div class="flex-1 flex flex-col relative">
        <!-- Header -->
        <header class="h-16 flex items-center justify-between px-4 border-b border-gray-200">
          <div class="flex items-center">
            <h1 class="text-xl font-semibold">MAMA</h1>
          </div>
          <div class="relative">
            <button @click="toggleProfileDropdown" class="w-8 h-8 rounded-full bg-gray-200 focus:outline-none">
              <span class="sr-only">Profile</span>
            </button>
            <div v-if="showProfileDropdown" class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-10">
              <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
                Profile
              </a>
              <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                  <circle cx="9" cy="7" r="4"></circle>
                  <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                  <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                </svg>
                Agents
              </a>
              <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"></path>
                </svg>
                Tools
              </a>
              <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                  <polyline points="16 17 21 12 16 7"></polyline>
                  <line x1="21" y1="12" x2="9" y2="12"></line>
                </svg>
                Sign Out
              </a>
            </div>
          </div>
        </header>
  
        <!-- Chat Area -->
        <div class="flex-1 flex flex-col p-4 overflow-y-auto">
          <h2 class="text-3xl font-semibold text-gray-800 mb-4">Hi, How can I help you?</h2>
          <!-- Chat messages would go here -->
        </div>
  
        <!-- Input Area -->
        <div class="absolute bottom-4 left-1/2 transform -translate-x-1/2 w-1/2">
          <div class="relative">
            <textarea
              v-model="message"
              placeholder="Message MAMA"
              rows="1"
              @input="autoResize"
              class="w-full px-12 py-3 bg-gray-100 rounded-lg focus:outline-none resize-none overflow-hidden pr-12"
            ></textarea>
            <div class="absolute bottom-3 left-4">
              <input type="file" id="fileUpload" class="hidden" @change="handleFileUpload" accept="image/*,audio/*,.pdf" />
              <label for="fileUpload" class="cursor-pointer">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-400 hover:text-gray-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48" />
                </svg>
              </label>
            </div>
            <div class="absolute bottom-3 right-4">
              <button @click="sendMessage" class="p-1 text-gray-400 hover:text-gray-600">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 transform rotate-45" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ChatInterface',
    data() {
      return {
        message: '',
        conversations: [],
        showProfileDropdown: false,
        activeConversationMenu: null,
      }
    },
    methods: {
      sendMessage() {
        if (this.message.trim()) {
          // Handle message sending logic here
          console.log('Sending message:', this.message)
          this.message = ''
          this.$nextTick(() => {
            this.autoResize()
          })
        }
      },
      autoResize(event) {
        const textarea = event ? event.target : this.$el.querySelector('textarea')
        textarea.style.height = 'auto'
        textarea.style.height = textarea.scrollHeight + 'px'
        const maxHeight = 200
        if (textarea.scrollHeight > maxHeight) {
          textarea.style.height = maxHeight + 'px'
          textarea.style.overflowY = 'auto'
        } else {
          textarea.style.overflowY = 'hidden'
        }
      },
      createNewConversation() {
        const newConversation = {
          id: Date.now(),
          title: `Conversation ${this.conversations.length + 1}`,
          messages: []
        }
        this.conversations.unshift(newConversation)
        console.log('New conversation created:', newConversation)
      },
      toggleProfileDropdown() {
        this.showProfileDropdown = !this.showProfileDropdown
      },
      toggleConversationMenu(index) {
        this.activeConversationMenu = this.activeConversationMenu === index ? null : index
      },
      handleFileUpload(event) {
        const file = event.target.files[0]
        if (file) {
          console.log('File uploaded:', file.name, file.type)
          // Handle file upload logic here
        }
      },
    },
    mounted() {
      this.$nextTick(() => {
        this.autoResize()
      })
    }
  }
  </script>
  
  <style scoped>
  .min-h-screen {
    min-height: 100vh;
  }
  
  textarea {
    min-height: 44px;
    transition: height 0.1s ease;
  }
  </style>  