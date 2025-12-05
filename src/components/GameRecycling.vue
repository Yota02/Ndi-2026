<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits(['finish'])

// --- VARIABLES ---
// 'none', 'trash', 'recycle'
const choix = ref('none')

// --- LOGIQUE DRAG & DROP ---

function onDragStart(event: DragEvent) {
    if (event.dataTransfer) {
        event.dataTransfer.dropEffect = 'move'
        event.dataTransfer.effectAllowed = 'move'
        event.dataTransfer.setData('item', 'phone')
    }
}

function onDrop(event: DragEvent, destination: string) {
    choix.value = destination
}

function finirJeu() {
    emit('finish')
}
</script>

<template>
  <div class="recycling-zone" :class="{ 'burning': choix === 'trash' }">
    
    <div class="header-ui box-pixel">
        <h1>♻️ FIN DE VIE</h1>
        <p v-if="choix === 'none'">Ton téléphone est vieux et lent. Qu'en fais-tu ?</p>
    </div>

    <div v-if="choix === 'none'" class="game-area">
        
        <div 
            class="bin trash-bin"
            @dragover.prevent
            @drop="onDrop($event, 'trash')"
        >
            <div class="bin-lid"></div>
            <div class="bin-body">ORDURES</div>
        </div>

        <div 
            class="old-phone"
            draggable="true"
            @dragstart="onDragStart"
        >
            📱 <br>vieux<br>tel
        </div>

        <div 
            class="bin recycle-bin"
            @dragover.prevent
            @drop="onDrop($event, 'recycle')"
        >
            <div class="bin-lid"></div>
            <div class="bin-body">RECYCLAGE</div>
            <div class="recycle-icon">♻️</div>
        </div>

    </div>

    <div v-else-if="choix === 'trash'" class="result-zone box-pixel">
        <h1 class="title-end">DÉCHARGE SAUVAGE</h1>
        
        <div class="fire-anim">🔥 INCENDIE TOXIQUE 🔥</div>

        <p class="shock-text">
            Ton téléphone a fini dans une décharge à ciel ouvert (probablement au Ghana).<br><br>
            <strong>DANGER :</strong> La batterie lithium a été percée et a explosé. 
            Les fumées libèrent du plomb et du mercure dans l'air.
        </p>
        
        <div class="big-data-box">
            <div class="data-point">RECYCLAGE : <span class="highlight-red">0 %</span></div>
            <div class="data-point">POLLUTION SOL : <span class="highlight-red">IRRÉVERSIBLE</span></div>
        </div>

        <button @click="choix = 'none'" class="retry-btn">ESSAYER AUTRE CHOSE</button>
    </div>

    <div v-else-if="choix === 'recycle'" class="result-zone box-pixel">
        <h1 class="title-end green">RECYCLAGE... OU PRESQUE</h1>
        
        <p class="shock-text">
            C'est mieux que la poubelle. On va récupérer un peu d'or et de cuivre.<br>
            <strong>MAIS ATTENTION :</strong> Le processus de recyclage consomme lui aussi beaucoup d'énergie.
        </p>

        <div class="lesson-box">
            <p>LE MEILLEUR DÉCHET EST CELUI QU'ON NE PRODUIT PAS.</p>
            <p>La meilleure solution était de le <strong>RÉPARER</strong> ou de le <strong>GARDER</strong>.</p>
        </div>
        
        <div class="big-data-box">
            <div class="data-point">MATIÈRE RÉCUPÉRÉE : <span class="highlight-white">~20 %</span></div>
            <div class="data-point">PERTE : <span class="highlight-red">80 %</span></div>
        </div>

        <div class="end-buttons">
             <button @click="location.reload()" class="restart-btn">REJOUER LE CYCLE</button>
        </div>
    </div>

  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

.recycling-zone {
    min-height: 90vh;
    background-color: #222; 
    color: #e0e0e0;
    font-family: 'Press Start 2P', monospace;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    transition: background 1s;
}

.box-pixel {
    background: #000;
    border: 4px solid #fff;
    padding: 15px;
    text-align: center;
    box-shadow: 4px 4px 0 #555;
    z-index: 10;
}

/* HEADER */
.header-ui { margin-bottom: 40px; }
h1 { font-size: 1.2rem; margin-bottom: 10px; color: #fff; }
p { font-size: 0.7rem; line-height: 1.5; color: #aaa; }

/* GAME AREA */
.game-area {
    display: flex;
    align-items: flex-end;
    justify-content: center;
    gap: 50px;
    height: 40vh;
    width: 100%;
}

/* LE TÉLÉPHONE */
.old-phone {
    width: 80px; height: 140px;
    background: #111;
    border: 4px solid #555;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    text-align: center; font-size: 0.6rem; color: #555;
    cursor: grab;
    margin-bottom: 50px; /* Pour qu'il soit plus haut que les poubelles */
    animation: float 2s infinite ease-in-out;
}
.old-phone:active { cursor: grabbing; }

@keyframes float { 0% { transform: translateY(0); } 50% { transform: translateY(-10px); } 100% { transform: translateY(0); } }

/* LES POUBELLES (Cubes CSS) */
.bin {
    width: 120px; height: 150px;
    position: relative;
    display: flex; flex-direction: column; align-items: center; justify-content: flex-end;
}

.bin-lid {
    width: 130px; height: 20px;
    background: #444;
    border: 2px solid #000;
    margin-bottom: 5px;
    transform: rotate(-5deg); /* Couvercle un peu ouvert */
}

.bin-body {
    width: 100%; height: 100%;
    border: 4px solid #000;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.6rem; color: black; font-weight: bold;
}

/* Style Poubelle Trash */
.trash-bin .bin-body { background: #555; color: white; }
.trash-bin .bin-lid { background: #333; }

/* Style Poubelle Recyclage */
.recycle-bin .bin-body { background: #2ecc71; }
.recycle-bin .bin-lid { background: #27ae60; }
.recycle-icon { position: absolute; font-size: 2rem; opacity: 0.5; bottom: 20px; }


/* --- RESULTATS --- */
.result-zone { width: 90%; max-width: 600px; display: flex; flex-direction: column; align-items: center; gap: 20px;}
.title-end { color: #ff4444; }
.title-end.green { color: #2ecc71; }
.shock-text { font-size: 0.7rem; line-height: 1.6; text-align: left; }
.highlight-red { color: #ff4444; }
.highlight-white { color: #fff; }

.lesson-box {
    border: 2px dashed #fff;
    padding: 15px;
    margin: 10px 0;
    font-size: 0.6rem;
    color: #ffff00;
}

.restart-btn {
    background-color: #fff; color: black; border: 4px solid #555; 
    padding: 15px 30px; cursor: pointer; font-family: inherit; font-size: 1rem;
    margin-top: 10px;
}
.retry-btn {
    background: transparent; color: #fff; border: 1px solid #fff; padding: 10px; cursor: pointer; font-family: inherit;
}

/* --- EFFET DE FEU (POUR LA DÉCHARGE) --- */
.recycling-zone.burning {
    animation: fireBg 2s infinite;
}

@keyframes fireBg {
    0% { background-color: #220000; }
    25% { background-color: #441100; }
    50% { background-color: #552200; }
    75% { background-color: #330000; }
    100% { background-color: #220000; }
}

.fire-anim {
    font-size: 1.2rem; color: #ffcc00;
    animation: blink 0.2s infinite;
    font-weight: bold;
    text-shadow: 0 0 10px red;
}
</style>