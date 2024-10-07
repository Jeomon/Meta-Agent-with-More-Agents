import { createApp } from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import './assets/index.css'
import axios from 'axios'

axios.defaults.baseURL='http://127.0.0.1:8000'
axios.defaults.headers.common['Content-Type']='application/json'
axios.defaults.headers.common['Access-Control-Allow-Origin']='http://127.0.0.1:8000'
createApp(App).use(store).use(router).mount('#app')
