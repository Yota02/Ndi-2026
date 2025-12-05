<script setup lang="ts">
import { RouterView } from 'vue-router'
import ChatBot from '@/components/ChatBot.vue'
import { ref, provide } from 'vue'
import SpriteAnimation from '@/components/TuxAnimation.vue'

// 1. Définir la configuration par défaut (État initial)
const defaultTuxConfig = {
  x: 10,
  y: 65,
  width: 300,
  height: 300,
  emotion: 'happy',
  hoverEmotion: 'happy',
  clickEmotion: 'clinOeil',
  enableHover: true,
  enableClick: true,
  resetOnMouseLeave: true,
}

// 2. Créer une version réactive modifiable
const tuxConfig = ref({ ...defaultTuxConfig })

// 3. Fournir cet objet et une fonction de reset à toute l'application
provide('tuxConfig', tuxConfig)
provide('resetTuxConfig', () => {
  tuxConfig.value = { ...defaultTuxConfig }
})

const tuxRef = ref()
</script>

<template>
  <div>
    <RouterView />
    <ChatBot />

    <SpriteAnimation
      ref="tuxRef"
      :x="tuxConfig.x"
      :y="tuxConfig.y"
      :width="tuxConfig.width"
      :height="tuxConfig.height"
      :emotion="tuxConfig.emotion"
      :hoverEmotion="tuxConfig.hoverEmotion"
      :clickEmotion="tuxConfig.clickEmotion"
      :enableHover="tuxConfig.enableHover"
      :enableClick="tuxConfig.enableClick"
      :resetOnMouseLeave="tuxConfig.resetOnMouseLeave"
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
