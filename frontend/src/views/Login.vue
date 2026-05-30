<template>
    <main class="login">
        <router-link to="/" class="login__link">
            <div class="login__back">
                <span class="login__back-txt">◄ На главную</span>  
            </div>
        </router-link>
        
        <div class="login__form">
            <div class="login__form-info">
                <div class="login__form-info-head">
                    <h1 class="login__form-info-header">Вход в аккаунт</h1>
                    <h3 class="login__form-info-undertext">Мы тебя ждали!</h3>
                </div>
                
                <form @submit.prevent="handleSubmit">
                    <div class="login__form-info-email">
                        <label class="login__form-info-email-txt">Email</label>
                        <input 
                            type="email" 
                            placeholder="►► Email" 
                            v-model="form.email" 
                            @blur="validateEmail"
                            class="login-input" 
                            :class="{ 'input-error': errors.email }"
                            required
                        >
                        <span v-if="errors.email" class="input-error-text">{{ errors.email }}</span>
                    </div>
                    
                    <div class="login__form-info-password">
                        <label class="login__form-info-password-txt">Пароль</label>
                        <input 
                            type="password" 
                            placeholder="►► Пароль" 
                            v-model="form.password" 
                            @blur="validatePassword"
                            class="login-input" 
                            :class="{ 'input-error': errors.password }"
                            required
                        >
                        <span v-if="errors.password" class="input-error-text">{{ errors.password }}</span>
                    </div>
                    
                    <div v-if="serverError" class="login__toast error">
                        {{ serverError }}
                    </div>
                    
                    <button type="submit" :disabled="isLoading || !isFormValid" class="login__btn">
                        {{ isLoading ? 'Вход...' : '► Войти' }}
                    </button>
                </form>
                
                <div class="login__register-link">
                    <span>У меня нет аккаунта?</span>
                    <router-link to="/auth/register">Создать аккаунт</router-link>
                </div>

                <div class="login__recovery-link">
                    <router-link to="/auth/recovery" class="login__recovery-txt">
                    Забыли пароль?
                    </router-link>
                </div>
            </div>
            
            <div class="login__img-wrapper">
                <template v-if="imageLoading">
                    <div class="login__img-skeleton"></div>
                </template>
                
                <template v-else-if="imageError">
                    <div class="login__img-error">🍔</div>
                </template>
                
                <template v-else>
                    <img 
                        :src="loginImageUrl" 
                        alt="Bons Burger" 
                        class="login__img"
                        @error="handleImageError"
                        crossorigin="anonymous"
                    >
                </template>
            </div>
        </div>
    </main> 
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({ email: '', password: '' })
const errors = ref({ email: '', password: '' })
const serverError = ref('')
const isLoading = ref(false)  // 🔥 ДОБАВЛЕНО: состояние загрузки

const loginImageUrl = ref(null)
const imageLoading = ref(true)
const imageError = ref(false)

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

const fetchLoginImage = async () => {
    imageLoading.value = true
    imageError.value = false
    try {
        const res = await axios.get(`${API_BASE}/home/login-page-image`)
        loginImageUrl.value = res.data.imageUrl || res.data.image || res.data
    } catch (e) {
        console.warn('Не удалось загрузить картинку логина:', e)
        imageError.value = true
    } finally {
        imageLoading.value = false
    }
}

const handleImageError = () => {
    imageError.value = true
    imageLoading.value = false
}

const validateEmail = () => {
    const email = form.value.email.trim()
    if (!email) {
        errors.value.email = 'Email обязателен'
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        errors.value.email = 'Некорректный формат email'
    } else {
        errors.value.email = ''
    }
}

const validatePassword = () => {
    const password = form.value.password
    if (!password) {
        errors.value.password = 'Пароль обязателен'
    } else if (password.length < 6) {
        errors.value.password = 'Минимум 6 символов'
    } else {
        errors.value.password = ''
    }
}

const isFormValid = computed(() => {
    return form.value.email && form.value.password && !errors.value.email && !errors.value.password
})

const handleSubmit = async () => {
    validateEmail()
    validatePassword()
    if (!isFormValid.value) return
    
    serverError.value = ''
    isLoading.value = true
    
    try {
        await authStore.login({ email: form.value.email, password: form.value.password })
        const redirect = router.currentRoute.value.query.redirect || '/'
        router.push(redirect)
    } catch (e) {
        serverError.value = authStore.error || 'Ошибка входа'
    } finally {
        isLoading.value = false
    }
}

onMounted(() => {
    fetchLoginImage()
})
</script>

<style scoped src="@/assets/styles/views/Login.css">

</style>