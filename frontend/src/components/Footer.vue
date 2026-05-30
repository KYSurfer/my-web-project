<template>
  <footer class="footer">
    <div class="footer__main">
      <div>
        <div class="footer__main-logo">
          <template v-if="logoLoading">
            <div class="footer__logo-skeleton"></div>
          </template>
          
          <template v-else-if="logoError">
            <div class="footer__logo-error">🍔</div>
          </template>
          <template v-else>
            <img 
              :src="logoUrl" 
              alt="Bon's Burgers лого" 
              class="footer__main-logo-img"
              @error="handleLogoError"
            >
          </template>
          
          <div class="footer__main-logo-text">
            <h2 class="footer__main-logo-text-name">Bon's Burgers</h2>
            <span class="footer__main-logo-text-est">est. 1974</span>
          </div>
        </div>
        <div class="footer__main-under-logo">
          <span>Вместе навсегда!</span>
          <span>BUNNY SMILES INC. © 1974</span>
        </div>
      </div>
      <div class="footer__main-contacts">
        <h2>Контакты</h2>
        <span>Брайтон, Висконсин</span>
        <span>(555) 294-2453</span>
        <span>info@bonsburgers.com</span>
      </div>
    </div>
    <div class="footer__bottom">
      <div class="footer__bottom-txt">© 1974 Bon's Burgers / Bunny Smiles Inc. All Rights Reserved.</div>
      <div>Создаем улыбки с 1974</div>
    </div>
  </footer>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/plugins/axios'

const logoUrl = ref(null)
const logoLoading = ref(true)
const logoError = ref(null)

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

const fetchLogo = async () => {
  logoLoading.value = true
  logoError.value = null
  try {
    const res = await api.get('/home/logo')
    logoUrl.value = res.data.imageUrl || res.data.logo || res.data
  } catch (e) {
    logoError.value = true
    console.warn('Не удалось загрузить логотип:', e)
  } finally {
    logoLoading.value = false
  }
}

const handleLogoError = () => {
  logoError.value = true
  logoLoading.value = false
}

onMounted(() => {
  fetchLogo()
})
</script>

<style scoped src="@/assets/styles/components/Footer.css">

</style>