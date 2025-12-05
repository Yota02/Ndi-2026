<script setup lang="ts">
import { RouterView } from 'vue-router'
import ChatBot from '@/components/ChatBot.vue'
import { ref, onMounted, onUnmounted } from 'vue'
import SpriteAnimation from './components/TuxAnimation.vue'

const currentEmotion = ref('happy')

const handleScroll = () => {
  if (window.scrollY > 500) {
    currentEmotion.value = 'sad'
  } else {
    currentEmotion.value = 'happy'
  }
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<template>
  <RouterView />
  <ChatBot/>
  <SpriteAnimation
    :x="100"
    :y="100"
    :width="300"
    :height="300"
    :emotion="currentEmotion"
    :hoverEmotion="'happy'"
  />
</template>

<style>
/* Reset global */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html,
body,
#app {
  height: 100%;
  width: 100%;
  min-height: 100vh;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #000;
}
</style>
