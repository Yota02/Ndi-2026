<template>
  <div class="main-container" :class="{ 'theme-linux': isLinuxInstalled, 'theme-windows': !isLinuxInstalled }">

    <header class="terminal-header">
      <div class="traffic-lights">
        <span class="red"></span><span class="yellow"></span><span class="green"></span>
      </div>
      <div class="title">
        {{ headerTitle }}
      </div>
    </header>

    <main class="terminal-body">
      <h1><span class="prompt">$</span> {{ currentScriptName }}</h1>

      <div class="mission-brief">
        <transition name="fade" mode="out-in">
          <div v-if="!isLinuxInstalled" key="win">
            <p>Système actuel : <strong>Windows {{ windowsVersion }} {{ currentEdition.name }}</strong></p>
            <p class="warning-text">⚠️ Support terminé. Mise à niveau requise.</p>
            <p class="debug-text" style="font-size: 0.7rem; color: #444;">(Debug: Input Status: {{ brokenMethod === 'NONE' ? 'MIRACLE MODE' : brokenMethod + ' BROKEN' }})</p>
          </div>
          <div v-else key="lin">
            <p class="success-text">✅ SYSTÈME LIBRE DEBIAN/LINUX INSTALLÉ.</p>
          </div>
        </transition>
      </div>

      <form @submit.prevent class="input-group">
        <label for="name-field">Identité du citoyen :</label>

        <div class="input-wrapper">
          <input
            ref="inputRef"
            id="name-field"
            type="text"
            v-model="inputValue"
            @input="handleInput"
            @keydown.enter="handleAction('ENTER')"
            :disabled="isSystemBusy && !isLinuxInstalled"
            placeholder="..."
            autocomplete="off"
            :class="{ 'glitch-effect': isLinuxInstalled }"
          />
          <span class="cursor">_</span>
        </div>

        <p class="status-log" v-if="lastLog">{{ lastLog }}</p>

        <button
          type="button"
          v-if="inputValue.length > 0"
          class="action-btn"
          @mousedown="handleAction('CLICK')"
        >
          {{ isLinuxInstalled ? 'sudo send_petition' : 'executer_formulaire.exe' }}
        </button>
      </form>
    </main>

    <template v-if="!isLinuxInstalled">

      <transition name="fade">
        <div v-if="overlayState.active" class="fullscreen-overlay" :class="overlayClass">

          <div v-if="overlayState.type === 'BSOD'" class="crash-content">
            <div class="sad-face">:(</div>
            <h2>Votre ordinateur a rencontré un problème.</h2>
            <div class="qr-section">
              <div class="qr-placeholder">QR</div>
              <div class="stop-code">
                <p>{{ progress }}% complet</p>
                <p>Code d'arrêt : {{ bsodErrorMsg }}</p>
              </div>
            </div>
          </div>

          <div v-else class="update-content">
            <div v-if="!overlayState.isLinux" class="loader-ring"></div>
            <div v-else class="loader-dots"></div>

            <h2>{{ updateMessage }}</h2>

            <div class="progress-bar-wrapper" v-if="overlayState.type === 'INSTALL'">
              <div class="progress-bar-fill" :style="{ width: progress + '%' }"></div>
            </div>
            <h1 v-else>{{ progress }}%</h1>

            <p v-if="!overlayState.isLinux">N'éteignez pas l'ordinateur.</p>
          </div>
        </div>
      </transition>

      <div v-if="showBingPopup" class="modal-backdrop-transparent">
        <transition name="bounce">
          <div class="clippy-popup shake-animation">
            <div class="clippy-header">
              <span>✨ Copilot AI Assistant</span>
              <button @click="showBingPopup = false">×</button>
            </div>
            <div class="clippy-body">
              <p>Je remarque que vous écrivez "<strong>{{ inputValue }}</strong>".</p>
              <p>Laissez l'IA générative optimiser votre pensée dans le Cloud !</p>
              <div class="clippy-actions">
                <button @click="acceptBing" class="btn-bing-primary">Oui (Recommandé)</button>
                <button @click="showBingPopup = false" class="btn-bing-secondary">Non (Risqué)</button>
              </div>
            </div>
          </div>
        </transition>
      </div>

      <div v-if="showErrorModal" class="modal-backdrop">
        <div class="windows-window error-window">
          <div class="window-header error-header">
            <span>Erreur Périphérique</span>
            <button @click="showErrorModal = false">×</button>
          </div>
          <div class="window-body">
            <div class="icon">🚫</div>
            <h3>Entrée non reconnue</h3>
            <p>{{ errorModalText }}</p>
            <button @click="showErrorModal = false" class="btn-secondary">Fermer</button>
          </div>
        </div>
      </div>

      <div v-if="showPaywall" class="modal-backdrop">
        <div class="windows-window">
          <div class="window-header">
            <span>Windows Update Center</span>
            <button @click="closePaywall">×</button>
          </div>
          <div class="window-body">
            <div class="icon">⚙️</div>
            <h3>Mise à niveau disponible</h3>
            <div class="upgrade-card">
              <h4>Passer à : Windows {{ nextWindowsVersion }} {{ nextEditionName }}</h4>
              <p>Inclus : {{ nextFeature }}</p>
              <p class="price">Prix : <strong>{{ nextPrice }}</strong></p>
              <button @click="buyUpgrade" class="btn-primary">Installer et Redémarrer</button>
            </div>

            <div v-if="canInstallLinux" class="linux-option">
              <div class="divider">OU</div>
              <p class="hint-text">C'est votre dernière chance avant Windows {{ windowsVersion + 1 }}...</p>
              <button @click="installLinux" class="btn-linux-install">
                🐧 Installer Debian GNU/Linux (Gratuit)
              </button>
            </div>

            <button @click="closePaywall" class="btn-secondary link-style">
              Me rappeler plus tard
            </button>
          </div>
        </div>
      </div>

    </template>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted, reactive } from 'vue';

