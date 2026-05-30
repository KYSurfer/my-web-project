import { ref } from 'vue'
import axios from 'axios'

const API_URL = 'http://localhost:5000'

export function useCharacters() {
  const characters = ref([])
  const loading = ref(true)
  const error = ref(null)

  const fetchCharacters = async () => {
    try {
      loading.value = true
      error.value = null
      
      const response = await axios.get(`${API_URL}/api/characters`)
      
      if (response.data.success) {
        characters.value = response.data.data
      } else {
        throw new Error('Некорректный ответ сервера')
      }
    } catch (err) {
      error.value = err.message
      console.error('Ошибка загрузки персонажей:', err)
    } finally {
      loading.value = false
    }
  }

  fetchCharacters()

  return {
    characters,
    loading,
    error,
    fetchCharacters
  }
}