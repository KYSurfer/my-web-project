import { ref } from 'vue'
import axios from 'axios'

const API_URL = 'http://localhost:5000'

export function useProducts() {
  const products = ref([])
  const loading = ref(true)
  const error = ref(null)

  const fetchProducts = async () => {
    try {
      loading.value = true
      error.value = null
      const response = await axios.get(`${API_URL}/api/products`)
      
      if (response.data?.success) {
        products.value = response.data.data
      } else {
        throw new Error(response.data?.error || 'Некорректный ответ сервера')
      }
    } catch (err) {
      error.value = err.message
      console.error('Ошибка загрузки товаров:', err)
    } finally {
      loading.value = false
    }
  }

  fetchProducts()
  return { products, loading, error, fetchProducts }
}