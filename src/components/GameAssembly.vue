<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import phoneCaseImg from '../assets/coce.png'
import cpuImg from '../assets/cpu.png'
import batteryImg from '../assets/bateri.png'
import screenImg from '../assets/ecran.png'
import backgroundImage from '../assets/fondusine.png'

const emit = defineEmits(['finish'])

// --- DONNÉES DU JEU ---
const salaire = ref(0.00)
const malus = ref(0.00)
const telephoneFini = ref(false)
const erreurMessage = ref("")

// Calcul du total en temps réel (pour l'affichage final)
const totalNet = computed(() => salaire.value - malus.value)

const ordreRequis = ['cpu', 'battery', 'screen']
const etapeActuelle = ref(0)

const tapis = ref([
    { id: 1, type: 'cpu', name: 'CPU', y: 10, img: cpuImg },
    { id: 2, type: 'battery', name: 'BATTERIE', y: 40, img: batteryImg },
    { id: 3, type: 'screen', name: 'ECRAN', y: 70, img: screenImg }
])

const assemblés = ref<{ type: string, name: string, img?: string }[]>([])
let animationId: number;

// --- BOUCLE DE JEU ---
function gameLoop() {
    if (telephoneFini.value) return;

    tapis.value.forEach(item => {
        item.y += 0.2;

        if (item.y > 110) {
            item.y = -20;
            malus.value += 0.01;
        }
    });
    animationId = requestAnimationFrame(gameLoop);
}

// --- DRAG & DROP ---
function onDragStart(event: DragEvent, index: number, item: any) {
    if (event.dataTransfer) {
        event.dataTransfer.dropEffect = 'move'
        event.dataTransfer.effectAllowed = 'move'
        event.dataTransfer.setData('index', index.toString())
        event.dataTransfer.setData('type', item.type)
        event.dataTransfer.setData('name', item.name)
    }
}

function onDrop(event: DragEvent) {
    if (!event.dataTransfer) return
    const type = event.dataTransfer.getData('type')
    const index = parseInt(event.dataTransfer.getData('index'))

    if (type === ordreRequis[etapeActuelle.value]) {
        const itemComplet = tapis.value.find(x => x.type === type)
        installerComposant(index, itemComplet)
        erreurMessage.value = ""
    } else {
        erreurMessage.value = "Regarde le Post-it ! Mauvais ordre !"
        setTimeout(() => erreurMessage.value = "", 2000)
    }
}

function installerComposant(index: number, item: any) {
    const vraiIndex = tapis.value.findIndex(x => x.type === item.type)
    if (vraiIndex !== -1) tapis.value.splice(vraiIndex, 1)

    assemblés.value.push(item)
    etapeActuelle.value++

    salaire.value += 0.02

    if (tapis.value.length === 0) {
        setTimeout(() => {
            telephoneFini.value = true
            cancelAnimationFrame(animationId)
        }, 2000)
    }
}

function finirNiveau() { emit('finish') }

onMounted(() => { animationId = requestAnimationFrame(gameLoop); })
onUnmounted(() => { cancelAnimationFrame(animationId); })
</script>

