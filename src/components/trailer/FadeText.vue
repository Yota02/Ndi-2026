<script setup lang="ts">
defineProps<{
  text: string;
  visible: boolean;
}>();
</script>

<template>
  <Transition name="fade-blur">
    <div v-if="visible" class="fade-text">
      {{ text }}
    </div>
  </Transition>
</template>

<style scoped>
.fade-text {
  font-size: 2.5rem;
  color: white;
  text-align: center;
  padding: 20px;
  font-family: sans-serif;
  font-weight: 400;
  /* Contour noir autour des lettres */
  text-shadow:
    -2px -2px 0 #000,
    2px -2px 0 #000,
    -2px 2px 0 #000,
    2px 2px 0 #000,
    -2px 0 0 #000,
    2px 0 0 #000,
    0 -2px 0 #000,
    0 2px 0 #000;
}

/* Transition avec flou */
.fade-blur-enter-active,
.fade-blur-leave-active {
  transition: opacity 1s ease, filter 1s ease;
}

.fade-blur-enter-from {
  opacity: 0;
  filter: blur(10px);
}

.fade-blur-leave-to {
  opacity: 0;
  filter: blur(10px);
}
</style>