<template>
  <main class="character-page">
    <div class="character-container" v-if="character">
      <!-- Заголовок -->
      <div class="character-header">
        <h1 class="character-title">{{ character.name }}</h1>
        <p class="character-role" v-if="character.role">{{ character.role }}</p>
      </div>

      <div class="character-content">
        <div class="character-main">
          <div class="character-summary" v-if="character.summary">
            <p>{{ character.summary }}</p>
          </div>

          <div class="character-bio" v-if="character.bio">
            <h2 class="character-bio-title">Биография</h2>
            <div v-html="character.bio"></div>
          </div>

        </div>

        <div class="character-infobox">
          <div class="infobox-image" v-if="activeImage">
            <img :src="activeImage" :alt="character.name">
          </div>

          <div class="infobox-section">
            <h3>Основная информация</h3>

            <div class="infobox-row" v-if="character.creator">
              <span class="label">Создатель:</span>
              <span class="value">{{ character.creator }}</span>
            </div>
          </div>


          <div class="infobox-section" v-if="character.knownFor && character.knownFor.length">
            <h3>Известен как</h3>
            <ul class="known-list">
              <li v-for="(item, index) in character.knownFor" :key="index">{{ item }}</li>
            </ul>
          </div>

          <div class="infobox-section" v-if="character.related && character.related.length">
            <h3>Связанные аниматроники</h3>
            <div class="related-list">
              <router-link 
                v-for="rel in character.related" 
                :key="rel.id"
                :to="`/character/${rel.id}`"
                class="related-link"
              >
                {{ rel.name }}
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="loading" class="loading-state">Загрузка персонажа...</div>
    <div v-else-if="error" class="error-state">{{ error }}</div>

    <div v-if="lightboxOpen && character?.gallery?.length" class="lightbox" @click="closeLightbox">
      <img :src="character.gallery[lightboxIndex]" class="lightbox-img">
    </div>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/plugins/axios'

const route = useRoute()
const character = ref(null)
const loading = ref(true)
const error = ref(null)
const lightboxOpen = ref(false)
const lightboxIndex = ref(0)

const isCastPage = computed(() => route.path.startsWith('/cast/'))

const activeImage = computed(() => {
  return character.value?.images?.[0]?.url || character.value?.image || null
})

const getStatLabel = (key) => {
  const labels = {
    danger: 'Опасность',
    intelligence: 'Интеллект',
    speed: 'Скорость',
    strength: 'Сила',
    mystery: 'Загадочность'
  }
  return labels[key] || key
}

const openLightbox = (index) => {
  lightboxIndex.value = index
  lightboxOpen.value = true
}

const closeLightbox = () => {
  lightboxOpen.value = false
}

const fetchCharacter = async () => {
  try {
    loading.value = true
    error.value = null
    
    const characterId = route.params.id
    const isCastRoute = route.path.startsWith('/cast/')
    const endpoint = isCastRoute ? `/cast/${characterId}` : `/characters/${characterId}`
    
    const res = await api.get(endpoint)
    
    if (res.data?.success) {
      character.value = res.data.data
    } else {
      throw new Error(res.data.message || 'Некорректный ответ сервера')
    }
  } catch (err) {
    error.value = `Не удалось загрузить: ${err.message}`
    console.error('Ошибка:', err)
    character.value = getMockCharacter()
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchCharacter()
})
</script>

<style scoped src="@/assets/styles/views/CharacterPage.css">

</style>