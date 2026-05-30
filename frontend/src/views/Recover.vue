<template>
  <main class="recovery-page">
    <router-link to="/auth/login" class="recovery__back">
      <span class="recovery__back-txt">◄ Назад ко входу</span>
    </router-link>

    <h1 class="page-title">🔐 Восстановление пароля</h1>

    <!-- 🔹 Шаг 1: Email + Секретное слово -->
    <div v-if="step === 1" class="recovery-step">
      <p class="step-desc">Введите email и ваше секретное слово</p>
      
      <input 
        v-model="email" 
        type="email" 
        placeholder="►► Email" 
        class="recovery-input"
        :disabled="loading"
      >
      <input 
        v-model="keyword" 
        type="text" 
        placeholder="►► Секретное слово" 
        class="recovery-input"
        :disabled="loading"
        @keyup.enter="verifyKeyword"
      >
      
      <button @click="verifyKeyword" :disabled="!canVerify || loading" class="recovery-btn">
        {{ loading ? 'Проверка...' : '► Проверить данные' }}
      </button>
      
      <p v-if="error" class="error-msg">{{ error }}</p>
    </div>

    <!-- 🔹 Шаг 2: Новый пароль -->
    <div v-else-if="step === 2" class="recovery-step">
      <p class="step-desc">Придумайте новый пароль</p>
      
      <input 
        v-model="newPassword" 
        type="password" 
        placeholder="►► Новый пароль (мин. 6 символов)" 
        class="recovery-input"
        minlength="6"
      >
      <input 
        v-model="confirmPassword" 
        type="password" 
        placeholder="►► Повторите пароль" 
        class="recovery-input"
        @keyup.enter="resetPassword"
      >
      
      <p v-if="passwordError" class="error-msg">{{ passwordError }}</p>
      
      <button @click="resetPassword" :disabled="!canReset || loading" class="recovery-btn">
        {{ loading ? 'Смена...' : '► Сменить пароль' }}
      </button>
      
      <p v-if="resetSuccess" class="success-msg">
        ✅ Пароль изменён! <router-link to="/auth/login">Войти</router-link>
      </p>
    </div>
  </main>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/plugins/axios'

const router = useRouter()

// Состояния
const step = ref(1)
const email = ref('')
const keyword = ref('')
const loading = ref(false)
const error = ref(null)

// Новый пароль
const newPassword = ref('')
const confirmPassword = ref('')
const passwordError = ref(null)
const resetSuccess = ref(false)

const userId = ref(null)
const resetToken = ref(null)

// Вычисляемые свойства
const canVerify = computed(() => 
  email.value.trim().length > 0 && keyword.value.trim().length >= 4
)

const canReset = computed(() => 
  newPassword.value.length >= 6 && 
  newPassword.value === confirmPassword.value
)

// 🔹 Шаг 1: Проверка email + keyword
const verifyKeyword = async () => {
  if (!canVerify.value) return
  loading.value = true
  error.value = null
  
  try {
    const res = await api.post('/auth/recovery/verify-keyword', {
      email: email.value.trim().toLowerCase(),
      keyword: keyword.value.trim()
    })
    
    if (res.data.success) {
      userId.value = res.data.user_id
      resetToken.value = res.data.reset_token
      step.value = 2
    }
  } catch (e) {
    error.value = e.response?.data?.error || 'Неверные данные'
  } finally {
    loading.value = false
  }
}

// 🔹 Шаг 2: Сброс пароля
const resetPassword = async () => {
  if (!canReset.value) {
    passwordError.value = newPassword.value.length < 6 
      ? 'Минимум 6 символов' 
      : 'Пароли не совпадают'
    return
  }
  
  loading.value = true
  passwordError.value = null
  
  try {
    await api.post('/auth/recovery/reset', {
      user_id: userId.value,
      reset_token: resetToken.value,
      new_password: newPassword.value
    })
    resetSuccess.value = true
  } catch (e) {
    passwordError.value = e.response?.data?.error || 'Не удалось сменить пароль'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.recovery-page { 
  padding-top: 150px; 
  min-height: 100vh; 
  background: #000; 
  color: #fff; 
  font-family: 'Uncage', sans-serif; 
  text-align: center; 
}

.recovery__back {
  display: inline-block;
  margin-bottom: 20px;
  text-decoration: none;
}
.recovery__back-txt {
  color: var(--static-gray, #6b6b6b);
  font-family: 'Uncage', sans-serif;
  transition: color 0.2s;
}
.recovery__back-txt:hover {
  color: var(--vintage-yellow);
}

.page-title { 
  font-size: 2.5rem; 
  color: var(--vintage-yellow); 
  text-shadow: -3px 3px 0 var(--blood-red); 
  margin-bottom: 10px; 
}

.recovery-step { 
  max-width: 500px; 
  margin: 0 auto; 
}

.step-desc { 
  color: rgb(180,180,180); 
  margin-bottom: 24px; 
  font-size: 1.1rem; 
}

.recovery-input { 
  width: 100%; 
  padding: 12px 16px; 
  margin-bottom: 16px; 
  background: #0a0a0a; 
  border: 2px solid var(--vintage-yellow); 
  border-radius: 6px; 
  color: #fff; 
  font-family: 'Uncage'; 
  font-size: 1rem; 
  box-sizing: border-box;
}
.recovery-input::placeholder { color: #666; }
.recovery-input:disabled { opacity: 0.6; cursor: not-allowed; }

.recovery-btn { 
  width: 100%; 
  padding: 14px; 
  background: var(--vintage-yellow); 
  border: none; 
  border-radius: 6px; 
  color: black; 
  font-family: 'Uncage'; 
  font-size: 1.1rem; 
  font-weight: bold; 
  cursor: pointer; 
  margin-bottom: 12px; 
  transition: transform 0.2s;
}
.recovery-btn:hover:not(:disabled) { 
  transform: translate(-2px, -2px); 
  box-shadow: 3px 3px 0 var(--blood-red); 
}
.recovery-btn:disabled { 
  background: #555; 
  cursor: not-allowed; 
  transform: none;
  box-shadow: none;
}

.error-msg { 
  color: var(--blood-red); 
  margin: 12px 0; 
  font-size: 0.95rem;
}
.success-msg { 
  color: #2a9d8f; 
  margin: 12px 0; 
}
.success-msg a {
  color: var(--vintage-yellow);
  text-decoration: none;
  font-weight: bold;
}

@media (max-width: 600px) {
  .page-title { font-size: 2rem; }
  .recovery-input { font-size: 1rem; padding: 10px 14px; }
  .recovery-btn { font-size: 1rem; padding: 12px; }
}
</style>