<template>
  <main class="main-content">
    <div class="main-content__welcome">
      <div>
        <h1 class="main-content__welcome-ru">Добро пожаловать в</h1>
        <h1 class="main-content__welcome-eng">Bon's Burgers</h1>
        <p class="main-content__welcome-par">В наших ресторанах не только много вкусной еды, но и множество развлечений, которые вам не найти нигде на свете. Bon's Burgers — место, где еда — это только начало приключений.</p>
      </div>
      
      <div class="main-content__welcome-img-wrapper">
        <template v-if="welcomeLoading">
          <div class="skeleton-welcome-image"></div>
        </template>
        
        <template v-else-if="welcomeError">
          <div class="welcome-image-error">
            <p>Не удалось загрузить изображение</p>
          </div>
        </template>
        
        <template v-else>
          <img 
            :src="welcomeImage" 
            alt="Бон" 
            class="main-content__welcome-img"
            @error="handleImageError"
          >
        </template>
      </div>
    </div>

    <h1 class="main-content__important-txt">Встречайте наших звезд</h1>
    <p class="main-content__animatronic-desc">Аниматроники ресторана Bon's Burgers!</p>
    <div class="main-content__block-second">
      <div class="main-content__b">
        
        <template v-if="animatronicsLoading">
          <SkeletonCard v-for="i in 3" :key="`sk-ani-${i}`" />
        </template>

        <template v-else-if="animatronicsError">
          <div class="main-content__error">
            <p>{{ animatronicsError }}</p>
            <button @click="fetchAnimatronics">Попробовать снова</button>
          </div>
        </template>
        <template v-else>
          <AnimatronicCard v-for="char in animatronics" :key="char.id" :animatronic="char"/>
        </template>
      </div>
      <div class="button-center">
        <router-link to="/stars">
          <button class="main-content__meet-all">★Встретить их всех★</button>
        </router-link>
      </div>
    </div>

    <div class="main-content__third">
      <h1 class="main-content__important-txt">Выбор покупателей</h1>
      <p class="main-content__animatronic-desc">Топ-3 товара по версии наших гостей!</p>
      
      <template v-if="loading">
        <div class="main-content__b">
          <SkeletonCard v-for="i in 3" :key="`sk-prod-${i}`" />
        </div>
      </template>

      <div v-else-if="productsError" class="main-content__error">
        <p>{{ productsError }}</p>
        <button @click="fetchBestProducts">Попробовать снова</button>
      </div>

<template v-else-if="bestProducts.length > 0">
  <div class="main-content__b">
    <ProductCard 
      v-for="product in bestProducts" 
      :key="product.id" 
      :product="product"
    />
  </div>
</template>

      <div v-else class="main-content__no-products">
        <p>Пока нет товаров с лайками</p>
      </div>
    </div>
    
    <div class="button-center-low">
      <router-link to="/menu">
        <button class="main-content__meet-all">★Посмотреть всё меню★</button>
      </router-link>
    </div>
  </main>
</template>

<script setup>
import AnimatronicCard from '@/components/AnimatronicCard.vue'
import SkeletonCard from '@/components/SkeletonCard.vue'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAnimatronics } from '@/composables/useAnimatronics'
import ProductCard from '@/components/BestProductCard.vue'

const router = useRouter()

const bestProducts = ref([])
const loading = ref(true)
const productsError = ref(null)

const welcomeImage = ref(null)
const welcomeLoading = ref(true)
const welcomeError = ref(null)

const { 
  animatronics, 
  loading: animatronicsLoading, 
  error: animatronicsError, 
  fetchAnimatronics 
} = useAnimatronics()

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

const fetchWelcomeImage = async () => {
  welcomeLoading.value = true
  welcomeError.value = null
  try {
    const response = await axios.get(`${API_BASE}/home/welcome`)
    welcomeImage.value = response.data.imageUrl || response.data.image || response.data
  } catch (error) {
    welcomeError.value = 'Не удалось загрузить изображение'
    console.error('Ошибка загрузки welcome-изображения:', error)
  } finally {
    welcomeLoading.value = false
  }
}

const handleImageError = () => {
  welcomeError.value = 'Изображение не найдено'
  welcomeLoading.value = false
}

const fetchBestProducts = async () => {
  loading.value = true
  productsError.value = null
  try {
    const response = await axios.get(`${API_BASE}/products/best`)
    if (response.data?.success) {
      bestProducts.value = response.data.data
    } else {
      productsError.value = 'Некорректный ответ сервера'
    }
  } catch (error) {
    productsError.value = error.response?.data?.message || 'Не удалось загрузить товары'
    console.error('Ошибка загрузки товаров:', error)
  } finally {
    loading.value = false
  }
}

const goToProduct = (id) => {
  router.push(`/product/${id}`)
}

onMounted(() => {
  fetchWelcomeImage()
  fetchBestProducts()
})
</script>

<style scoped src="@/assets/styles/views/Home.css">

</style>