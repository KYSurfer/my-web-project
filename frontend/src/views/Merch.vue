<template>
  <main>
    <h1 class="page-title">Магазин Bon's Burgers</h1>
    <p class="page-subtitle">Сувениры и мерч для настоящих фанатов</p>

    <div class="filters-toggle-wrapper">
      <button type="button" @click="toggleFilters" class="filters-toggle-btn">
        <span>Фильтры</span>
        <span class="toggle-icon" :class="{ 'open': filtersOpen }">▼</span>
        <span v-if="activeCount > 0" class="filters-badge">{{ activeCount }}</span>
      </button>
    </div>

    <div v-show="filtersOpen" class="filters-panel">
      <div class="filters-grid">
        <div class="filter-group">
          <label>Цена, ₽</label>
          <div class="price-row">
            <input type="number" v-model.number="draft.min" placeholder="0" min="0" :max="draft.max" class="f-input" @input="dirty = true">
            <input type="number" v-model.number="draft.max" :placeholder="globalMax" :min="draft.min" :max="globalMax" class="f-input" @input="dirty = true">
          </div>
        </div>
        <div class="filter-group">
          <label>Дата</label>
          <input type="date" v-model="draft.date" class="f-input" @input="dirty = true">
          <button v-if="draft.date" @click="draft.date = null; dirty = true" class="f-clear">✕</button>
        </div>
      </div>
      <div class="f-actions">
        <button @click="apply" class="f-btn f-apply">Применить</button>
        <button @click="reset" class="f-btn f-reset">Сброс</button>
      </div>
    </div>

    <template v-if="loading">
      <div class="grid">
        <SkeletonCard v-for="i in 10" :key="`sk-${i}`" />
      </div>
    </template>

    <div v-else-if="error" class="msg err">
      <p>{{ error }}</p>
      <button @click="fetchProducts">Повторить</button>
    </div>

    <div v-else-if="!filtered.length" class="msg">
      <p>Ничего не найдено</p>
      <button @click="reset">Сбросить</button>
    </div>

    <template v-else>
      <div class="grid">