// --- CONFIGURATION ---
const EDITIONS = [
  { slug: 'home', name: "Famille", price: "145,00 €", feature: "Pubs dans le menu Démarrer" },
  { slug: 'pro', name: "Professionnel", price: "259,00 €", feature: "BitLocker (Clé perdue)" },
  { slug: 'ent', name: "Entreprise", price: "Abonnement Mensuel", feature: "Télémétrie Avancée" },
  { slug: 'ult', name: "Ultimate", price: "439,00 €", feature: "Support Technique par IA" },
  { slug: 'ai', name: "AI Edition", price: "Vos Données Perso", feature: "Enregistrement d'écran 24/7" }
];
const BSOD_ERRORS = ["CRITICAL_PROCESS_DIED", "IRQL_NOT_LESS_OR_EQUAL", "MEMORY_MANAGEMENT"];

// --- ÉTAT GLOBAL ---
const windowsVersion = ref(10);
const editionIndex = ref(0);
const isLinuxInstalled = ref(false);
const brokenMethod = ref('CLICK'); // 'CLICK', 'ENTER', ou 'NONE' (Miracle)

// État des inputs
const inputValue = ref('');
const inputRef = ref(null);
const keyPressCount = ref(0);
const lastLog = ref('');

// Gestion des overlays
const overlayState = reactive({
  active: false,
  type: null,
  isLinux: false
});

const progress = ref(0);
const bsodErrorMsg = ref('');
const updateMessage = ref('');

// Modals
const showPaywall = ref(false);
const showBingPopup = ref(false);
const showErrorModal = ref(false);
const errorModalText = ref('');

// --- COMPUTED ---
const currentEdition = computed(() => EDITIONS[editionIndex.value]);

// Logique de la prochaine édition/version
const isEndOfCycle = computed(() => editionIndex.value === EDITIONS.length - 1);

const nextEditionIndex = computed(() => (editionIndex.value + 1) % EDITIONS.length);
const nextWindowsVersion = computed(() => isEndOfCycle.value ? windowsVersion.value + 1 : windowsVersion.value);

const nextEditionName = computed(() => EDITIONS[nextEditionIndex.value].name);
const nextPrice = computed(() => EDITIONS[nextEditionIndex.value].price);
const nextFeature = computed(() => EDITIONS[nextEditionIndex.value].feature);

// MODIFICATION : Linux dispo uniquement à la fin du cycle d'éditions
const canInstallLinux = computed(() => isEndOfCycle.value);

const isSystemBusy = computed(() => overlayState.active || showPaywall.value || showErrorModal.value || showBingPopup.value);

