<script setup lang="ts">
import { onMounted, onUnmounted, inject } from 'vue'
import NavBar from '@/components/NavBar.vue'
import Sobriete from '@/components/Sobriete.vue'

// 1. Injecter la configuration globale du Tux
// On typage 'any' ici pour simplifier, mais idéalement utilisez une interface
const tuxConfig = inject<any>('tuxConfig')
const resetTuxConfig = inject<() => void>('resetTuxConfig')

onMounted(() => {
  if (tuxConfig) {
    // 2. OVERWRITE : Définir la logique spécifique pour cette page
    // Exemple : On le met au centre, un peu plus grand, et en mode "sad" pour la sobriété
    tuxConfig.value.x = 40 // Nouvelle position X (au centre environ)
    tuxConfig.value.y = 50 // Nouvelle position Y
    tuxConfig.value.width = 400 // Plus grand
    tuxConfig.value.height = 400

    tuxConfig.value.emotion = 'sad' // Émotion par défaut triste
    tuxConfig.value.hoverEmotion = 'sad2' // Si on survole, il pleure plus
    tuxConfig.value.clickEmotion = 'parleSad' // Clic différent

    // On peut même désactiver le comportement de reset standard si besoin
    // tuxConfig.value.resetOnMouseLeave = false;
  }
})

onUnmounted(() => {
  // 3. NETTOYAGE : Important !
  // Quand on quitte cette vue, on remet le Tux comme il est défini dans App.vue par défaut
  if (resetTuxConfig) {
    resetTuxConfig()
  }
})
</script>

<template>
  <NavBar />
  <Sobriete />
</template>

<style scoped></style>
