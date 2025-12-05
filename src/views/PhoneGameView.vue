<script setup lang="ts">
import { ref, watch } from 'vue'

import GameMiner from '../components/GameMiner.vue'
import GameAssembly from '../components/GameAssembly.vue'
import GameTransport from '../components/GameTransport.vue'
import GameUsage from '../components/GameUsage.vue'
// AJOUT FINAL
import GameRecycling from '../components/GameRecycling.vue'
import NavBar from '@/components/NavBar.vue'

const savedLevel = localStorage.getItem('playerLevel')
const currentLevel = ref(savedLevel ? parseInt(savedLevel) : 1)

watch(currentLevel, (newLevel) => {
    localStorage.setItem('playerLevel', newLevel.toString())
})

function changerNiveau(niveau: number) {
    currentLevel.value = niveau
}

function allerAuNiveauSuivant() {
    currentLevel.value++
}

function recommencerJeu() {
    currentLevel.value = 1
}
</script>

<template>
  <NavBar/>
  <div class="main-container">

    <div class="nav-bar">
        <button @click="changerNiveau(1)" :class="{ active: currentLevel === 1 }">1. MINE</button>
        <button @click="changerNiveau(2)" :class="{ active: currentLevel === 2 }">2. USINE</button>
        <button @click="changerNiveau(3)" :class="{ active: currentLevel === 3 }">3. AVION</button>
        <button @click="changerNiveau(4)" :class="{ active: currentLevel === 4 }">4. USAGE</button>
        <button @click="changerNiveau(5)" :class="{ active: currentLevel === 5 }">5. FIN</button>
    </div>

    <div class="game-wrapper">
        <GameMiner v-if="currentLevel === 1" @finish="allerAuNiveauSuivant" />
        <GameAssembly v-else-if="currentLevel === 2" @finish="allerAuNiveauSuivant" />
        <GameTransport v-else-if="currentLevel === 3" @finish="allerAuNiveauSuivant" />
        <GameUsage v-else-if="currentLevel === 4" @finish="allerAuNiveauSuivant" />

        <GameRecycling v-else-if="currentLevel === 5" @finish="allerAuNiveauSuivant" @restart="recommencerJeu" />
    </div>

  </div>
</template>

<style scoped>
.main-container { background-color: #000; min-height: 100vh; padding-top: 80px;}
.nav-bar { display: flex; justify-content: center; gap: 5px; padding: 10px; background: #222; border-bottom: 2px solid #555; flex-wrap: wrap; }
.nav-bar button { background: #444; color: #fff; border: 1px solid #666; padding: 5px 10px; cursor: pointer; font-family: monospace; font-size: 0.8rem; }
.nav-bar button:hover { background: #666; }
.nav-bar button.active { background: #00ff00; color: black; font-weight: bold; border-color: #fff; }
</style>
