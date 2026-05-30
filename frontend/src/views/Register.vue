<template>
    <main class="register">
        <router-link to="/" class="register__link">
            <div class="register__back">
                <span class="register__back-txt">◄ На главную</span>  
            </div>
        </router-link>

        <div class="register__form">
            <div class="register__form-info">
                <div class="register__form-info-head">
                    <h1 class="register__form-info-header">Создание аккаунта</h1>
                    <h3 class="register__form-info-undertext">Добро пожаловать!</h3>
                </div>
                
                <form @submit.prevent="handleSubmit">
                    <div class="register__form-info-username">
                        <label class="register__form-info-username-txt">Имя пользователя</label>
                        <input 
                            type="text" 
                            v-model="form.username" 
                            placeholder="►► Имя" 
                            class="register-input"
                            @blur="validateUsername"
                            :class="{ 'input-error': errors.username }"
                            required
                        >
                        <span v-if="errors.username" class="input-error-text">{{ errors.username }}</span>
                    </div>

                    <div class="register__form-info-email">
                        <label class="register__form-info-email-txt">Email</label>
                        <input 
                            type="email" 
                            v-model="form.email" 
                            placeholder="►► Email" 
                            class="register-input"
                            @blur="validateEmail"
                            :class="{ 'input-error': errors.email }"
                            required
                        >
                        <span v-if="errors.email" class="input-error-text">{{ errors.email }}</span>
                    </div>

                    <div class="register__recovery-section">
                        <label class="register__recovery-title">ВОССТАНОВЛЕНИЕ ПАРОЛЯ</label>
                        
                        <input 
                            v-model="recoveryKeyword" 
                            type="text" 
                            placeholder="►► Например: кличка питомца" 
                            class="register__recovery-input"
                            minlength="4"
                        />
                    </div>

                    <div class="register__form-info-password">
                        <label class="register__form-info-password-txt">Пароль</label>
                        <input 
                            type="password" 
                            v-model="form.password" 
                            placeholder="►► Пароль" 
                            class="register-input"
                            @blur="validatePassword"
                            :class="{ 'input-error': errors.password }"
                            required
                        >
                        <span v-if="errors.password" class="input-error-text">{{ errors.password }}</span>
                    </div>

                    <button type="submit" :disabled="isLoading || !isFormValid" class="register__btn">
                        {{ isLoading ? 'Регистрация...' : '► Зарегистрироваться' }}
                    </button>
                </form>
                
                <div class="register__login-link">
                    <span>Уже есть аккаунт?</span>
                    <router-link to="/auth/login">Войти</router-link>
                </div>

                <div v-if="serverError" class="register__toast error">
                    {{ serverError }}
                </div>
            </div>

            <div class="register__img-wrapper">
                <template v-if="imageLoading">
                    <div class="register__img-skeleton"></div>
                </template>
                
                <template v-else-if="imageError">
                    <div class="register__img-error">
                        <span>--Логотип--</span>
                    </div>
                </template>
                
                <template v-else>
                    <img 
                        :src="registerImageUrl" 
                        alt="Bons Burger" 
                        class="register__img"
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
import api from '@/plugins/axios'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({ username: '', email: '', password: '' })
const errors = ref({ username: '', email: '', password: '' })
const serverError = ref('')
const isLoading = ref(false)

const registerImageUrl = ref(null)
const imageLoading = ref(true)
const imageError = ref(false)

const recoveryKeyword = ref('')

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

const fetchRegisterImage = async () => {
    imageLoading.value = true
    imageError.value = false
    try {
        const res = await api.get('/home/register-page-image')
        registerImageUrl.value = res.data.imageUrl || res.data.image || res.data
    } catch (e) {
        console.warn('Не удалось загрузить картинку регистрации:', e)
        imageError.value = true
    } finally {
        imageLoading.value = false
    }
}

const handleImageError = () => {
    imageError.value = true
    imageLoading.value = false
}

const validateUsername = () => {
    const name = form.value.username.trim()
    if (!name) {
        errors.value.username = 'Имя обязательно'
    } else if (name.length < 3) {
        errors.value.username = 'Минимум 3 символа'
    } else {
        errors.value.username = ''
    }
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
    return form.value.username && form.value.email && form.value.password &&
           !errors.value.username && !errors.value.email && !errors.value.password
})

const handleSubmit = async () => {
    validateUsername()
    validateEmail()
    validatePassword()
    
    if (!isFormValid.value) return
    
    serverError.value = ''
    isLoading.value = true
    
    try {
        // 🔥 1. Регистрируем пользователя
        const response = await api.post('/auth/register', {
            username: form.value.username,
            email: form.value.email,
            password: form.value.password
        })
        
        // 🔥 2. Сохраняем авторизацию
        localStorage.setItem('authToken', response.data.token)
        localStorage.setItem('user', JSON.stringify(response.data.user))
        
        authStore.token = response.data.token
        authStore.user = response.data.user
        
        // 🔥 3. Если введено секретное слово (мин. 4 символа) — сохраняем автоматически
        if (recoveryKeyword.value.trim().length >= 4) {
            await api.post('/auth/recovery/keyword', {
                keyword: recoveryKeyword.value.trim()
            }, {
                headers: { Authorization: `Bearer ${response.data.token}` }
            })
            console.log('✅ Секретное слово сохранено')
        }
        
        router.push('/profile')
        
    } catch (error) {
        serverError.value = error.response?.data?.error || 'Ошибка регистрации'
        console.error('Register error:', error)
    } finally {
        isLoading.value = false
    }
}

onMounted(() => {
    fetchRegisterImage()
})
</script>

<style scoped src="@/assets/styles/views/Register.css">
</style>