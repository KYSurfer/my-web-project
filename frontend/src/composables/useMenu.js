import { ref } from 'vue'
import axios from 'axios'

const API_URL = 'http://localhost:5000'

export function useMenu() {
  const menu = ref([])
  const categories = ref([])
  const loading = ref(true)
  const error = ref(null)

  const fetchMenu = async () => {
    try {
      loading.value = true
      error.value = null
      const catRes = await axios.get(`${API_URL}/api/menu/categories`)
      if (catRes.data?.success) {
        categories.value = catRes.data.data
      }
      const menuRes = await axios.get(`${API_URL}/api/menu`)
      if (menuRes.data?.success) {
        menu.value = menuRes.data.data
      } else {
        throw new Error(menuRes.data?.error || 'Некорректный ответ сервера')
      }
    } catch (err) {
      error.value = err.message
      console.error('Ошибка загрузки меню:', err)
    } finally {
      loading.value = false
    }
  }

  fetchMenu()
  return { menu, categories, loading, error, fetchMenu }
}