const headerTitle = computed(() =>
  isLinuxInstalled.value
    ? 'root@eco-linux:~ (Stable)'
    : `user@win-${windowsVersion.value}-${currentEdition.value.slug}: (Not Responding)`
);

const currentScriptName = computed(() => isLinuxInstalled.value ? './welcome_freedom.sh' : 'bloatware_installer.msi');

const overlayClass = computed(() => {
  if (overlayState.type === 'BSOD') return 'bsod-bg';
  if (overlayState.isLinux) return 'linux-install-bg';
  return 'windows-blue-bg';
});

// --- LOGIQUE DE ROTATION DES PANNES ---
const rotateBrokenMethod = () => {
  const rand = Math.random();
  if (rand < 0.45) {
    brokenMethod.value = 'CLICK'; // 45% Souris cassée
  } else if (rand < 0.90) {
    brokenMethod.value = 'ENTER'; // 45% Clavier cassé
  } else {
    brokenMethod.value = 'NONE';  // 10% Miracle (les deux marchent)
  }
  console.log(`[SYSTEM] New Input Config: ${brokenMethod.value} broken.`);
};

onMounted(() => {
  rotateBrokenMethod();
});

// --- LOGIQUE METIER ---

// 1. Gestion de la frappe
const handleInput = () => {
  if (isLinuxInstalled.value) return;
  keyPressCount.value++;

  // Bing intrusif (20%)
  if (Math.random() > 0.80 && !showBingPopup.value) {
    showBingPopup.value = true;
    inputRef.value?.blur();
  }

  // Update/BSOD aléatoire
  if (keyPressCount.value % (Math.floor(Math.random() * 3) + 5) === 0) {
    triggerSystemInterruption();
  }
};

// 2. Interruption système
const triggerSystemInterruption = () => {
  inputRef.value?.blur();
  progress.value = 0;
  overlayState.active = true;
  overlayState.isLinux = false;

  // 25% de chance de BSOD
  const willCrash = Math.random() < 0.25;

  if (willCrash) {
    overlayState.type = 'BSOD';
    bsodErrorMsg.value = BSOD_ERRORS[Math.floor(Math.random() * BSOD_ERRORS.length)];
    runProgressLoop(85, () => {
      setTimeout(() => {
        resetOverlay();
        inputValue.value = inputValue.value.slice(0, -3);
        lastLog.value = `[FATAL] ${bsodErrorMsg.value}. Données perdues.`;
      }, 3000);
    });
  } else {
    overlayState.type = 'UPDATE';
    const msgs = ["Optimisation...", "Téléchargement des pubs...", "Nettoyage du disque..."];
    updateMessage.value = msgs[Math.floor(Math.random() * msgs.length)];

    runProgressLoop(100, () => {
      setTimeout(resetOverlay, 500);
    });
  }
};

const runProgressLoop = (target, onComplete) => {
  let speed = overlayState.type === 'BSOD' ? 200 : 250;
  const interval = setInterval(() => {
    progress.value += Math.floor(Math.random() * 10) + 2;
    if (progress.value >= target) {
      progress.value = target;
      clearInterval(interval);
      onComplete();
    }
  }, speed);
};

const resetOverlay = () => {
  overlayState.active = false;
  overlayState.type = null;
  nextTick(() => inputRef.value?.focus());
};

// 3. Gestion des Actions (Validation)
const handleAction = (method) => {
  if (isLinuxInstalled.value) {
    alert("Votre pétition a été envoyée avec succès via un système libre !");
    return;
  }

  // Vérification de la méthode cassée
  if (method === brokenMethod.value) {
    // Si c'est cassé -> Erreur
    errorModalText.value = method === 'ENTER'
      ? "La touche ENTREE nécessite le module 'Legacy Input Driver'."
      : "Votre souris n'est pas certifiée 'Precision'. Clic désactivé.";
    showErrorModal.value = true;
  } else {
    // Si ça marche (ou si c'est un Miracle) -> On affiche le Paywall
    // C'est là la frustration : même si l'input marche, Windows veut de l'argent.
    showPaywall.value = true;
  }
};

// 4. Upgrade & Installation
const closePaywall = () => {
  showPaywall.value = false;
  triggerSystemInterruption(); // Punition
};

const buyUpgrade = () => {
  showPaywall.value = false;
  startInstall(false);
};

const installLinux = () => {
  showPaywall.value = false;
  startInstall(true);
};

