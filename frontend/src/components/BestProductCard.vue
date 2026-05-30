<template>
  <div class="main-content__block best-product-card">
    <img :src="product.image" :alt="product.name" class="main-content__block-img">
    <h1 class="main-content__block-name">{{ product.name }}</h1>
    <h3 class="main-content__block-alias">►►{{ product.category }}</h3>
    <p class="main-content__block-desc">{{ product.description }}</p>
    
    <div class="actions-row">
      <div class="likes-counter" @click="toggleLike" :class="{ clickable: auth.isAuthenticated }">
        <svg 
          class="heart-icon"
          :class="{ liked: isLiked }"
          viewBox="0 0 22 22" 
          :fill="isLiked ? '#ff0000' : '#d4a84a'"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path d="M12 20H10V19H9V18H8V17H7V16H6V15H5V14H4V13H3V12H2V10H1V5H2V4H3V3H4V2H9V3H10V4H12V3H13V2H18V3H19V4H20V5H21V10H20V12H19V13H18V14H17V15H16V16H15V17H14V18H13V19H12V20M5 11V12H6V13H7V14H8V15H9V16H10V17H12V16H13V15H14V14H15V13H16V12H17V11H18V9H19V6H18V5H17V4H14V5H13V6H12V7H10V6H9V5H8V4H5V5H4V6H3V9H4V11H5Z" />
        </svg>
        <span>{{ likesCount }}</span>
      </div>

      <div 
        class="save-icon-wrapper" 
        @click="toggleCart"
        :class="{ clickable: auth.isAuthenticated }"
        :title="auth.isAuthenticated ? (isInCart ? 'Удалить из корзины' : 'Добавить в корзину') : 'Войдите чтобы добавить'"
      >
        <svg 
          v-if="!isInCart"
          class="save-icon"
          width="24" 
          height="24" 
          viewBox="0 0 24 24" 
          xmlns="http://www.w3.org/2000/svg"
        >
          <path 
            d="M20.4961766,5.62668182 C21.3720675,5.93447702 22,6.76890777 22,7.75 L22,17.75 C22,20.0972102 20.0972102,22 17.75,22 L7.75,22 C6.76890777,22 5.93447702,21.3720675 5.62668182,20.4961766 L7.72396188,20.4995565 L17.75,20.5 C19.2687831,20.5 20.5,19.2687831 20.5,17.75 L20.5,7.75 L20.4960194,7.69901943 L20.4961766,5.62668182 Z M17.246813,2 C18.4894537,2 19.496813,3.00735931 19.496813,4.25 L19.496813,17.246813 C19.496813,18.4894537 18.4894537,19.496813 17.246813,19.496813 L4.25,19.496813 C3.00735931,19.496813 2,18.4894537 2,17.246813 L2,4.25 C2,3.00735931 3.00735931,2 4.25,2 L17.246813,2 Z M17.246813,3.5 L4.25,3.5 C3.83578644,3.5 3.5,3.83578644 3.5,4.25 L3.5,17.246813 C3.5,17.6610266 3.83578644,17.996813 4.25,17.996813 L17.246813,17.996813 C17.6610266,17.996813 17.996813,17.6610266 17.996813,17.246813 L17.996813,4.25 C17.996813,3.83578644 17.6610266,3.5 17.246813,3.5 Z M10.75,6.75 C11.1642136,6.75 11.5,7.08578644 11.5,7.5 L11.5,10 L14,10 C14.4142136,10 14.75,10.3357864 14.75,10.75 C14.75,11.1642136 14.4142136,11.5 14,11.5 L11.5,11.5 L11.5,14 C11.5,14.4142136 11.1642136,14.75 10.75,14.75 C10.3357864,14.75 10,14.4142136 10,14 L10,11.5 L7.5,11.5 C7.08578644,11.5 6.75,11.1642136 6.75,10.75 C6.75,10.3357864 7.08578644,10 7.5,10 L10,10 L10,7.5 C10,7.08578644 10.3357864,6.75 10.75,6.75 Z" 
            fill="#212121"
          />
        </svg>

        <svg 
          v-else
          class="success-icon"
          width="24" 
          height="24" 
          viewBox="0 0 512 512" 
          xmlns="http://www.w3.org/2000/svg"
        >
          <path 
            d="M213.333333,3.55271368e-14 C95.51296,3.55271368e-14 3.55271368e-14,95.51296 3.55271368e-14,213.333333 C3.55271368e-14,331.153707 95.51296,426.666667 213.333333,426.666667 C331.153707,426.666667 426.666667,331.153707 426.666667,213.333333 C426.666667,95.51296 331.153707,3.55271368e-14 213.333333,3.55271368e-14 Z M213.333333,384 C119.227947,384 42.6666667,307.43872 42.6666667,213.333333 C42.6666667,119.227947 119.227947,42.6666667 213.333333,42.6666667 C307.43872,42.6666667 384,119.227947 384,213.333333 C384,307.43872 307.438933,384 213.333333,384 Z M293.669333,137.114453 L323.835947,167.281067 L192,299.66912 L112.916693,220.585813 L143.083307,190.4192 L192,239.335893 L293.669333,137.114453 Z" 
            fill="#d4a84a"
          />
        </svg>
      </div>
    </div>

    <button @click="goToProduct" class="product-card__btn">Подробнее</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/plugins/axios'

const props = defineProps({
  product: { type: Object, required: true }
})
const emit = defineEmits(['likes-updated', 'cart-updated']) 

const router = useRouter()
const auth = useAuthStore()

const isLiked = ref(false)
const likesCount = ref(props.product.likes || 0)
const isInCart = ref(false) 

onMounted(async () => {
  likesCount.value = props.product.likes || 0
  
  if (!auth.isAuthenticated || !auth.user?.id) return
  
  try {
    const likeRes = await api.get(`/products/${props.product.id}/like/status`, {
      params: { user_id: auth.user.id }
    })
    isLiked.value = likeRes.data.is_liked
    
    const cartRes = await api.get(`/cart/${props.product.id}/check`)
    isInCart.value = cartRes.data.in_cart
  } catch (e) {
    console.error('Ошибка загрузки состояния:', e)
  }
})

const toggleLike = async () => {
  if (!auth.isAuthenticated) {
    router.push('/auth/login')
    return
  }
  
  try {
    const res = await api.post(`/products/${props.product.id}/like`, {
      user_id: auth.user.id
    })
    
    if (res.data.success) {
      isLiked.value = res.data.is_liked
      likesCount.value = res.data.likes
      emit('likes-updated', { 
        productId: props.product.id, 
        isLiked: isLiked.value 
      })
    }
  } catch (error) {
    console.error('Ошибка при лайке:', error)
  }
}

const toggleCart = async () => {
  if (!auth.isAuthenticated) {
    router.push('/auth/login')
    return
  }
  
  try {
    if (isInCart.value) {
      await api.delete(`/cart/${props.product.id}`)
      isInCart.value = false
      console.log('Удалено из корзины')
    } else {
      await api.post('/cart', {
        product_id: props.product.id,
        quantity: 1
      })
      isInCart.value = true
      console.log('Добавлено в корзину')
    }
    
    emit('cart-updated', { 
      productId: props.product.id, 
      isInCart: isInCart.value 
    })
  } catch (error) {
    console.error('Ошибка корзины:', error)
    isInCart.value = !isInCart.value // откат
  }
}

const goToProduct = () => {
  router.push(`/product/${props.product.id}`)
}
</script>

<style scoped src="@/assets/styles/components/BestProductCard.css">

</style>