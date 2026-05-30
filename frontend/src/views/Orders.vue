<template>
  <main class="orders-page">
    <h1 class="page-title">История заказов</h1>
    
    <div v-if="loading" class="state-message">
      <div class="spinner"></div>
      <p>Загрузка заказов...</p>
    </div>

    <div v-else-if="error" class="state-message error">
      <p>{{ error }}</p>
    </div>

    <div v-else-if="orders.length === 0" class="state-message">
      <p>У вас пока нет заказов</p>
      <router-link to="/menu" class="order-btn">Перейти в меню</router-link>
    </div>

    <div v-else>
      <div class="orders-filter">
        <select v-model="statusFilter" @change="applyFilter">
          <option value="all">Все заказы</option>
          <option value="pending">В обработке</option>
          <option value="completed">Завершён</option>
          <option value="cancelled">Отменён</option>
        </select>
      </div>

      <div class="orders-list">
        <div v-for="order in filteredOrders" :key="order.id" class="order-card">
          <div class="order-header">
            <span class="order-id">Заказ {{ order.id }}</span>
            <span class="order-date">{{ formatDate(order.created_at) }}</span>
            <span class="order-status" :class="order.status">{{ getStatusLabel(order.status) }}</span>
          </div>
          
          <div class="order-items">
            <div v-for="item in order.items" :key="item.id" class="order-item">
              <img :src="item.image" :alt="item.name" class="item-img" loading="lazy">
              <div class="item-info">
                <span class="item-name">{{ item.name }}</span>
                <span class="item-qty">×{{ item.quantity }}</span>
              </div>
              <span class="item-price">{{ (item.price * item.quantity).toFixed(2) }} ₽</span>
            </div>
          </div>

          <div class="order-footer">
            <span class="order-total">Итого: <strong>{{ order.total }} ₽</strong></span>
            <button class="order-btn-sm" @click="reorder(order)">Повторить</button>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/plugins/axios'

const router = useRouter()
const orders = ref([])
const statusFilter = ref('all')
const loading = ref(true)
const error = ref(null)

const fetchOrders = async () => {
  try {
    loading.value = true
    error.value = null
    const res = await api.get('/orders') 
    orders.value = res.data.data || res.data.orders || res.data || []
  } catch (e) {
    console.error('Ошибка загрузки истории заказов:', e)
    
    if (e.response?.status === 401) {
      error.value = 'Требуется авторизация'
      router.push('/auth/login')
    } else if (e.response?.status === 404) {
      error.value = 'Эндпоинт не найден на сервере'
    } else if (e.response?.status === 500) {
      error.value = 'Ошибка сервера. Попробуйте позже'
    } else {
      error.value = 'Не удалось загрузить заказы. Проверьте соединение'
    }
  } finally {
    loading.value = false
  }
}

const filteredOrders = computed(() => {
  if (statusFilter.value === 'all') return orders.value
  return orders.value.filter(o => o.status === statusFilter.value)
})

const applyFilter = () => {}

const reorder = async (order) => {
  try {
    for (const item of order.items) {
      await api.post('/cart', {
        product_id: item.id,
        quantity: item.quantity
      })
    }
    router.push('/profile/cart')
  } catch (e) {
    console.error('Не удалось повторить заказ:', e)
    alert('Не удалось добавить товары в корзину')
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getStatusLabel = (status) => {
  const map = { 
    pending: 'В обработке', 
    completed: 'Завершён', 
    cancelled: 'Отменён' 
  }
  return map[status] || status
}

onMounted(fetchOrders)
</script>

<style scoped src="@/assets/styles/views/Orders.css">

</style>