<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import fondMapImg from '../assets/fondmap.png'

const emit = defineEmits(['finish'])

// --- VARIABLES ---
const tours = ref(0)
const distance = ref(0)       // Progression du tour actuel (0 à 100)
const distanceParcourue = ref(0) // Pour le défilement visuel du fond (pixels)
const vitesse = ref(0)
const co2 = ref(0)
const jeuTermine = ref(false)

const puissance = ref(0)
const messages = ref("POUSSE LA MANETTE !")
const messageStyle = ref({}) 

const OBJECTIF_TOURS = 4 
const TOTAL_CO2_OBJECTIF = 82.0 // L'objectif exact en KG

let animationId: number;

function gameLoop() {
    if (jeuTermine.value) return;

    // 1. GESTION VITESSE
    if (parseInt(puissance.value.toString()) === 0) {
        vitesse.value = 0;
    } else {
        const vitesseCible = puissance.value / 80; // Divisé par 80 au lieu de 40 = 2x plus lent
        vitesse.value += (vitesseCible - vitesse.value) * 0.05;
    }
    
    // 2. AVANCEMENT
    if (vitesse.value > 0.001) {
        // "distance" va de 0 à 100 pour un tour
        distance.value += vitesse.value;
        
        // "distanceParcourue" sert juste à faire bouger l'image de fond
        distanceParcourue.value += (vitesse.value * 15); // Facteur visuel

        // --- NOUVEAU CALCUL CO2 ---
        // On calcule le pourcentage total du voyage réalisé (de 0 à 1)
        // (Tours complets + % du tour actuel) / Total à faire
        let progressionTotale = (tours.value + (distance.value / 100)) / OBJECTIF_TOURS;
        
        // On s'assure qu'on ne dépasse pas 100% (1.0)
        if (progressionTotale > 1) progressionTotale = 1;

        // Le CO2 est simplement ce pourcentage appliqué à 82kg
        co2.value = progressionTotale * TOTAL_CO2_OBJECTIF;
        
        // Messages d'ambiance
        if (puissance.value > 80) {
             messageStyle.value = {
                transform: `translate(${Math.random()*2}px, ${Math.random()*2}px)`,
                color: '#ff0000', fontWeight: 'bold'
            }
            messages.value = "POLLUTION MAXIMALE..."
        } else {
             messageStyle.value = { color: '#fff' }
             messages.value = "Transport en cours..."
        }
    }

    // 3. GESTION DES TOURS
    if (distance.value >= 100) {
        tours.value++;
        distance.value = 0; // On remet le compteur du tour à 0
        
        if (tours.value < OBJECTIF_TOURS) {
            document.body.style.backgroundColor = 'white';
            setTimeout(() => document.body.style.backgroundColor = '', 50);
        }
    }

    // 4. FIN DU JEU
    if (tours.value >= OBJECTIF_TOURS) {
        jeuTermine.value = true;
        co2.value = TOTAL_CO2_OBJECTIF; // On force l'affichage final propre
        cancelAnimationFrame(animationId);
    } else {
        animationId = requestAnimationFrame(gameLoop);
    }
}

function finirNiveau() { emit('finish') }

onMounted(() => {
    puissance.value = 0; vitesse.value = 0;
    document.addEventListener('contextmenu', event => event.preventDefault());
    animationId = requestAnimationFrame(gameLoop);
})

onUnmounted(() => { cancelAnimationFrame(animationId); })
</script>

<template>
  <div class="transport-zone" @touchmove.prevent>
    
    <div class="hud box-pixel">
        <div class="row">
            <span>DISTANCE : <span class="highlight">{{ tours }} / {{ OBJECTIF_TOURS }} TOURS</span></span>
            <span>VITESSE : {{ (vitesse * 800).toFixed(0) }} km/h</span>
        </div>
        <div class="co2-row">
            BILAN CARBONE : <span class="highlight-red">{{ co2.toFixed(1) }} kg CO2</span>
        </div>
    </div>

    <div class="game-area">
        <div class="sky">
            <div class="world-container" 
                 :style="{ 
                    backgroundImage: `url(${fondMapImg})`,
                    // Décalage initial -450px pour l'Asie + le défilement
                    backgroundPositionX: `calc(-${distanceParcourue}px - 450px)`
                 }">
            </div>

            <div class="plane-box" :class="{ 'shaking': vitesse > 0.5, 'super-fast': vitesse > 2.0 }">
                ✈️ CARGO
            </div>
            
            <div class="smoke" :style="{ 
                opacity: vitesse > 0.1 ? (puissance / 100) : 0,
                width: (puissance / 2) + '%' 
            }"></div>
        </div>

        <div v-if="!jeuTermine" class="throttle-container box-pixel">
            <label>GAZ</label>
            <div class="slider-wrapper">
                <input type="range" min="0" max="100" v-model="puissance" class="throttle-input">
                <div class="throttle-gauge" :style="{ height: puissance + '%' }"></div>
            </div>
            <span class="percent">{{ puissance }}%</span>
        </div>
    </div>

    <div v-if="!jeuTermine" class="boss-msg" :style="messageStyle">{{ messages }}</div>

    <div v-else class="result-zone box-pixel">
        <h1 class="title-end">LIVRAISON TERMINÉE</h1>
        <p class="shock-text">
            <strong>4 TOURS DU MONDE</strong><br>
            JUSTE POUR LE TRANSPORT
        </p>
        <div class="big-data-box">
            <div class="data-point"><span class="highlight-red">{{ co2.toFixed(0) }} KG CO2</span></div>
        </div>
        <button @click="finirNiveau" class="restart-btn">NIVEAU 4 : UTILISATION >></button>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

