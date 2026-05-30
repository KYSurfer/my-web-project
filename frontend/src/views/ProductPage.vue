<template>
  <main class="product-page">
    <template v-if="loading">
      <div class="loading">
        <div class="spinner"></div>
        <p>Загрузка...</p>
      </div>
    </template>

    <div v-else-if="error" class="error-message">
      <p>{{ error }}</p>
      <router-link to="/merch" class="back-btn">◄ Вернуться к товарам</router-link>
    </div>

    <div v-else-if="product" class="product-container">
      <div class="product-image-section">
        <img 
          :src="product.image" 
          :alt="product.name" 
          class="product-main-img"
        >
      </div>

      <div class="product-info-section">
        <h1 class="product-title">{{ product.name }}</h1>
        
        <div class="product-meta">
          <span class="product-category">{{ product.category }}</span>
          <span class="product-price">{{ product.price }} ₽</span>
        </div>

        <div class="product-description">
          <h3>Описание</h3>
          <p>{{ product.description || 'Описание отсутствует' }}</p>
        </div>

        <div class="product-stats">
          <div class="stat-item">
            <span class="stat-icon">❤️</span>
            <span class="stat-value">{{ product.likes }} лайков</span>
          </div>
          <div class="stat-item">
            <span class="stat-icon">👁️</span>
            <span class="stat-value">{{ product.views || 0 }} просмотров</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">В наличии: {{ product.stock }}</span>
          </div>
        </div>

        <div class="product-actions">
          <button @click="addToCart" class="btn-add-cart" :disabled="product.stock === 0">
            {{ product.stock > 0 ? ' Добавить в корзину' : ' Нет в наличии' }}
          </button>
          <button @click="$router.back()" class="btn-back">← Назад</button>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/plugins/axios'

const route = useRoute()
const product = ref(null)
const loading = ref(true)
const error = ref(null)

const fetchProduct = async () => {
  try {
    loading.value = true
    error.value = null
    const res = await api.get(`/products/${route.params.id}`)

    if (res.data.success) {
      product.value = res.data.data
      await api.post(`/api/products/${route.params.id}/view`).catch(() => {})
    } else {
      error.value = res.data.error || 'Товар не найден'
    }
  } catch (e) {
    console.error('❌ Ошибка загрузки:', e)
    error.value = e.response?.status === 404 
      ? 'Товар не найден в базе' 
      : 'Не удалось загрузить товар'
  } finally {
    loading.value = false
  }
}

const addToCart = async () => {
  if (!product.value) {
    alert('❌ Товар не загружен')
    return
  }
  
  const token = localStorage.getItem('authToken')
  if (!token) {
    alert('⚠️ Сначала войдите в аккаунт')
    router.push('/auth/login')
    return
  }
  
  try {
    console.log('Отправляю запрос на добавление в корзину...')
    
    const res = await api.post('/cart', {
      product_id: product.value.id,
      quantity: 1
    })
    
    console.log('Ответ от сервера:', res.data)
    
    if (res.data.success) {
      alert(`"${product.value.name}" добавлен в корзину!`)
    } else {
      alert(`Ошибка: ${res.data.error || 'Неизвестная ошибка'}`)
    }
    
  } catch (e) {
    console.error('❌ Ошибка добавления в корзину:', {
      status: e.response?.status,
      data: e.response?.data,
      url: e.config?.url
    })
    
    if (e.response?.status === 401) {
      alert('Session expired. Пожалуйста, войдите снова.')
      localStorage.removeItem('authToken')
      localStorage.removeItem('user')
      router.push('/auth/login')
    } else if (e.response?.status === 404) {
      alert(' Эндпоинт корзины не найден на сервере')
    } else {
      alert('Не удалось добавить товар. Проверьте консоль для деталей.')
    }
  }
}

onMounted(fetchProduct)
</script>

<style scoped src="@/assets/styles/views/ProductPage.css">

</style>