<script setup lang="ts">
import { useRouter } from 'vue-router'
import LaserPuzzleGame from '@/components/lasergame/LaserPuzzleGame.vue'

const router = useRouter()

const goBack = () => {
  router.push('/laser-game')
}
</script>

<template>
  <div class="puzzle-page">
    <LaserPuzzleGame @close="goBack" @win="goBack" />
  </div>
</template>

<style scoped>
.puzzle-page {
  width: 100vw;
  height: 100%;
  background: #111;
  overflow-y: hidden;
}
</style>