const startInstall = (isLinux) => {
  overlayState.active = true;
  overlayState.type = 'INSTALL';
  overlayState.isLinux = isLinux;
  progress.value = 0;

  updateMessage.value = isLinux
    ? "Extraction du noyau..."
    : `Installation de Windows ${nextWindowsVersion.value}...`;

  const speed = isLinux ? 30 : 100;

  const interval = setInterval(() => {
    progress.value += 2;
    if (progress.value >= 100) {
      clearInterval(interval);
      finishInstall(isLinux);
    }
  }, speed);
};

const finishInstall = (isLinux) => {
  setTimeout(() => {
    resetOverlay();

    if (isLinux) {
      isLinuxInstalled.value = true;
      inputValue.value = "sudo apt-get install freedom";
      lastLog.value = "Root access granted.";
    } else {
      // Rotation des inputs cassés pour la nouvelle version
      rotateBrokenMethod();

      // Incrémentation version/édition
      editionIndex.value++;
      if (editionIndex.value >= EDITIONS.length) {
        editionIndex.value = 0;
        windowsVersion.value++;
      }

      alert(`Mise à jour réussie : Windows ${windowsVersion.value} ${currentEdition.value.name}`);
      inputValue.value = "";
      lastLog.value = "[SYSTEM] Drivers updated. Input methods reconfigured.";
    }
  }, 1000);
};

const acceptBing = () => {
  window.open('https://www.bing.com/search?q=acheter+licence+windows+pas+cher', '_blank');
  showBingPopup.value = false;
};
</script>

<style scoped>
/* --- THEMES --- */
.main-container {
  min-height: 100vh;
  font-family: 'Fira Code', monospace;
  transition: all 1s ease;
  display: flex; flex-direction: column;
}

