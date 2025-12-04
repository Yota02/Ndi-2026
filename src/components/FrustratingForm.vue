<template>
  <div class="linux-container">
    <header class="terminal-header">
      <div class="traffic-lights">
        <span class="red"></span><span class="yellow"></span><span class="green"></span>
      </div>
      <div class="title">user@eco-linux:~/petition/save_planet</div>
    </header>

    <main class="terminal-body">
      <h1><span class="prompt">$</span> ./abandon_proprietary_os.sh</h1>

      <div class="mission-brief">
        <p>Les mises à jour forcées consomment des TWh d'électricité inutilement.</p>
        <p>Prouvez votre patience. Signez la pétition pour passer au Libre.</p>
      </div>

      <div class="input-group">
        <label for="name-field">Entrez votre nom :</label>
        <div class="input-wrapper">
          <input
            ref="inputRef"
            id="name-field"
            type="text"
            v-model="inputValue"
            @input="handleInput"
            :disabled="isSystemBusy"
            placeholder="Tapez ici..."
            autocomplete="off"
          />
          <span class="cursor">_</span>
        </div>
        <p class="status-log" v-if="lastLog">{{ lastLog }}</p>
      </div>

      <button v-if="inputValue.length > 8" @click="submitForm" class="btn-linux">
        sudo submit
      </button>
    </main>

    <transition name="fade">
      <div v-if="isUpdating" class="windows-update-overlay">
        <div class="loader-ring"></div>
        <h2>Configuration des mises à jour de l'input...</h2>
        <h1>{{ progress }}% effectué</h1>
        <p>N'éteignez pas votre ordinateur.</p>
        <p class="subtext">Votre PC redémarrera plusieurs fois.</p>
      </div>
    </transition>

    <div v-if="showAssistant" class="clippy-popup">
      <div class="clippy-header">
        <span>Assistant Saisie</span>
        <button @click="closeAssistant" class="close-x">×</button>
      </div>
      <div class="clippy-body">
        <p>J'ai remarqué que vous essayez de taper "<strong>{{ inputValue }}</strong>".</p>
        <p>Voulez-vous plutôt rechercher ce terme sur Bing pour économiser de l'énergie ?</p>
        <div class="clippy-actions">
          <button @click="acceptBing">Oui (Recommandé)</button>
          <button @click="closeAssistant" class="btn-secondary">Non, je pollue</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue';

// --- ÉTATS ---
const inputValue = ref('');
const inputRef = ref(null);
const keyPressCount = ref(0);
const isSystemBusy = ref(false); // Bloque l'input
const isUpdating = ref(false);   // Affiche l'écran bleu
const progress = ref(0);         // Pourcentage de maj
const showAssistant = ref(false);
const lastLog = ref('');

// --- LOGIQUE DU PIÈGE ---

const handleInput = () => {
  keyPressCount.value++;

  // LOGIQUE 1 : Windows Update tous les 3 caractères
  if (keyPressCount.value % 3 === 0) {
    triggerFakeUpdate();
    return;
  }

  // LOGIQUE 2 : L'assistant apparaît aléatoirement au 5ème ou 8ème caractère
  if (keyPressCount.value === 5 || keyPressCount.value === 8) {
    if (Math.random() > 0.3) triggerAssistant();
  }
};

const triggerFakeUpdate = () => {
  // On bloque tout
  isSystemBusy.value = true;
  isUpdating.value = true;
  progress.value = 0;

  // On retire le focus pour embêter l'utilisateur
  if(inputRef.value) inputRef.value.blur();

  lastLog.value = "[SYSTEM] Critical Update Service triggered...";

  // Simulation de progression irrégulière (très frustrant)
  let interval = setInterval(() => {
    // Incrémentation aléatoire
    const jump = Math.floor(Math.random() * 15) + 1;
    progress.value += jump;

    // Parfois ça bloque à 99%
    if (progress.value > 99) progress.value = 99;

    // Fin de la mise à jour
    if (Math.random() > 0.85 && progress.value >= 90) {
      clearInterval(interval);
      finishUpdate();
    }
  }, 800);
};

const finishUpdate = () => {
  progress.value = 100;
  setTimeout(() => {
    isUpdating.value = false;
    isSystemBusy.value = false;
    lastLog.value = "[SYSTEM] Update installed. Drivers loaded. Ready.";

    // On remet le focus... mais on efface le dernier caractère (BUG Windows !)
    nextTick(() => {
      // Petite méchanceté supplémentaire :
      // On retire parfois le dernier caractère tapé à cause du "redémarrage"
      inputValue.value = inputValue.value.slice(0, -1);
      if(inputRef.value) inputRef.value.focus();
    });
  }, 1500); // Petit délai à 100%
};

// --- LOGIQUE ASSISTANT ---

const triggerAssistant = () => {
  showAssistant.value = true;
  // L'assistant ne bloque pas totalement, mais cache le champ
};

