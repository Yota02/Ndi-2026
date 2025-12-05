<script setup lang="ts">
import { useRouter } from 'vue-router'
import LaserQuizGame from '@/components/lasergame/LaserQuizGame.vue'

const router = useRouter()

// Fonction pour retourner au menu
const goBack = () => {
  router.push('/laser-game')
}
</script>

<template>
  <div class="quiz-page">
    <LaserQuizGame @close="goBack" @win="goBack" />
  </div>
</template>

<style scoped>
.quiz-page {
  width: 100vw;
  height: 100vh;
  background-color: #111; /* Fond sombre par défaut pour le quiz */
  overflow: hidden;
}
</style>
