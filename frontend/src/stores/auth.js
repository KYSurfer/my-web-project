import { defineStore } from 'pinia'
import api from '@/plugins/axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,          // 🔥 Инициализируем пустым, main.js заполнит
    token: null,         // 🔥 Инициализируем пустым, main.js заполнит
    isLoading: false,
    error: null
  }),

  getters: {
    userName: (s) => s.user?.name || s.user?.username || 'Гость',
    // isAuthenticated вычисляется автоматически на основе token
    isAuthenticated: (s) => !!s.token 
  },

  actions: {
    async checkAuth() {
      if (!this.token) return
      try {
        this.isLoading = true
        // Проверка валидности токена на сервере (опционально)
        const res = await api.get('/auth/me') 
        this.user = res.data.user
        localStorage.setItem('user', JSON.stringify(res.data.user)) 
      } catch {
        this.logout()
      } finally {
        this.isLoading = false
      }
    },

    async login(credentials) {
      this.isLoading = true
      this.error = null
      try {
        const res = await api.post('/auth/login', credentials)
        this.token = res.data.token
        this.user = res.data.user
        
        // 🔥 ВАЖНО: Используем 'authToken', чтобы совпадало с main.js и router
        localStorage.setItem('authToken', this.token)
        localStorage.setItem('user', JSON.stringify(res.data.user)) 
      } catch (e) {
        this.error = e.response?.data?.message || 'Ошибка входа'
        throw e
      } finally {
        this.isLoading = false
      }
    },

    logout() {
      this.user = null
      this.token = null
      this.error = null
      // 🔥 ВАЖНО: Чистим 'authToken'
      localStorage.removeItem('authToken')
      localStorage.removeItem('user')
    }
  }
})