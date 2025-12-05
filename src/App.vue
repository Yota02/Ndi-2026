<script setup lang="ts">
import { RouterView } from 'vue-router'
import ChatBot from '@/components/ChatBot.vue'
import { ref } from 'vue'
import SpriteAnimation from '@/components/TuxAnimation.vue'

const tuxRef = ref()

</script>

<template>
  <div>
    <RouterView />
    <ChatBot />
    <SpriteAnimation
      ref="tuxRef"
      :x="100"
      :y="100"
      :width="300"
      :height="300"
      :emotion="'happy'"
      :hoverEmotion="'happy'"
      :clickEmotion="'clinOeil'"
      :enableHover="true"
      :enableClick="true"
      :resetOnMouseLeave="true"
    />
  </div>
</template>

<style>
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
