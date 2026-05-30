<template>
  <div id="app">
    <Header 
      v-if="!$route.meta.hideHeader" 
      :is-authenticated="auth.isAuthenticated"
      :user-name="auth.userName"
      @logout="handleLogout"
    />
    
    <main class="app-main">
      <template v-if="auth.isAuthenticated && settings.enableFx">
        <router-view v-slot="{ Component, route }">
          <transition name="fnaf-cam" mode="out-in">
            <component :is="Component" :key="route.fullPath" />
          </transition>
        </router-view>
      </template>
      
      <template v-else>
        <router-view :key="$route.fullPath" />
      </template>
    </main>
    
    <Footer v-if="!$route.meta.hideFooter" />
    
    <div v-if="auth.isLoading" class="global-loader">
      <div class="loader-spinner"></div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useSettingsStore } from '@/stores/settings'
import Header from "@/components/Header.vue"
import Footer from "@/components/Footer.vue"

const router = useRouter()
const auth = useAuthStore()
const settings = useSettingsStore()

const handleLogout = () => {
  auth.logout()
  localStorage.removeItem('enableFnaFx')
  router.push('/')
}

onMounted(async () => {
  if (!auth.isAuthenticated && auth.token) {
    await auth.checkAuth()
  }
})
</script>

<style>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #000;
  color: #fff;
  font-family: 'Uncage', 'EkiR', sans-serif;
}

.app-main {
  flex: 1;
  position: relative;
  overflow: hidden;
}

.fnaf-cam-enter-active,
.fnaf-cam-leave-active {
  position: relative;
}

@keyframes cam-glitch-enter {
  0% { opacity: 0; filter: grayscale(1) contrast(1.5) brightness(0.2); transform: translateX(-4px) skewX(-1deg); }
  10% { opacity: 0.5; filter: grayscale(1) contrast(2) brightness(0.8); transform: translateX(2px); }
  20% { opacity: 0.7; filter: grayscale(1) contrast(1.2) brightness(0.4); transform: translateX(-2px); }
  30% { opacity: 0.4; filter: grayscale(1) contrast(3) brightness(0.9); transform: translateX(1px); }
  40% { opacity: 0.8; filter: grayscale(1) contrast(1.5) brightness(0.6); transform: translateX(-1px); }
  60% { opacity: 0.9; filter: grayscale(1) contrast(1.1) brightness(0.8); transform: translateX(0); }
  100% { opacity: 1; filter: grayscale(0) contrast(1) brightness(1); transform: translateX(0) skewX(0); }
}

@keyframes cam-glitch-leave {
  0% { opacity: 1; filter: grayscale(0); transform: translateX(0); }
  20% { filter: grayscale(1) brightness(0.8); transform: translateX(-2px); }
  40% { filter: grayscale(1) brightness(0.5); transform: translateX(2px); }
  60% { filter: grayscale(1) brightness(0.3); transform: translateX(-1px); }
  100% { opacity: 0; filter: grayscale(1) brightness(0); transform: translateX(0); }
}

.fnaf-cam-enter-active {
  animation: cam-glitch-enter 0.6s steps(8) forwards;
}
.fnaf-cam-leave-active {
  animation: cam-glitch-leave 0.3s ease-out forwards;
}

.fnaf-cam-enter-active::after {
  content: '';
  position: absolute;
  top: -100%;
  left: 0;
  width: 100%;
  height: 200px;
  background: linear-gradient(to bottom, 
    transparent 0%, 
    rgba(255,255,255,0.1) 10%,
    rgba(255,255,255,0.4) 50%, 
    rgba(255,255,255,0.1) 90%,
    transparent 100%
  );
  animation: scan-bar-move 0.6s linear forwards;
  z-index: 50;
  pointer-events: none;
  mix-blend-mode: screen;
  filter: blur(1px);
}

@keyframes scan-bar-move {
  0% { top: -20%; opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { top: 120%; opacity: 0; }
}

.fnaf-cam-enter-active::before,
.fnaf-cam-leave-active::before {
  content: '';
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent 0px,
    transparent 2px,
    rgba(0, 0, 0, 0.3) 3px,
    rgba(0, 0, 0, 0.3) 4px
  );
  z-index: 40;
  pointer-events: none;
}

.global-loader {
  position: fixed;
  inset: 0;
  background: rgba(10, 10, 10, 0.95);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.loader-spinner {
  width: 50px;
  height: 50px;
  border: 3px solid rgba(255, 255, 255, 0.1);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>