<template>
  <div class="factory-zone" :style="{ backgroundImage: `url(${backgroundImage})` }">

    <div v-if="!telephoneFini" class="boss-container">
        <div class="boss-avatar">🤬</div>
        <div class="boss-bubble">
            <p><strong>ALLEZ TRAVAILLE !</strong><br>
            Je te paie pas pour rien.<br>
            T'as une femme et des gosses à nourrir.<br>
            Ta journée de 12h commence !</p>
        </div>
    </div>

    <div class="header-ui box-pixel">
        <h1>🏭 L'USINE</h1>

        <div class="stats-container">
            <div class="stat-box gain">
                <span>GAINS</span>
                <span>{{ salaire.toFixed(2) }} €</span>
            </div>
            <div class="stat-box debt">
                <span>DETTE</span>
                <span>-{{ malus.toFixed(2) }} €</span>
            </div>
        </div>
        <div v-if="erreurMessage" class="error-msg">{{ erreurMessage }}</div>
    </div>

    <div v-if="!telephoneFini" class="work-area">
        <div class="conveyor-belt">
            <div class="belt-track"></div>
            <div v-for="(item, index) in tapis" :key="item.id"
                class="component-item" draggable="true"
                @dragstart="onDragStart($event, index, item)"
                :style="{ top: item.y + '%' }">

                <img v-if="item.img" :src="item.img" class="comp-img pixel-art" />
                <div v-else class="shape-icon" :class="item.type"></div>

                <span class="comp-name">{{ item.name }}</span>
            </div>
        </div>

        <div class="assembly-table">
            <div class="post-it">
                <h3>ORDRE :</h3>
                <ul>
                    <li :class="{ done: etapeActuelle > 0 }">1. Processeur</li>
                    <li :class="{ done: etapeActuelle > 1 }">2. Batterie</li>
                    <li :class="{ done: etapeActuelle > 2 }">3. Écran</li>
                </ul>
            </div>

            <div class="phone-case"
                :style="{ backgroundImage: `url(${phoneCaseImg})` }"
                @dragover.prevent @drop="onDrop">

                <div v-for="(item, i) in assemblés" :key="i"
                    class="installed-part" :class="item.type">
                    <img v-if="item.img" :src="item.img" class="installed-img pixel-art" />
                </div>
            </div>
        </div>
    </div>

    <div v-else class="result-zone">
        <h1 class="title-end box-pixel">ASSEMBLAGE TERMINÉ</h1>
        <div class="big-data-box box-pixel">
            <div class="data-line">
                <span>REVENU BRUT :</span>
                <span class="highlight-green">+{{ salaire.toFixed(2) }} €</span>
            </div>
            <div class="data-line">
                <span>PENALITÉS :</span>
                <span class="highlight-red">-{{ malus.toFixed(2) }} €</span>
            </div>
            <hr class="separator">
            <div class="data-line total">
                <span>TOTAL NET :</span>
                <span :class="totalNet < 0 ? 'highlight-red' : 'highlight-green'">
                    {{ totalNet.toFixed(2) }} €
                </span>
            </div>
        </div>

        <p class="shock-text box-pixel" v-if="totalNet < 0">
            VOUS DEVEZ DE L'ARGENT À L'ENTREPRISE.<br>
            CELA SERA DÉDUIT DE VOTRE PROCHAIN REPAS.
        </p>
        <p class="shock-text box-pixel" v-else>
            QUOTA ATTEINT DE JUSTESSE.<br>
            CONTINUEZ À TRAVAILLER.
        </p>

        <button @click="finirNiveau" class="restart-btn box-pixel">PASSER AU TRANSPORT >></button>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Kalam:wght@700&display=swap');

.factory-zone {
    min-height: 90vh;
    color: #e0e0e0;
    font-family: 'Press Start 2P', monospace;
    display: flex;
    flex-direction: column;
    align-items: center;
    overflow: hidden;
    padding-top: 20px;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    image-rendering: pixelated;
    position: relative; /* Important pour le positionnement absolu du patron */
}

/* --- LE PATRON (STYLES) --- */
.boss-container {
    position: absolute;
    top: 20px;
    right: 20px;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    z-index: 50;
    pointer-events: none; /* Le clic passe à travers */
}