.transport-zone {
    min-height: 90vh; background-color: #000033; color: #e0e0e0; font-family: 'Press Start 2P', monospace;
    display: flex; flex-direction: column; align-items: center; overflow: hidden; position: relative;
    touch-action: none; user-select: none; -webkit-user-select: none; overscroll-behavior: none; 
}
.box-pixel { background: #000; border: 4px solid #fff; padding: 10px; text-align: center; z-index: 10; }
.hud { width: 90%; margin-top: 20px; background: rgba(0,0,0,0.8); }
.row { display: flex; justify-content: space-between; font-size: 0.6rem; margin-bottom: 10px; }
.highlight { color: #ffff00; }
.highlight-red { color: #ff0000; font-size: 1rem; display: block; margin-top: 5px; }

.game-area { width: 100%; display: flex; align-items: center; justify-content: center; height: 50vh; margin: 20px 0; }

.sky {
    position: relative; width: 70%; height: 100%;
    border-top: 4px solid #fff; border-bottom: 4px solid #fff;
    overflow: hidden; margin-right: 20px;
}

.world-container { 
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background-repeat: repeat-x;
    background-size: auto 100%; 
    image-rendering: pixelated;
}

.plane-box {
    position: absolute; top: 40%; left: 20%; transform: translate(-50%, -50%);
    background-color: #fff; color: #000; padding: 10px; border: 4px solid #ccc;
    font-size: 0.8rem; z-index: 5; border-radius: 0 20px 20px 0;
}
.plane-box.shaking { animation: shake 0.1s infinite; }
.plane-box.super-fast { background-color: #ff4444; color: white; box-shadow: 0 0 10px #ff0000; }
@keyframes shake { 0% { margin-top: 0; } 25% { margin-top: -5px; } 75% { margin-top: 5px; } 100% { margin-top: 0; } }

.smoke { position: absolute; top: 45%; left: 0; height: 20px; background: #555; z-index: 4; transition: width 0.1s; }

.throttle-container { width: 20%; height: 80%; display: flex; flex-direction: column; align-items: center; justify-content: space-between; }
.slider-wrapper { position: relative; height: 100%; width: 40px; background: #333; border: 2px solid #fff; margin: 10px 0; }
.throttle-input { writing-mode: bt-lr; -webkit-appearance: slider-vertical; width: 100%; height: 100%; opacity: 0; cursor: ns-resize; position: absolute; top: 0; left: 0; z-index: 2; }
.throttle-gauge { position: absolute; bottom: 0; left: 0; width: 100%; background-color: #ff0000; transition: height 0.1s; z-index: 1; }
.percent { font-size: 0.8rem; color: #ff0000; }
.boss-msg { font-size: 0.8rem; color: #ffcc00; text-align: center; height: 40px; margin-bottom: 20px; }

.result-zone { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 90%; max-width: 500px; display: flex; flex-direction: column; gap: 20px; background: black; }
.title-end { color: #00ff00; margin-bottom: 20px; }
.shock-text { line-height: 1.5; font-size: 0.8rem; }
.highlight-white { color: white; font-size: 1.2rem; }
.big-data-box { margin: 20px 0; }
.data-point { font-size: 1.2rem; margin: 10px 0; }
.restart-btn { background-color: #ff4444; color: white; border: 4px solid #fff; padding: 15px 30px; cursor: pointer; font-family: inherit; font-size: 1rem; margin-top: 20px; }
.restart-btn:hover { background-color: #cc0000; }
</style>