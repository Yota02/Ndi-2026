<script setup lang="ts">
import { ref, computed } from 'vue'

const emit = defineEmits(['finish'])

// --- ETAPES DU SCÉNARIO ---
// 0 = Installation (Tout allumer)
// 1 = Recherche Google
// 2 = IA
// 3 = La Nuit (Tout éteindre... ou pas)
// 4 = Bilan
const etape = ref(0)

// --- VARIABLES ---
const co2 = ref(0.0)
const logMessage = ref("Le colis est arrivé.")

// Configuration de la nuit
const modeVeilleDesactive = ref(false) 

// LISTE DES APPAREILS (Au début tout est FALSE = Éteint/Gris)
const devices = ref([
    { id: 1, name: 'TV 4K', on: false, conso: 0.5 },
    { id: 2, name: 'PC GAMER', on: false, conso: 0.8 },
    { id: 3, name: 'DOUBLE ÉCRAN', on: false, conso: 0.3 },
    { id: 4, name: 'CONSOLE', on: false, conso: 0.2 },
    { id: 5, name: 'BOX FIBRE', on: true, conso: 0.1 } // La box reste souvent allumée
])

// Vérifie si tout est allumé pour passer à l'étape suivante
const toutEstAllume = computed(() => {
    // On regarde si tous les appareils (sauf la box qui l'est déjà) sont ON
    return devices.value.every(d => d.on)
})

// --- ACTIONS ---

function toggleDevice(index: number) {
    devices.value[index].on = !devices.value[index].on
}

function passerALaSuite() {
    etape.value = 1
    logMessage.value = "Tu es installé confortablement."
}

function faireRecherche() {
    co2.value += 0.5
    logMessage.value = "🔍 Recherche : 'Météo plage demain'"
    setTimeout(() => {
        etape.value = 2
        logMessage.value = "Tu veux une réponse plus complexe..."
    }, 1500)
}

function faireRechercheIA() {
    co2.value += 5.0
    logMessage.value = "🤖 IA : Génération d'une image de chat..."
    setTimeout(() => {
        etape.value = 3
        logMessage.value = "Il est 1h du matin. Tes yeux fatiguent."
    }, 2000)
}

function allerDormir() {
    // Calcul de la nuit
    let consoHeure = 0
    
    // On compte tout ce qui est resté ALLUMÉ (Vert)
    devices.value.forEach(d => {
        if (d.on) consoHeure += d.conso
    })

    if (modeVeilleDesactive.value) {
        consoHeure *= 2.5; 
    }

    const totalNuit = consoHeure * 8; // 8 heures de sommeil
    
    // Animation du score
    const interval = setInterval(() => {
        co2.value += 0.5
        if (co2.value >= totalNuit + 5.5) {
            clearInterval(interval)
            co2.value = totalNuit + 5.5
            etape.value = 4
        }
    }, 50)
}

function finirNiveau() {
    emit('finish')
}
</script>

<template>
  <div class="usage-zone">
    
    <div class="header-ui box-pixel">
        <h1 v-if="etape === 0">📦 LE DÉBALLAGE</h1>
        <h1 v-else>🏠 LE SALON</h1>
        
        <div class="stats-row">
            <span>
                <span v-if="etape === 0">18:00</span>
                <span v-else-if="etape < 3">20:00</span>
                <span v-else-if="etape === 3">01:00</span>
                <span v-else>09:00</span>
            </span>
            <span class="co2-score">CO2 : {{ co2.toFixed(1) }} g</span>
        </div>
    </div>

    <div class="interaction-area">
        
        <div v-if="etape === 0" class="setup-phase">
            <p class="intro-text">
                Ça y est ! L'Européen a reçu son nouveau téléphone et ses gadgets.<br>
                <br>
                <span class="blink">>>> ALLUME TOUT TON SETUP POUR COMMENCER <<<</span>
            </p>
            
            <div class="devices-grid">
                <div 
                    v-for="(device, index) in devices" 
                    :key="index"
                    class="device-btn box-pixel"
                    :class="{ 'is-on': device.on }"
                    @click="toggleDevice(index)"
                >
                    <div class="led"></div>
                    {{ device.name }}
                </div>
            </div>

            <button 
                v-if="toutEstAllume" 
                @click="passerALaSuite" 
                class="next-step-btn box-pixel"
            >
                COMMENCER À SCROLLER
            </button>
        </div>

        <div v-if="etape === 1" class="center-content">
            <p class="context-text">Tu es assis sur ton canapé. Tout est allumé.</p>
            <button @click="faireRecherche" class="action-btn google-btn box-pixel">
                🔍 FAIRE UNE RECHERCHE GOOGLE INUTILE
            </button>
        </div>

        <div v-if="etape === 2" class="center-content">
            <p class="context-text">Google ne suffit plus. Tu veux de la puissance.</p>
            <button @click="faireRechercheIA" class="action-btn ia-btn box-pixel">
                ✨ GÉNÉRER UNE IMAGE PAR IA (Gourmand)
            </button>
        </div>

        <div v-if="etape === 3" class="night-setup">
            <p class="context-text warning">
                Tu vas dormir. <br>
                Les appareils en <strong>VERT</strong> consomment encore.<br>
                Clique dessus pour les éteindre (si tu as le courage).
            </p>
            
            <div class="devices-grid">
                <div 
                    class="device-btn box-pixel special" 
                    :class="{ 'is-active': modeVeilleDesactive }"
                    @click="modeVeilleDesactive = !modeVeilleDesactive"
                >
                    <div class="checkbox">{{ modeVeilleDesactive ? '☒' : '☐' }}</div>
                    <span>MODE PERFORMANCE (Pas de veille)</span>
                </div>

                <div 
                    v-for="(device, index) in devices" 
                    :key="index"
                    class="device-btn box-pixel"
                    :class="{ 'is-on': device.on }"
                    @click="toggleDevice(index)"
                >
                    <div class="led"></div>
                    <span>{{ device.name }}</span>
                </div>
            </div>

            <button @click="allerDormir" class="sleep-btn box-pixel">
                💤 ALLER DORMIR
            </button>
        </div>

        <div v-if="etape === 4" class="result-box box-pixel">
            <h2>BILAN MATINAL</h2>
            <div class="data-grid">
                <div class="data-row">
                    <span>TA NUIT :</span>
                    <span class="red">{{ co2.toFixed(1) }} g CO2</span>
                </div>
                <div class="data-row">
                    <span>MOYENNE UE :</span>
                    <span class="white">~600 KG CO2 / AN</span>
                </div>
            </div>
            
            <p class="info-text">
                En Europe, on laisse souvent tout en veille.<br>
                La "pollution dormante" représente 10% de la conso électrique.
            </p>

            <button @click="finirNiveau" class="next-btn">DERNIÈRE ÉTAPE : LE RECYCLAGE >></button>
        </div>

    </div>

    <div class="log-console box-pixel">
        > {{ logMessage }}<span class="blink">_</span>
    </div>

  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