const closeAssistant = () => {
  showAssistant.value = false;
  // Pénalité : fermer l'assistant déclenche parfois une mise à jour
  if (Math.random() > 0.7) {
    setTimeout(triggerFakeUpdate, 500);
  }
};

const acceptBing = () => {
  alert("Ouverture de Edge... (C'est une blague, continuez à souffrir)");
  closeAssistant();
};

const submitForm = () => {
  alert("Bravo ! Vous avez vaincu l'obsolescence programmée. Linux installé.");
  window.location.reload();
};
</script>

<style scoped>
/* --- STYLE DE BASE (LINUX / ÉCO) --- */
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&family=Segoe+UI:wght@300;400;600&display=swap');

.linux-container {
  background-color: #1e1e1e;
  color: #00ff00; /* Vert Terminal */
  font-family: 'Fira Code', monospace;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 2rem;
  box-sizing: border-box;
  position: relative;
  overflow: hidden;
}

.terminal-header {
  display: flex;
  background: #333;
  padding: 10px;
  border-radius: 8px 8px 0 0;
  align-items: center;
}

.traffic-lights span {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  display: inline-block;
  margin-right: 6px;
}
.red { background: #ff5f56; }
.yellow { background: #ffbd2e; }
.green { background: #27c93f; }

.title {
  margin-left: 15px;
  color: #ccc;
  font-size: 0.9rem;
}

.terminal-body {
  border: 1px solid #333;
  border-top: none;
  padding: 2rem;
  flex-grow: 1;
  background: rgba(0, 0, 0, 0.9);
}

.prompt { color: #27c93f; font-weight: bold; margin-right: 10px; }

.input-group {
  margin-top: 50px;
  display: flex;
  flex-direction: column;
  max-width: 500px;
}

label {
  margin-bottom: 10px;
  color: #aaa;
}

.input-wrapper {
  display: flex;
  align-items: center;
  border-bottom: 2px solid #00ff00;
}

input {
  background: transparent;
  border: none;
  color: white;
  font-family: 'Fira Code', monospace;
  font-size: 1.5rem;
  width: 100%;
  outline: none;
}

.cursor {
  animation: blink 1s step-end infinite;
  font-size: 1.5rem;
}

.status-log {
  margin-top: 20px;
  font-size: 0.8rem;
  color: #666;
  font-style: italic;
}

.btn-linux {
  margin-top: 30px;
  background: #00ff00;
  color: black;
  border: none;
  padding: 10px 20px;
  font-family: 'Fira Code', monospace;
  font-weight: bold;
  cursor: pointer;
}

@keyframes blink { 50% { opacity: 0; } }

/* --- LE STYLE GAFAM (WINDOWS UPDATE) --- */

.windows-update-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: #0078D7; /* Le Bleu de la mort / MAJ */
  color: white;
  font-family: 'Segoe UI', sans-serif;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  cursor: wait;
}

.windows-update-overlay h1 { font-weight: 300; font-size: 3rem; margin: 10px 0; }
.windows-update-overlay h2 { font-weight: 400; font-size: 1.2rem; margin-top: 20px; }
.windows-update-overlay p { font-size: 1rem; opacity: 0.8; }
.subtext { margin-top: 40px; font-size: 0.8rem !important; opacity: 0.6; }

/* Loader circulaire Windows style */
.loader-ring {
  display: inline-block;
  width: 60px;
  height: 60px;
  margin-bottom: 20px;
}
.loader-ring:after {
  content: " ";
  display: block;
  width: 44px;
  height: 44px;
  margin: 8px;
  border-radius: 50%;
  border: 4px solid #fff;
  border-color: #fff transparent #fff transparent;
  animation: ring 1.2s linear infinite;
}
@keyframes ring {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* --- LE STYLE POPUP ASSISTANT --- */
.clippy-popup {
  position: absolute;
  bottom: 20%;
  right: 10%;
  width: 300px;
  background: white;
  border: 1px solid #ccc;
  box-shadow: 0 4px 15px rgba(0,0,0,0.3);
  font-family: 'Segoe UI', sans-serif;
  color: #333;
  z-index: 5000;
  border-radius: 4px;
}

.clippy-header {
  background: #f1f1f1;
  padding: 5px 10px;
  display: flex;
  justify-content: space-between;
  border-bottom: 1px solid #ddd;
  font-size: 0.8rem;
}

.clippy-body { padding: 15px; font-size: 0.9rem; }
.clippy-actions { margin-top: 10px; display: flex; gap: 10px; }

.clippy-actions button {
  flex: 1;
  padding: 5px;
  cursor: pointer;
  background: #0078D7;
  color: white;
  border: none;
}
.clippy-actions .btn-secondary { background: #ccc; color: #333; }

/* Transitions Vue */
.fade-enter-active, .fade-leave-active { transition: opacity 0.5s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
