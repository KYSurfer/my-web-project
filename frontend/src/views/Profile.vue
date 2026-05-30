<template>
  <main>
    <h1 class="page-title">Личный кабинет</h1>
    <p class="page-subtitle">Управление аккаунтом и заказами</p>

    <div v-if="loading" class="main-content__loading">
      <div class="spinner"></div>
      <p>Загрузка профиля...</p>
    </div>

    <div v-else-if="error" class="main-content__error">
      <p>{{ error }}</p>
      <button @click="initProfile" class="retry-btn">Повторить попытку</button>
    </div>

    <div v-else class="profile-container">
      
      <div class="main-content__block profile-block">
        
        <div class="profile-header">
          <div class="profile-avatar-wrapper">
            <img 
              :src="avatarUrl" 
              :alt="user?.username" 
              class="profile-avatar"
              @error="avatarUrl = '/static/images/default-avatar.jpg'"
            >
          </div>
          
          <div class="profile-info">
            <h2 class="profile-name">{{ user?.username || 'Пользователь' }}</h2>
            <p class="profile-email">{{ user?.email }}</p>
            <span class="profile-role" :class="user?.role">
              {{ user?.role === 'admin' ? 'Администратор' : 'Зарегистрирован' }}
            </span>
          </div>
        </div>

        <div class="profile-divider"></div>

        <!-- <div class="profile-stats">
          <div class="stat-box">
            <span class="stat-num">{{ cartItems.length }}</span>
            <span class="stat-label">Товаров в корзине</span>
          </div>
          <div class="stat-box">
            <span class="stat-num">{{ purchasedCount }}</span>
            <span class="stat-label">Куплено товаров</span>
          </div>
        </div> -->

        <button @click="logout" class="btn btn-logout">Выйти из аккаунта</button>
      </div>

      <!-- <div class="main-content__block cart-block">
        <h2 class="cart-title">Ваша корзина</h2>

        <div v-if="cartLoading" class="cart-loading">
          <div class="spinner-sm"></div>
          <p>Загрузка товаров...</p>
        </div>

        <div v-else-if="cartItems.length === 0" class="cart-empty">
          <p>Корзина пуста</p>
          <router-link to="/menu" class="btn btn-secondary">Перейти в меню</router-link>
        </div>

        <div v-else class="cart-list">
          <div v-for="item in cartItems" :key="item.cart_id" class="cart-item">
            <img :src="item.image_url" :alt="item.name" class="cart-item__img">
            <div class="cart-item__info">
              <h3 class="cart-item__name">{{ item.name }}</h3>
              <p class="cart-item__category">{{ item.category }}</p>
              <div class="cart-item__price-row">
                <span class="cart-item__price">{{ item.price }} ₽</span>
                <span class="cart-item__qty">× {{ item.quantity }} шт.</span>
              </div>
              <p class="cart-item__subtotal">Итого: <strong>{{ item.price * item.quantity }} ₽</strong></p>
            </div>
          </div>

          <div class="cart-total">
            <span>Общая сумма заказа:</span>
            <strong class="cart-total-sum">{{ cartTotal }} ₽</strong>
          </div>

          <button @click="checkout" class="btn btn-cart">►Оформить заказ</button>
        </div>
      </div> -->

      <div class="main-content__block settings-block">
        <h2 class="settings-title">Настройки интерфейса</h2>
        
        <div class="setting-item">
          <div class="setting-info">
            <span class="setting-label">Эффект перехода</span>
          </div>
          
          <button 
            @click="toggleFx" 
            class="retro-switch"
            :class="{ 'switch-on': enableFx }"
            :aria-pressed="enableFx"
            :title="enableFx ? 'Выключить эффект' : 'Включить эффект'"
          >
            <span class="switch-indicator"></span>
            {{ enableFx ? 'ВКЛ' : 'ВЫКЛ' }}
          </button>
        </div>
      </div>

    </div>
  </main>
</template>

<script>
import api from '@/plugins/axios'
import { useSettingsStore } from '@/stores/settings'

export default {
  name: 'Profile',
  data() {
    return {
      user: null,
      cartItems: [],
      purchasedCount: 0,
      loading: true,
      error: null,
      cartLoading: true,
      avatarPool: [
        '/static/images/bon-frontpage.jpg',
        '/static/images/banny-frontpage.png',
        '/static/images/Sha-frontpage.jpg',
        '/static/images/boozoo-frontpage.jpg',
        '/static/images/billy-frontpage.jpg',
        '/static/images/jack-walten-info.jpg',
        '/static/images/kranken-info.webp',
        '/static/images/susan-info.webp',
        '/static/images/felix-info.jpg',
        '/static/images/default-avatar.jpg'
      ]
    }
  },
  computed: {
    cartTotal() {
      return this.cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0)
    },
    avatarUrl() {
      if (!this.user?.email) return this.avatarPool[0]
      const index = this.user.email.charCodeAt(0) % this.avatarPool.length
      return this.avatarPool[index]
    },
    enableFx() {
      const settings = useSettingsStore()
      return settings.enableFx
    }
  },
  methods: {
    toggleFx() {
      const settings = useSettingsStore()
      settings.toggleFx()
    },
    
    async initProfile() {
      this.loading = true
      this.error = null
      try {
        this.user = JSON.parse(localStorage.getItem('user') || '{}')
      } catch (e) {
        this.error = 'Не удалось загрузить данные профиля'
      } finally {
        this.loading = false
        this.fetchCart()
      }
    },
    async fetchCart() {
      this.cartLoading = true
      try {
        const res = await api.get('/cart')
        if (res.data?.success) {
          this.cartItems = res.data.data
        }
      } catch (e) {
        console.error('Ошибка загрузки корзины:', e)
      } finally {
        this.cartLoading = false
      }
    },
    logout() {
      localStorage.removeItem('authToken')
      localStorage.removeItem('user')
      this.$router.replace('/')
    },
    checkout() {
      alert('Заказ оформлен!')
    }
  },
  mounted() {
    this.initProfile()
  }
}
</script>

<style scoped src="@/assets/styles/views/Profile.css">

</style>