<script setup lang="ts">
import { useRouter } from 'vue-router'
import LaserSurvivalGame from '@/components/lasergame/LaserSurvivalGame.vue' // Vérifie le chemin

const router = useRouter()

// Quand le jeu émet "close", on retourne au menu
const goBack = () => {
  router.push('/laser-game')
}
</script>

<template>
  <div class="survival-page">
    <LaserSurvivalGame @close="goBack" />
  </div>
</template>

<style scoped>
.survival-page {
  width: 100vw;
  height: 100vh;
  /* On remet le fond ici car le composant est transparent */
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  overflow: hidden;
}
</style>