.boss-avatar {
    font-size: 3rem;
    margin-right: 10px;
    filter: drop-shadow(2px 2px 0 #000);
    animation: shake 0.2s infinite; /* Tremblement frénétique */
}

.boss-bubble {
    background-color: #fff;
    color: #000;
    border: 3px solid #000;
    padding: 8px;
    width: 180px; /* Petit et compact */
    font-size: 0.55rem; /* Texte petit */
    line-height: 1.4;
    text-align: left;
    position: relative;
    box-shadow: 5px 5px 0px rgba(0,0,0,0.5);
    animation: shout 0.8s ease-in-out infinite alternate;
}

/* Petite flèche de la bulle */
.boss-bubble::after {
    content: '';
    position: absolute;
    top: -10px;
    right: 20px;
    border-width: 0 10px 10px 10px;
    border-style: solid;
    border-color: transparent transparent #000 transparent;
}

/* Animations patron */
@keyframes shout {
    from { transform: scale(1); }
    to { transform: scale(1.05); }
}
@keyframes shake {
    0% { transform: translate(1px, 1px) rotate(0deg); }
    10% { transform: translate(-1px, -2px) rotate(-1deg); }
    20% { transform: translate(-3px, 0px) rotate(1deg); }
    30% { transform: translate(3px, 2px) rotate(0deg); }
    40% { transform: translate(1px, -1px) rotate(1deg); }
    50% { transform: translate(-1px, 2px) rotate(-1deg); }
    60% { transform: translate(-3px, 1px) rotate(0deg); }
    70% { transform: translate(3px, 1px) rotate(-1deg); }
    80% { transform: translate(-1px, -1px) rotate(1deg); }
    90% { transform: translate(1px, 2px) rotate(0deg); }
    100% { transform: translate(1px, -2px) rotate(-1deg); }
}

/* --- RESTE DU CSS (INCHANGÉ) --- */
.box-pixel { background: #000; border: 4px solid #555; padding: 15px; text-align: center; margin-bottom: 20px; z-index: 20; }
.error-msg { color: #ff0000; background: black; padding: 5px; margin-top: 10px; animation: blink 0.5s infinite; }

.stats-container { display: flex; gap: 20px; justify-content: center; }
.stat-box { display: flex; flex-direction: column; align-items: center; padding: 5px 10px; border: 2px solid #333; background: rgba(0,0,0,0.8); }
.stat-box.gain span:last-child { color: #44ff44; font-size: 1.2rem; margin-top: 5px;}
.stat-box.debt span:last-child { color: #ff4444; font-size: 1.2rem; margin-top: 5px;}

.post-it { position: absolute; top: 0px; left: -30px; width: 150px; background-color: #ffeb3b; color: #333; padding: 15px; font-family: 'Kalam', cursive, sans-serif; font-size: 0.9rem; box-shadow: 5px 5px 10px rgba(0,0,0,0.5); transform: rotate(-3deg); z-index: 5; }
.post-it li.done { text-decoration: line-through; color: #888; }

.work-area { display: flex; width: 100%; height: 80vh; align-items: center; justify-content: space-around; }
.conveyor-belt { width: 15%; height: 100%; background: rgba(51, 51, 51, 0.9); border-right: 10px solid #555; position: relative; overflow: hidden; }
.belt-track { position: absolute; width: 100%; height: 100%; background: repeating-linear-gradient(0deg, #333, #333 20px, #222 20px, #222 40px); animation: scrollBelt 1s linear infinite; z-index: 0; }
@keyframes scrollBelt { from { background-position: 0 0; } to { background-position: 0 40px; } }
.component-item { position: absolute; left: 50%; transform: translateX(-50%); background: rgba(255,255,255,0.1); border: 2px solid #fff; padding: 10px; cursor: grab; text-align: center; width: 90px; z-index: 2; }
.shape-icon { margin: 0 auto; border: 2px solid #000; }
.shape-icon.screen { width: 50px; height: 80px; background-color: #3498db; }
.comp-img { width: 50px; height: 50px; margin: 0 auto; display: block; }
.pixel-art { image-rendering: pixelated; }
.comp-name { display: block; font-size: 0.5rem; margin-top: 5px; background: rgba(0,0,0,0.5); }
.assembly-table { width: 70%; display: flex; justify-content: center; align-items: center; position: relative; height: 100%; }
.phone-case { width: 900px; height: 491px; background-size: contain; background-repeat: no-repeat; background-position: center; position: relative; box-shadow: 15px 15px 0 rgba(0,0,0,0.5); transition: transform 0.2s; image-rendering: pixelated; }
.phone-case:hover { transform: scale(1.01); }
.installed-part { position: absolute; transform: translate(-50%, -50%); }
.installed-part.cpu { top: 26%; left: 50%; width: 250px; height: 135px; z-index: 2; }
.installed-img { width: 100%; height: 100%; display: block; object-fit: contain; }
.installed-part.battery { top: calc(55% + 20px); left: 50%; width: 600px; height: 250px; z-index: 2; }
.installed-part.screen { top: 50%; left: 50%; width: 850px; height: 465px; z-index: 10; }

.result-zone { display: flex; flex-direction: column; align-items: center; margin-top: 50px; z-index: 100; }
.big-data-box { width: 80%; max-width: 500px; display: flex; flex-direction: column; gap: 10px; padding: 20px; background: rgba(0,0,0,0.9); }
.data-line { display: flex; justify-content: space-between; font-size: 1rem; }
.data-line.total { font-size: 1.4rem; margin-top: 10px; }
.separator { border: 1px dashed #555; width: 100%; margin: 10px 0; }

.highlight-red { color: #ff4444; }
.highlight-green { color: #44ff44; }
.highlight-white { color: #fff; }

.shock-text { margin-bottom: 30px; font-size: 0.8rem; line-height: 1.6; max-width: 450px; color: #fff; text-transform: uppercase; margin-top: 20px; background: rgba(0,0,0,0.7); padding: 10px; }
.restart-btn { background-color: #ff4444; color: white; border: 4px solid #fff; padding: 15px 30px; cursor: pointer; font-family: inherit; font-size: 1rem; margin-top: 20px;}
.restart-btn:hover { background-color: #cc0000; }
</style>