<div v-for="item in paginatedItems" :key="item.id" class="card">
          <img 
            :src="item.image" 
            :alt="item.name" 
            class="card-img" 
            loading="lazy"
            @error="item.image = 'https://via.placeholder.com/300x260/111/f4d03f?text=No+Image'"
          >
          <h2 class="card-name">{{ item.name }}</h2>
          
          <div class="card-price">{{ item.price }} br</div>

          <div class="actions-row">
            <div 
              class="likes-counter" 
              @click="toggleLike(item.id)" 
              :class="{ clickable: auth.isAuthenticated }"
            >
              <svg 
                class="heart-icon"
                :class="{ liked: likesState[item.id] }"
                viewBox="0 0 22 22" 
                :fill="likesState[item.id] ? '#ff0000' : '#d4a84a'"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path d="M12 20H10V19H9V18H8V17H7V16H6V15H5V14H4V13H3V12H2V10H1V5H2V4H3V3H4V2H9V3H10V4H12V3H13V2H18V3H19V4H20V5H21V10H20V12H19V13H18V14H17V15H16V16H15V17H14V18H13V19H12V20M5 11V12H6V13H7V14H8V15H9V16H10V17H12V16H13V15H14V14H15V13H16V12H17V11H18V9H19V6H18V5H17V4H14V5H13V6H12V7H10V6H9V5H8V4H5V5H4V6H3V9H4V11H5Z" />
              </svg>
              <span>{{ likesCount[item.id] ?? item.likes }}</span>
            </div>
            <div 
              class="save-icon-wrapper" 
              @click="toggleCart(item.id)"
              :class="{ clickable: auth.isAuthenticated, 'in-cart': cartState[item.id] }"
              :title="auth.isAuthenticated ? (cartState[item.id] ? 'Удалить из корзины' : 'Добавить в корзину') : 'Войдите чтобы добавить'"
            >
              <svg v-if="!cartState[item.id]" class="save-icon" width="24" height="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path d="M20.4961766,5.62668182 C21.3720675,5.93447702 22,6.76890777 22,7.75 L22,17.75 C22,20.0972102 20.0972102,22 17.75,22 L7.75,22 C6.76890777,22 5.93447702,21.3720675 5.62668182,20.4961766 L7.72396188,20.4995565 L17.75,20.5 C19.2687831,20.5 20.5,19.2687831 20.5,17.75 L20.5,7.75 L20.4960194,7.69901943 L20.4961766,5.62668182 Z M17.246813,2 C18.4894537,2 19.496813,3.00735931 19.496813,4.25 L19.496813,17.246813 C19.496813,18.4894537 18.4894537,19.496813 17.246813,19.496813 L4.25,19.496813 C3.00735931,19.496813 2,18.4894537 2,17.246813 L2,4.25 C2,3.00735931 3.00735931,2 4.25,2 L17.246813,2 Z M17.246813,3.5 L4.25,3.5 C3.83578644,3.5 3.5,3.83578644 3.5,4.25 L3.5,17.246813 C3.5,17.6610266 3.83578644,17.996813 4.25,17.996813 L17.246813,17.996813 C17.6610266,17.996813 17.996813,17.6610266 17.996813,17.246813 L17.996813,4.25 C17.996813,3.83578644 17.6610266,3.5 17.246813,3.5 Z M10.75,6.75 C11.1642136,6.75 11.5,7.08578644 11.5,7.5 L11.5,10 L14,10 C14.4142136,10 14.75,10.3357864 14.75,10.75 C14.75,11.1642136 14.4142136,11.5 14,11.5 L11.5,11.5 L11.5,14 C11.5,14.4142136 11.1642136,14.75 10.75,14.75 C10.3357864,14.75 10,14.4142136 10,14 L10,11.5 L7.5,11.5 C7.08578644,11.5 6.75,11.1642136 6.75,10.75 C6.75,10.3357864 7.08578644,10 7.5,10 L10,10 L10,7.5 C10,7.08578644 10.3357864,6.75 10.75,6.75 Z" fill="#212121"/>
              </svg>
              <svg v-else class="success-icon" width="24" height="24" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
                <path d="M213.333333,3.55271368e-14 C95.51296,3.55271368e-14 3.55271368e-14,95.51296 3.55271368e-14,213.333333 C3.55271368e-14,331.153707 95.51296,426.666667 213.333333,426.666667 C331.153707,426.666667 426.666667,331.153707 426.666667,213.333333 C426.666667,95.51296 331.153707,3.55271368e-14 213.333333,3.55271368e-14 Z M213.333333,384 C119.227947,384 42.6666667,307.43872 42.6666667,213.333333 C42.6666667,119.227947 119.227947,42.6666667 213.333333,42.6666667 C307.43872,42.6666667 384,119.227947 384,213.333333 C384,307.43872 307.438933,384 213.333333,384 Z M293.669333,137.114453 L323.835947,167.281067 L192,299.66912 L112.916693,220.585813 L143.083307,190.4192 L192,239.335893 L293.669333,137.114453 Z" fill="#d4a84a"/>
              </svg>
            </div>
          </div>
          <button @click="goTo(item.id)" class="card-btn">► Подробнее</button>
        </div>
      </div>
      <div v-if="totalPages > 1" class="pagination">
        <button 
          @click="goToPage(currentPage - 1)" 
          :disabled="currentPage === 1"
          class="pagination-btn"
        >
          ◄ Назад
        </button>
        
        <span class="pagination-info">
          Страница {{ currentPage }} из {{ totalPages }}
        </span>
        
        <button 
          @click="goToPage(currentPage + 1)" 
          :disabled="currentPage === totalPages"
          class="pagination-btn"
        >
          Вперёд ►
        </button>
      </div>
    </template>
  </main>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useProducts } from '@/composables/useProducts'
import { useAuthStore } from '@/stores/auth'
import SkeletonCard from '@/components/SkeletonCard.vue'
import api from '@/plugins/axios'

const router = useRouter()
const auth = useAuthStore()
const { products, loading, error, fetchProducts } = useProducts()

const filtersOpen = ref(false)
const toggleFilters = () => { filtersOpen.value = !filtersOpen.value }

const globalMax = ref(5000)
const draft = ref({ min: 0, max: null, date: null })
const dirty = ref(false) 
const applied = ref({ min: 0, max: null, date: null })

const likesState = ref({})
const likesCount = ref({})
const cartState = ref({})

