import './assets/index.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'

axios.defaults.baseURL='http://localhost:8000/'
axios.defaults.headers.common['Content-Type']='application/json'
axios.defaults.headers.common['Access-Control-Allow-Origin']='http://localhost:8000'

const app = createApp(App)
app.use(router).use(store)
app.mount('#app')
