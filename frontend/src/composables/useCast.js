import { ref } from 'vue'
import axios from 'axios'

const API_URL = 'http://localhost:5000'

export function useCast() {
  const cast = ref([])
  const loading = ref(true)
  const error = ref(null)

  const fetchCast = async () => {
    try {
      loading.value = true
      error.value = null
      const response = await axios.get(`${API_URL}/api/cast`)
      
      if (response.data?.success && Array.isArray(response.data.data)) {
        cast.value = response.data.data
      } else {
        throw new Error('Некорректный ответ сервера')
      }
    } catch (err) {
      error.value = err.message
      console.error('Ошибка загрузки команды:', err)
    } finally {
      loading.value = false
    }
  }

  fetchCast()

  return {
    cast,
    loading,
    error,
    fetchCast
  }
}