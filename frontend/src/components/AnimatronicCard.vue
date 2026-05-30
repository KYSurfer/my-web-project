<template>
  <div class="main-content__block">
    <img :src="animatronic.image" :alt="animatronic.name" class="main-content__block-img">
    <div class="animatronic-card__content">
        <h1 class="animatronic-card__name">{{ animatronic.name }}</h1>
        <h3 class="animatronic-card__alias">{{ animatronic.alias }}</h3>
        <p class="animatronic-card__desc">{{ animatronic.description }}</p>
        <button class="animatronic-card__btn" @click="goToDetail">►Узнать больше!</button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  animatronic: {
    type: Object,
    required: true
  }
})

const router = useRouter()

const goToDetail = () => {
  if (props.animatronic.route) {
    router.push(props.animatronic.route)
  } else {
    router.push(`/character/${props.animatronic.id}`)
  }
}
</script>

<style scoped src="@/assets/styles/components/AnimatronicCard.css">

</style>