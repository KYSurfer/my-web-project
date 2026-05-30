<template>
  <main class="not-found">
    <div class="not-found__content">
      <h1 class="not-found__code">404</h1>
      <h2 class="not-found__title">Страница не найдена</h2>
      <p class="not-found__text">
        Похоже, ты заблудился в лабиринтах Bon's Burgers... 
        Но не волнуйся — наши аниматроники уже высланы на поиски!
      </p>
      
      <div class="not-found__actions">
        <router-link to="/" class="not-found__btn not-found__btn--primary">
          ► На главную
        </router-link>
        <button @click="goBack" class="not-found__btn not-found__btn--secondary">
          ◄ Назад
        </button>
      </div>
    </div>
  </main>
</template>

<script scoped src="@/assets/styles/views/NotFound.css">
import { useRouter } from 'vue-router'

const router = useRouter()

const goBack = () => {
  if (window.history.length <= 1) {
    router.push('/')
  } else {
    router.back()
  }
}
</script>

<style scoped src="@/assets/styles/views/NotFound.css">

</style>