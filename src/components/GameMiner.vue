<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'

// IMPORT DES IMAGES (Chemin relatif depuis components vers assets)
import cobaltImg from '../assets/cobalt.png'
import mineBgImg from '../assets/mine.png'
import minerImg from '../assets/mineur.png'

// Pour dire au parent que le jeu est fini
const emit = defineEmits(['finish'])

interface Minerai {
    id: number;
    top: string;
    left: string;
    miné: boolean;
}

// --- VARIABLES ---
const score = ref(0)
const objectif = 3
const jeuTermine = ref(false)
const cibleIndex = ref<number | null>(null);
const enTrainDeMiner = computed(() => cibleIndex.value !== null);
const listeMinerais = ref<Minerai[]>([]);

// Position de départ du mineur
const minerBaseTop = '85%'
const minerBaseLeft = '50%'
const minerTop = ref(minerBaseTop)
const minerLeft = ref(minerBaseLeft)

// --- FONCTIONS ---
function getPositionAleatoire() {
    const randomTop = Math.floor(Math.random() * 30) + 45; 
    const randomLeft = Math.floor(Math.random() * 80) + 10;
    return { top: `${randomTop}%`, left: `${randomLeft}%` };
}

function genererTousLesMinerais() {
    listeMinerais.value = [];
    for (let i = 0; i < objectif; i++) {
        const pos = getPositionAleatoire();
        listeMinerais.value.push({
            id: i, top: pos.top, left: pos.left, miné: false
        });
    }
}

function lancerMinage(index: number) {
  if (jeuTermine.value || enTrainDeMiner.value || listeMinerais.value[index].miné) return
  
  cibleIndex.value = index;
  minerTop.value = listeMinerais.value[index].top
  minerLeft.value = listeMinerais.value[index].left

  setTimeout(() => {
      score.value++
      listeMinerais.value[index].miné = true;
      
      if (score.value >= objectif) {
        jeuTermine.value = true
      } else {
        minerTop.value = minerBaseTop
        minerLeft.value = minerBaseLeft
        setTimeout(() => { cibleIndex.value = null; }, 1500)
      }
  }, 1500)
}

function finirNiveau() {
    emit('finish') // On signale la fin au parent
}

onMounted(() => {
    genererTousLesMinerais();
})
</script>

<template>
  <div class="pixel-zone" :style="{ backgroundImage: `url(${mineBgImg})` }">
    <div v-if="!jeuTermine" class="game-container">
        <div class="header-box box-pixel top-ui">
            <h1>⛏️ MISSION COBALT</h1>
            <p v-if="!enTrainDeMiner" class="instruction">Tu as 8 ans. Au travail.</p>
            <p v-else class="instruction clignote">Extraction en cours...</p>
            <div class="stats">SAC : <span class="score-color">{{ score }} / {{ objectif }}</span></div>
        </div>
      
      <img :src="minerImg" alt="Mineur" class="miner-img" :style="{ top: minerTop, left: minerLeft }" />

      <template v-for="(minerai, index) in listeMinerais" :key="minerai.id">
        <button v-if="!minerai.miné" @click="lancerMinage(index)" class="cobalt-btn" :class="{ 'disabled': enTrainDeMiner }" :style="{ top: minerai.top, left: minerai.left }">
            <img :src="cobaltImg" alt="Minerai" class="ore-image" />
        </button>
      </template>
    </div>

    <div v-else class="result-zone">
      <h1 class="title-end box-pixel">BRAVO ?</h1>
      <div class="big-data-box box-pixel">
        <div class="data-point">PAIEMENT : <br><span class="highlight-red">1 CENTIME</span></div>
        <div class="data-point">SANTÉ : <br><span class="highlight-red">POUMONS DÉTRUITS</span></div>
      </div>
      <div class="shock-text box-pixel">
        <p>Tu es un mineur de 8 ans.</p>
        <p>Tu as perdu tes poumons pour le confort des Européens.</p>
      </div>
      <button @click="finirNiveau" class="restart-btn box-pixel">ALLER À L'USINE (Niveau 2) >></button>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
.pixel-zone { min-height: 90vh; background-repeat: no-repeat; background-position: center center; background-size: cover; color: #e0e0e0; font-family: 'Press Start 2P', monospace; overflow: hidden; image-rendering: pixelated; position: relative; }
.pixel-zone::before { content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.4); pointer-events: none; }
.box-pixel { background: rgba(0, 0, 0, 0.8); border: 4px solid #000; padding: 15px; display: inline-block; }
.top-ui { position: relative; z-index: 50; }
.game-container { position: relative; height: 80vh; width: 100%; text-align: center; padding-top: 20px; z-index: 2; }
.header-box { margin-bottom: 20px; }
h1 { font-size: 1.2rem; margin-bottom: 15px; text-shadow: 2px 2px #000; }
.instruction { font-size: 0.7rem; color: #ffcccc; margin-bottom: 10px; height: 20px; }
.clignote { animation: blink 1s infinite; color: #ffcc00; }
@keyframes blink { 50% { opacity: 0; } }
.stats { font-size: 1rem; }
.score-color { color: #ffcc00; }
.miner-img { position: absolute; transform: translate(-50%, -50%); width: 420px; height: auto; z-index: 10; transition: top 1.5s ease-in-out, left 1.5s ease-in-out; filter: drop-shadow(4px 4px 0 rgba(0,0,0,0.5)); pointer-events: none; }
.cobalt-btn { position: absolute; transform: translate(-50%, -50%); background: transparent; border: none; cursor: pointer; z-index: 5; transition: opacity 0.3s, transform 0.1s; }
.cobalt-btn:active { transform: translate(-50%, -45%); }
.cobalt-btn.disabled { cursor: not-allowed; }
.ore-image { width: 120px; height: 120px; filter: drop-shadow(5px 5px 0px rgba(0,0,0,0.5)); }
.result-zone { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 90vh; text-align: center; z-index: 2; position: relative; }
.title-end { margin-bottom: 20px; font-size: 1.5rem; color: #ff4444; }
.big-data-box { margin: 20px 0; display: flex; flex-direction: column; gap: 20px; width: 90%; max-width: 450px; }
.shock-text { margin-bottom: 30px; font-size: 0.8rem; line-height: 1.6; max-width: 450px; color: #fff; text-transform: uppercase; }
.highlight-red { color: #ff4444; font-size: 1.2rem; display: block; margin-top: 5px;}
.restart-btn { background-color: #ff4444; color: white; border: 4px solid #fff; padding: 15px 30px; cursor: pointer; font-family: inherit; font-size: 1rem; }
.restart-btn:hover { background-color: #cc0000; border-color: #ccc;}
</style>