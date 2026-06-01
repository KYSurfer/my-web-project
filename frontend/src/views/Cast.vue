<template>
  <main>
    <h1 class="page-title">Наш персонал</h1>
    <p class="page-subtitle">Команда, которая делает Bon's Burgers живым</p>

    <template v-if="loading">
      <div class="characters-grid">
        <SkeletonCard v-for="i in 10" :key="`sk-cast-${i}`" />
      </div>
    </template>

    <div v-else-if="error" class="main-content__error">
      <p>Ошибка: {{ error }}</p>
      <button @click="fetchCast" class="retry-btn">Попробовать снова</button>
    </div>

    <template v-else>
      <div class="characters-grid">
        <div v-for="member in cast" :key="member.id" class="main-content__block">
          <img 
            :src="member.image" 
            :alt="member.title" 
            class="main-content__block-img"
            loading="lazy"
          >
          <h2 class="main-content__block-name">{{ member.title }}</h2>
          <button @click="handleViewProfile(member)" class="learn-more-btn">►Профиль</button>
        </div>
      </div>
    </template>
  </main>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useCast } from '@/composables/useCast'
import SkeletonCard from '@/components/SkeletonCard.vue'

const router = useRouter()
const { cast, loading, error, fetchCast } = useCast()

const handleViewProfile = (member) => {
  if (member.route) {
    router.push(member.route)
  } else {
    router.push(`/cast/${member.id}`)
  }
}
</script>

<style scoped src="@/assets/styles/views/Cast.css">

</style>