const calcMaxPrice = () => {
  if (!products.value?.length) return
  const prices = products.value.map(p => p.price).filter(p => typeof p === 'number' && p >= 0)
  if (prices.length) {
    globalMax.value = Math.max(...prices)
    if (draft.value.max === null) draft.value.max = globalMax.value
    if (applied.value.max === null) applied.value.max = globalMax.value
  }
}
watch(() => products.value, calcMaxPrice, { immediate: true })

const apply = () => {
  applied.value.min = draft.value.min ?? 0
  applied.value.max = draft.value.max ?? globalMax.value
  applied.value.date = draft.value.date
  dirty.value = false
}

const reset = () => {
  draft.value = { min: 0, max: globalMax.value, date: null }
  applied.value = { min: 0, max: globalMax.value, date: null }
  dirty.value = false
  filtersOpen.value = false
}

const activeCount = computed(() => {
  let c = 0
  if (applied.value.min > 0) c++
  if (applied.value.max !== null && applied.value.max < globalMax.value) c++
  if (applied.value.date) c++
  return c
})

const filtered = computed(() => {
  const list = products.value || []
  const { min, max, date } = applied.value
  return list.filter(p => {
    const price = p.price ?? 0
    if (price < (min ?? 0) || price > (max ?? globalMax.value)) return false
    if (date && p.created_at) {
      const pd = p.created_at.split('T')[0]
      if (pd < date) return false
    }
    return true
  })
})

const goTo = (id) => router.push(`/product/${id}`)

const loadProductStates = async () => {
  if (!auth.isAuthenticated || !auth.user?.id || !products.value?.length) return
  for (const item of products.value) {
    try {
      const likeRes = await api.get(`/products/${item.id}/like/status`, {
  params: { user_id: auth.user.id }  // ← Добавь эту строку!
})
      likesState.value[item.id] = likeRes.data.is_liked
      likesCount.value[item.id] = likeRes.data.is_liked ? (item.likes || 0) + 1 : (item.likes || 0)
      
      const cartRes = await api.get(`/cart/${item.id}/check`)
      cartState.value[item.id] = cartRes.data.in_cart
    } catch (e) {
      console.error(`Ошибка загрузки состояния для ${item.id}:`, e)
      likesCount.value[item.id] = item.likes || 0
    }
  }
}

const toggleLike = async (productId) => {
  if (!auth.isAuthenticated) { router.push('/auth/login'); return }
  try {
    const res = await api.post(`/products/${productId}/like`, { user_id: auth.user.id })
    if (res.data.success) {
      likesState.value[productId] = res.data.is_liked
      likesCount.value[productId] = res.data.likes
    }
  } catch (err) { console.error('Ошибка лайка:', err) }
}

const toggleCart = async (productId) => {
  if (!auth.isAuthenticated) { router.push('/auth/login'); return }
  try {
    if (cartState.value[productId]) {
      await api.delete(`/cart/${productId}`)
      cartState.value[productId] = false
    } else {
      await api.post('/cart', { product_id: productId, quantity: 1 })
      cartState.value[productId] = true
    }
  } catch (err) {
    console.error('Ошибка корзины:', err)
    cartState.value[productId] = !cartState.value[productId]
  }
}

watch(() => auth.isAuthenticated, (val) => { if (val) loadProductStates() })
watch(() => products.value, () => { if (auth.isAuthenticated) loadProductStates() }, { deep: true })

onMounted(() => {
  if (auth.isAuthenticated) loadProductStates()
})

// 🔥 ПАГИНАЦИЯ
const currentPage = ref(1)
const itemsPerPage = 9 // 3 ряда × 3 колонки

// Вычисляем товары для текущей страницы
const paginatedItems = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filtered.value.slice(start, end)
})

// Общее количество страниц
const totalPages = computed(() => 
  Math.ceil(filtered.value.length / itemsPerPage)
)

// Переход на страницу
const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    window.scrollTo({ top: 0, behavior: 'smooth' }) // Прокрутка вверх
  }
}

// Сброс страницы при изменении фильтров
watch(() => [applied.value.min, applied.value.max, applied.value.date], () => {
  currentPage.value = 1
})
</script>

<style scoped src="@/assets/styles/views/Merch.css">

</style>