.theme-windows { background-color: #1e1e1e; color: #00ff00; }
.theme-windows .terminal-header { background: #333; }
.theme-windows .btn-primary { background: #0078D7; color: white; }

.theme-linux { background-color: #0d1117; color: #58a6ff; }
.theme-linux .terminal-header { background: #161b22; border-bottom: 1px solid #30363d; }
.theme-linux .input-wrapper { border-color: #58a6ff; }
.theme-linux .action-btn { background: #238636; color: white; }

/* --- TERMINAL UI --- */
.terminal-header { padding: 10px; display: flex; align-items: center; }
.traffic-lights span { width: 12px; height: 12px; border-radius: 50%; display: inline-block; margin-right: 6px; }
.red { background: #ff5f56; } .yellow { background: #ffbd2e; } .green { background: #27c93f; }
.title { margin-left: 15px; font-size: 0.9rem; opacity: 0.7; }
.terminal-body { padding: 2rem; flex: 1; position: relative; }
.prompt { color: #27c93f; margin-right: 10px; }
.input-group { margin-top: 40px; max-width: 600px; }
.input-wrapper { display: flex; align-items: center; border-bottom: 2px solid #00ff00; transition: border-color 0.5s; }
input { background: transparent; border: none; color: inherit; font-family: inherit; font-size: 1.5rem; width: 100%; outline: none; }
.cursor { animation: blink 1s step-end infinite; font-size: 1.5rem; }
.action-btn { margin-top: 30px; background: #00ff00; color: black; border: none; padding: 12px 24px; font-weight: bold; cursor: pointer; font-size: 1rem; }
.warning-text { color: #ff9800; }
.success-text { color: #2ea043; font-weight: bold; }
.status-log { margin-top: 15px; color: #666; font-style: italic; font-size: 0.85rem; }

/* --- OVERLAYS FULLSCREEN --- */
.fullscreen-overlay {
  position: fixed; inset: 0; z-index: 9999;
  display: flex; flex-direction: column; justify-content: center; align-items: center;
  color: white; font-family: 'Segoe UI', sans-serif;
  text-align: center;
}

.bsod-bg { background-color: #0078D7; align-items: flex-start; padding: 0 15%; text-align: left; }
.windows-blue-bg { background-color: #0078D7; }
.linux-install-bg { background-color: #222; font-family: 'Fira Code', monospace; color: #00ff00; }

.sad-face { font-size: 8rem; margin-bottom: 20px; }
.qr-section { display: flex; gap: 20px; margin-top: 30px; align-items: center; }
.qr-placeholder { width: 80px; height: 80px; background: white; color: #0078D7; display: flex; align-items: center; justify-content: center; font-weight: bold; }

.loader-ring { width: 40px; height: 40px; border: 4px solid #fff; border-top-color: transparent; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 20px; }
.progress-bar-wrapper { width: 300px; height: 6px; background: rgba(255,255,255,0.2); margin-top: 20px; border-radius: 3px; overflow: hidden; }
.progress-bar-fill { height: 100%; background: white; transition: width 0.2s; }

/* --- MODALS --- */
.modal-backdrop, .modal-backdrop-transparent { position: fixed; inset: 0; background: rgba(0,0,0,0.6); z-index: 9000; display: flex; justify-content: center; align-items: center; }
.modal-backdrop-transparent { background: rgba(0,0,0,0.1); z-index: 8500; }

.windows-window { background: #f0f0f0; width: 450px; border: 1px solid #999; box-shadow: 0 20px 50px rgba(0,0,0,0.5); font-family: 'Segoe UI', sans-serif; color: black; }
.window-header { background: white; padding: 8px 12px; display: flex; justify-content: space-between; border-bottom: 1px solid #ccc; font-size: 0.9rem; }
.window-body { padding: 25px; text-align: center; }
.error-window { border: 2px solid #cc0000; }
.error-header { background: #ffcccc; color: #cc0000; }
.upgrade-card { background: white; border: 1px solid #ddd; padding: 15px; margin: 20px 0; border-radius: 4px; text-align: left; }
.upgrade-card h4 { color: #0078D7; margin: 0 0 5px 0; }
.price { font-size: 1.1rem; color: #333; margin-top: 10px; }

.linux-option { margin-top: 15px; padding-top: 15px; border-top: 1px solid #ccc; }
.hint-text { font-size: 0.8rem; color: #666; margin-bottom: 5px; font-style: italic; }
.btn-linux-install { width: 100%; background: #E95420; color: white; border: none; padding: 10px; cursor: pointer; font-weight: bold; }
.btn-primary { width: 100%; background: #0078D7; color: white; border: none; padding: 8px; margin-top: 10px; cursor: pointer; }
.btn-secondary { width: 100%; background: #e1e1e1; border: 1px solid #ccc; padding: 8px; margin-top: 10px; cursor: pointer; }
.link-style { background: none; border: none; text-decoration: underline; color: #666; }
.icon { font-size: 3rem; margin-bottom: 10px; }

/* --- BING POPUP --- */
.clippy-popup { width: 320px; background: white; border: 3px solid #0078D7; border-radius: 8px; font-family: 'Segoe UI', sans-serif; box-shadow: 0 15px 40px rgba(0,0,0,0.4); pointer-events: auto; }
.clippy-header { background: linear-gradient(90deg, #0078D7, #00C7FD); color: white; padding: 8px 12px; font-weight: bold; display: flex; justify-content: space-between; font-size: 0.9rem; }
.clippy-body { padding: 20px; font-size: 1rem; color: #333; line-height: 1.4; }
.clippy-actions { display: flex; flex-direction: column; gap: 10px; margin-top: 15px; }
.btn-bing-primary { background: #0078D7; color: white; border: none; padding: 10px; font-weight: bold; cursor: pointer; transition: transform 0.2s; }
.btn-bing-primary:hover { transform: scale(1.05); }
.btn-bing-secondary { background: transparent; border: 1px solid #ccc; color: #666; padding: 8px; cursor: pointer; font-size: 0.8rem; }

/* ANIMATIONS */
@keyframes spin { 100% { transform: rotate(360deg); } }
@keyframes blink { 50% { opacity: 0; } }
.shake-animation { animation: shake 0.5s cubic-bezier(.36,.07,.19,.97) both; }
@keyframes shake { 10%, 90% { transform: translate3d(-1px, 0, 0); } 20%, 80% { transform: translate3d(2px, 0, 0); } 30%, 50%, 70% { transform: translate3d(-4px, 0, 0); } 40%, 60% { transform: translate3d(4px, 0, 0); } }
.fade-enter-active, .fade-leave-active { transition: opacity 0.5s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
.bounce-enter-active { animation: bounce-in 0.5s; }
@keyframes bounce-in { 0% { transform: scale(0); } 50% { transform: scale(1.1); } 100% { transform: scale(1); } }
</style>
