import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router/index.js'
import './assets/styles/global.css'
import { useAuthStore } from './stores/auth'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

const authStore = useAuthStore(pinia)
const token = localStorage.getItem('authToken')
const userStr = localStorage.getItem('user')

if (token && userStr) {
  authStore.token = token
  authStore.user = JSON.parse(userStr)
}

app.mount('#app')