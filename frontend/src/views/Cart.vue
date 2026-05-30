<template>
  <main class="cart-page">
    <h1 class="page-title"> Ваша корзина</h1>
    
    <div v-if="loading" class="state-message">
      <div class="spinner"></div>
      <p>Загрузка корзины...</p>
    </div>

    <div v-else-if="error" class="state-message error">
      <p>{{ error }}</p>
      <router-link to="/menu" class="retry-btn">Перейти в меню</router-link>
    </div>

    <div v-else-if="cartItems.length === 0" class="state-message empty">
      <p>Ваша корзина пуста</p>
      
    </div>

    <div v-else class="cart-container">
      <div class="cart-list">
        <div v-for="item in cartItems" :key="item.id" class="cart-item">
          <img :src="item.image" :alt="item.name" class="item-img" loading="lazy">
          
          <div class="item-info">
            <h3 class="item-name">{{ item.name }}</h3>
            <p class="item-price">{{ item.price }} ₽</p>
          </div>

          <div class="item-controls">
            <button @click="updateQuantity(item, -1)" class="qty-btn" :disabled="item.quantity <= 1">−</button>
            <span class="qty-value">{{ item.quantity }}</span>
            <button @click="updateQuantity(item, 1)" class="qty-btn">+</button>
          </div>

          <!-- <button @click="removeItem(item.id)" class="remove-btn" title="Удалить">✕</button> -->
           <button @click="removeItem(item)" class="remove-btn">✕</button>
        </div>
      </div>

      <div class="cart-summary">
        <div class="summary-row">
          <span>Товары ({{ totalQty }}):</span>
          <span>{{ subtotal }} ₽</span>
        </div>
        <div class="summary-row">
          <span>Доставка:</span>
          <span>{{ deliveryCost }} ₽</span>
        </div>
        <div v-if="discount > 0" class="summary-row discount">
          <span>Скидка:</span>
          <span>−{{ discount }} ₽</span>
        </div>
        
        <div class="summary-row total">
          <span>Итого:</span>
          <strong>{{ finalTotal }} ₽</strong>
        </div>

        <div class="promo-section">
          <input 
            v-model="promoCode" 
            placeholder="Промокод" 
            class="promo-input"
            @input="applyPromo"
          >
        </div>

        <button @click="checkout" class="checkout-btn" :disabled="isCheckingOut || cartItems.length === 0">
          {{ isCheckingOut ? 'Оформление...' : '► Оформить заказ' }}
        </button>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/plugins/axios'

const router = useRouter()
const cartItems = ref([])
const loading = ref(true)
const error = ref(null)
const promoCode = ref('')
const discount = ref(0)
const isCheckingOut = ref(false)

const fetchCart = async () => {
  try {
    loading.value = true
    error.value = null
    const res = await api.get('/cart')
    cartItems.value = res.data.items || res.data || []
  } catch (e) {
    console.error('Ошибка загрузки корзины:', e)
    cartItems.value = [
      { id: 1, name: 'Бон-Бургер', price: 299, quantity: 2, image: 'http://localhost:5000/static/images/bon-burger.jpg' },
      { id: 3, name: 'Картофель фри', price: 149, quantity: 1, image: 'http://localhost:5000/static/images/fries.jpg' }
    ]
  } finally {
    loading.value = false
  }
}

const updateQuantity = async (item, delta) => {
  const newQty = item.quantity + delta
  if (newQty < 1) return
  
  try {
    item.quantity = newQty
    await api.put(`/cart/${item.id}`, { quantity: newQty })
  } catch (e) {
    console.error('Не удалось обновить количество:', e)
    fetchCart()
  }
}

const removeItem = async (item) => {
  try {
    // 🔥 Отправляем product_id, а не cart_id
    await api.delete(`/cart/${item.product_id}`)
    
    // 🔥 Фильтруем по product_id
    cartItems.value = cartItems.value.filter(i => i.product_id !== item.product_id)
  } catch (e) {
    console.error('Ошибка удаления:', e)
    // 🔥 Показываем ошибку пользователю
    error.value = 'Не удалось удалить товар'
  }
}

const applyPromo = () => {
  const code = promoCode.value.toUpperCase().trim()
  if (code === 'BONUS10') {
    discount.value = Math.round(subtotal.value * 0.1)
  } else if (code === 'VIP20') {
    discount.value = Math.round(subtotal.value * 0.2)
  } else {
    discount.value = 0
  }
}

const checkout = async () => {
  if (isCheckingOut.value || cartItems.value.length === 0) return
  isCheckingOut.value = true
  
  try {
    // 🔥 Получаем токен
    const token = localStorage.getItem('authToken')
    
    // 🔥 Проверяем, авторизован ли пользователь
    if (!token) {
      error.value = 'Сначала войдите в аккаунт'
      router.push('/auth/login')
      return
    }

    // 🔥 Формируем payload
    const orderPayload = {
      items: cartItems.value.map(i => ({ 
        product_id: i.id,      
        quantity: i.quantity 
      }))
    }
    
    if (promoCode.value?.trim()) {
      orderPayload.promoCode = promoCode.value.toUpperCase().trim()
    }

    console.log(' Отправляем заказ:', orderPayload)
    
    const res = await api.post('/orders', orderPayload, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    
    console.log('✅ Заказ оформлен:', res.data)
    cartItems.value = []
    router.push('/profile/orders')
    
  } catch (e) {
    console.error('❌ Ошибка заказа:', {
      status: e.response?.status,
      data: e.response?.data
    })
    error.value = e.response?.data?.error || 'Не удалось оформить заказ'
  } finally {
    isCheckingOut.value = false
  }
}

const subtotal = computed(() => 
  cartItems.value.reduce((sum, item) => sum + item.price * item.quantity, 0)
)
const totalQty = computed(() => 
  cartItems.value.reduce((sum, item) => sum + item.quantity, 0)
)
const deliveryCost = computed(() => subtotal.value >= 1000 ? 0 : 150)
const finalTotal = computed(() => subtotal.value + deliveryCost.value - discount.value)

onMounted(fetchCart)
</script>

<style scoped src="@/assets/styles/views/Cart.css">

</style>