.usage-zone {
    min-height: 90vh;
    background-color: #111; 
    color: #eee;
    font-family: 'Press Start 2P', monospace;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
}

.box-pixel {
    background: #000;
    border: 4px solid #fff;
    padding: 15px;
    box-shadow: 4px 4px 0 #555;
    text-align: center;
}

/* HEADER */
.header-ui { width: 90%; margin-bottom: 30px; }
.stats-row { display: flex; justify-content: space-between; margin-top: 15px; font-size: 0.8rem; }
.co2-score { color: #ff5555; }

/* ZONE CENTRALE */
.interaction-area {
    flex-grow: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
}

.center-content { text-align: center; width: 100%; display: flex; flex-direction: column; align-items: center; }
.context-text { margin-bottom: 20px; font-size: 0.8rem; line-height: 1.5; color: #aaa; max-width: 500px; }
.intro-text { font-size: 0.7rem; line-height: 1.6; margin-bottom: 20px; text-align: center; }
.warning { color: #ff9999; }

/* GRILLE DES BOUTONS APPAREILS */
.devices-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
    margin-bottom: 20px;
    max-width: 600px;
}

.device-btn {
    width: 130px;
    padding: 15px 5px;
    cursor: pointer;
    font-size: 0.6rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    
    /* ÉTAT ÉTEINT (GRIS) */
    background-color: #333; 
    color: #888;
    border-color: #555;
    transition: all 0.2s;
}

/* ÉTAT ALLUMÉ (VERT) */
.device-btn.is-on {
    background-color: #004400;
    color: #00ff00;
    border-color: #00ff00;
    box-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
}

.led { width: 10px; height: 10px; background: #550000; border-radius: 50%; }
.is-on .led { background: #00ff00; box-shadow: 0 0 5px #00ff00; }

/* BOUTON OPTION SPÉCIAL */
.device-btn.special { width: 100%; flex-direction: row; justify-content: center; gap: 10px;}
.device-btn.special.is-active { background: #440000; color: #ff5555; border-color: #ff0000; }

/* BOUTONS ACTIONS */
.action-btn {
    font-family: inherit; font-size: 0.8rem; padding: 20px; cursor: pointer; color: black;
    width: 100%; max-width: 400px; border: 4px solid #fff;
}
.google-btn { background-color: #ddd; }
.ia-btn { background-color: #10a37f; color: white; border-color: #fff; animation: pulse 2s infinite; }
.next-step-btn { background: #00ff00; color: black; cursor: pointer; font-weight: bold; padding: 15px; margin-top: 20px; font-family: inherit;}
.sleep-btn { width: 100%; padding: 20px; background: #333; color: white; cursor: pointer; font-family: inherit; }
.sleep-btn:hover { background: #555; }

@keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.4); } 70% { box-shadow: 0 0 0 10px rgba(255, 255, 255, 0); } 100% { box-shadow: 0 0 0 0 rgba(255, 255, 255, 0); } }

/* RESULTATS */
.result-box { width: 90%; max-width: 500px; }
.data-grid { display: flex; flex-direction: column; gap: 15px; margin: 20px 0; border-bottom: 2px dashed #555; padding-bottom: 20px;}
.data-row { display: flex; justify-content: space-between; font-size: 0.8rem; }
.red { color: #ff5555; }
.white { color: #fff; }
.info-text { font-size: 0.7rem; line-height: 1.6; margin-bottom: 20px; text-align: left;}
.next-btn { background: #ff5555; color: white; border: 4px solid #fff; padding: 15px; cursor: pointer; font-family: inherit; width: 100%; }

/* LOG CONSOLE */
.log-console {
    width: 90%; margin-top: auto;
    font-size: 0.7rem; color: #00ff00; text-align: left;
    min-height: 50px; display: flex; align-items: center;
}
.blink { animation: blink 1s infinite; }
@keyframes blink { 50% { opacity: 0; } }
</style>