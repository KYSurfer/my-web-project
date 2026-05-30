<template>
  <main>
    <h1 class="page-title">Наши звезды</h1>
    <p class="page-subtitle">Уникальная команда аниматроников</p>

    <template v-if="loading">
      <div class="characters-grid">
        <SkeletonCard v-for="i in 10" :key="`sk-stars-${i}`" />
      </div>
    </template>

    <div v-else-if="error" class="main-content__error">
      <p> Ошибка: {{ error }}</p>
      <button @click="fetchCharacters" class="retry-btn">Попробовать снова</button>
    </div>

    <template v-else>
      <div class="characters-grid">
        <div v-for="char in characters" :key="char.id" class="main-content__block">
          <img 
            :src="char.image" 
            :alt="char.alt || char.title" 
            class="main-content__block-img"
            loading="lazy"
          >
          <h2 class="main-content__block-name">{{ char.title }}</h2>
          <button @click="handleLearnMore(char)" class="learn-more-btn">►Узнать больше!</button>
        </div>
      </div>
    </template>
  </main>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useCharacters } from '@/composables/useCharacters'
import SkeletonCard from '@/components/SkeletonCard.vue'

const router = useRouter()
const { characters, loading, error, fetchCharacters } = useCharacters()

const handleLearnMore = (char) => {
  if (char.route) {
    router.push(char.route)
  } else {
    router.push(`/character/${char.id}`)
  }
}
</script>

<style scoped src="@/assets/styles/views/Stars.css">

</style>