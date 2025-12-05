<template>
  <div class="app">
    <h1>Animation Tux</h1>

    <TuxAnimation
      image-url="/Ndi-2026/public/assets/tuxTriste2Larme.png"
      :frame-width="500"
      :gap="0"
      :total-frames="9"
      :speed="250"
      :width="500"
      :height="500"
    />
  </div>
</template>

<script setup lang="ts">
import TuxAnimation from './components/TuxAnimation.vue'
</script>
