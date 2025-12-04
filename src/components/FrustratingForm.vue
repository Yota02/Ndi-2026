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
            <p class="debug-text" style="font-size: 0.7rem; color: #444;">(Debug: Input: {{ brokenMethod === 'NONE' ? 'MIRACLE' : brokenMethod + ' BROKEN' }} | Ads: {{ activeAds.length }})</p>
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

    <div v-if="!isLinuxInstalled" class="adware-layer">
      <div
        v-for="ad in activeAds"
        :key="ad.id"
        class="ad-banner"
        :style="{ top: ad.top, left: ad.left, right: ad.right, bottom: ad.bottom }"
      >
        <div class="ad-header">Publicité <span @click="removeAd(ad.id)" class="ad-close">×</span></div>
        <div class="ad-content">{{ ad.text }}</div>
      </div>
    </div>

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

            <div class="progress-bar-wrapper">
              <div class="progress-bar-fill" :style="{ width: progress + '%' }"></div>
            </div>
            <h1>{{ progress }}%</h1>

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
              <p>L'édition Entreprise inclut l'optimisation neurale de vos pensées.</p>
              <div class="clippy-actions">
                <button @click="acceptBing" class="btn-bing-primary">Oui (Générer)</button>
                <button @click="showBingPopup = false" class="btn-bing-secondary">Non (Refuser le futur)</button>
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
              <p class="hint-text">Dernière chance avant Windows {{ windowsVersion + 1 }}...</p>
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

// --- DOCUMENTATION ET CONFIGURATION ---
const EDITIONS = [
  { slug: 'home', name: "Famille", price: "145,00 €", feature: "Pubs dans le menu Démarrer" },
  { slug: 'pro', name: "Professionnel", price: "259,00 €", feature: "BitLocker (Clé perdue)" },
  { slug: 'ent', name: "Entreprise", price: "Abonnement Mensuel", feature: "Télémétrie Avancée" },
  { slug: 'ult', name: "Ultimate", price: "439,00 €", feature: "Support Technique par IA" },
  { slug: 'ai', name: "AI Edition", price: "Vos Données Perso", feature: "Enregistrement d'écran 24/7" }
];
const BSOD_ERRORS = ["CRITICAL_PROCESS_DIED", "IRQL_NOT_LESS_OR_EQUAL", "MEMORY_MANAGEMENT", "INACCESSIBLE_BOOT_DEVICE"];
const ADS_TEXTS = ["GAGNEZ UN IPHONE 16 !!!", "Rencontrez des singles locaux", "NETTOYEZ VOTRE PC MAINTENANT", "Crypto : +4000% en 1h !"];

// --- ÉTAT GLOBAL (REACTIF) ---
const windowsVersion = ref(10);
const editionIndex = ref(0);
const isLinuxInstalled = ref(false);
const brokenMethod = ref('CLICK');
const activeAds = ref([]);

// Inputs
const inputValue = ref('');
const inputRef = ref(null);
const keyPressCount = ref(0);
const lastLog = ref('');

// Overlays (Écrans pleins)
const overlayState = reactive({
  active: false,
  type: null,
  isLinux: false
});

const progress = ref(0);
const bsodErrorMsg = ref('');
const updateMessage = ref('');

// Modals (Popups)
const showPaywall = ref(false);
const showBingPopup = ref(false);
const showErrorModal = ref(false);
const errorModalText = ref('');

// --- PROPRIÉTÉS CALCULÉES (COMPUTED) ---
const currentEdition = computed(() => EDITIONS[editionIndex.value]);
const isEndOfCycle = computed(() => editionIndex.value === EDITIONS.length - 1);
const nextEditionIndex = computed(() => (editionIndex.value + 1) % EDITIONS.length);
const nextWindowsVersion = computed(() => isEndOfCycle.value ? windowsVersion.value + 1 : windowsVersion.value);
const nextEditionName = computed(() => EDITIONS[nextEditionIndex.value].name);
const nextPrice = computed(() => EDITIONS[nextEditionIndex.value].price);
const nextFeature = computed(() => EDITIONS[nextEditionIndex.value].feature);
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

// --- LOGIQUE ROTATION PANNES ---
const rotateBrokenMethod = () => {
  const rand = Math.random();
  if (rand < 0.45) brokenMethod.value = 'CLICK';
  else if (rand < 0.90) brokenMethod.value = 'ENTER';
  else brokenMethod.value = 'NONE';
  console.log(`[SYSTEM] New Input Config: ${brokenMethod.value} broken.`);
};

onMounted(() => {
  rotateBrokenMethod();
});

// --- LOGIQUE METIER ---

// 1. Gestion de la frappe et IA (Bing/Clippy)
const handleInput = () => {
  if (isLinuxInstalled.value) return;
  keyPressCount.value++;

  // IA INTRUSIVE (Seuil basé sur l'édition)
  let aiThreshold = 1.0;
  if (editionIndex.value === 2) aiThreshold = 0.7;
  else if (editionIndex.value > 2) aiThreshold = 0.9;

  if (Math.random() > aiThreshold && !showBingPopup.value) {
    showBingPopup.value = true;
    inputRef.value?.blur();
  }

  // Update aléatoire
  if (keyPressCount.value % (Math.floor(Math.random() * 3) + 5) === 0) {
    triggerSystemInterruption();
  }
};

// 2. Interruption système (Update avec risque de BSOD "In-Process")
const triggerSystemInterruption = () => {
  inputRef.value?.blur();
  progress.value = 0;
  overlayState.active = true;
  overlayState.isLinux = false;
  overlayState.type = 'UPDATE';

  // FIX: Choix du message (augmentation de la fréquence de "Téléchargement des pubs...")
  const msgs = [
    "Optimisation...",
    "Nettoyage du disque...",
    "Configuration des mouchards...",
    "Téléchargement des pubs...", // 40% de chance
    "Téléchargement des pubs..."  // 40% de chance
  ];

  updateMessage.value = msgs[Math.floor(Math.random() * msgs.length)];
  const isAdDownload = updateMessage.value === "Téléchargement des pubs...";

  // Décision fatidique : Crash ou pas ?
  const willCrash = Math.random() < 0.25;
  const crashPoint = Math.floor(Math.random() * 20) + 75;

  const interval = setInterval(() => {
    progress.value += Math.floor(Math.random() * 5) + 1;

    // CRASH PENDANT LA MISE A JOUR
    if (willCrash && progress.value >= crashPoint) {
      clearInterval(interval);
      triggerBSOD();
      return;
    }

    // SUCCES
    if (progress.value >= 100) {
      progress.value = 100;
      clearInterval(interval);
      setTimeout(() => {
        resetOverlay();
        if (isAdDownload) spawnAds();
      }, 500);
    }
  }, 150);
};

const triggerBSOD = () => {
  overlayState.type = 'BSOD';
  bsodErrorMsg.value = BSOD_ERRORS[Math.floor(Math.random() * BSOD_ERRORS.length)];

  setTimeout(() => {
    resetOverlay();
    inputValue.value = inputValue.value.slice(0, -5);
    lastLog.value = `[FATAL] System halted at address 0xFFFA. Unsaved work lost.`;
  }, 4000);
};

const resetOverlay = () => {
  overlayState.active = false;
  overlayState.type = null;

  rotateBrokenMethod();

  nextTick(() => inputRef.value?.focus());
};

// --- GESTION DES PUBS (ADWARE) ---
const spawnAds = () => {
  const count = Math.floor(Math.random() * 2) + 2;
  for (let i = 0; i < count; i++) {
    const isTop = Math.random() > 0.5;
    const isLeft = Math.random() > 0.5;

    activeAds.value.push({
      id: Date.now() + i,
      text: ADS_TEXTS[Math.floor(Math.random() * ADS_TEXTS.length)],
      top: isTop ? `${Math.random() * 10 + 5}%` : 'auto',
      bottom: !isTop ? `${Math.random() * 10 + 5}%` : 'auto',
      left: isLeft ? `${Math.random() * 10 + 5}%` : 'auto',
      right: !isLeft ? `${Math.random() * 10 + 5}%` : 'auto'
    });
  }
};

const removeAd = (id) => {
  if (Math.random() > 0.5) {
    spawnAds();
  } else {
    activeAds.value = activeAds.value.filter(ad => ad.id !== id);
  }
};

// 3. Actions (gestion du mode cassé)
const handleAction = (method) => {
  if (isLinuxInstalled.value) { alert("Liberté !"); return; }

  if (method === brokenMethod.value) {
    errorModalText.value = method === 'ENTER'
      ? "Clavier non détecté. Veuillez acheter un clavier Surface."
      : "Souris incompatible. Veuillez mettre à jour le firmware.";
    showErrorModal.value = true;
  } else {
    showPaywall.value = true;
  }
};

// 4. Boucle d'Installation
const closePaywall = () => {
  showPaywall.value = false;
  rotateBrokenMethod();
  triggerSystemInterruption();
};

const buyUpgrade = () => { showPaywall.value = false; startInstall(false); };
const installLinux = () => { showPaywall.value = false; startInstall(true); };

const startInstall = (isLinux) => {
  overlayState.active = true;
  overlayState.type = 'INSTALL';
  overlayState.isLinux = isLinux;
  progress.value = 0;
  updateMessage.value = isLinux ? "Installation de la liberté..." : `Installation de Windows ${nextWindowsVersion.value}...`;

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
      activeAds.value = [];
    } else {
      editionIndex.value++;
      if (editionIndex.value >= EDITIONS.length) {
        editionIndex.value = 0;
        windowsVersion.value++;
      }
      alert(`Bienvenue sur Windows ${windowsVersion.value} ${currentEdition.value.name}`);
      inputValue.value = "";
    }
  }, 1000);
};

const acceptBing = () => {
  window.open('https://www.bing.com', '_blank');
  showBingPopup.value = false;
};
</script>

<style scoped>
/* --- STYLES GENERAUX --- */
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&family=Segoe+UI:wght@300;400;600&display=swap');

.main-container {
  min-height: 100vh;
  font-family: 'Fira Code', monospace;
  transition: all 1s ease;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}
.theme-windows { background-color: #1e1e1e; color: #00ff00; }
.theme-linux { background-color: #0d1117; color: #58a6ff; }
.theme-linux .terminal-header { background: #161b22; border-bottom: 1px solid #30363d; }
.theme-linux .input-wrapper { border-color: #58a6ff; }
.theme-linux .action-btn { background: #238636; color: white; }

/* TERMINAL */
.terminal-header { padding: 10px; display: flex; align-items: center; background: #333; }
.traffic-lights span { width: 12px; height: 12px; border-radius: 50%; display: inline-block; margin-right: 6px; }
.red { background: #ff5f56; } .yellow { background: #ffbd2e; } .green { background: #27c93f; }
.title { margin-left: 15px; font-size: 0.9rem; opacity: 0.7; }
.terminal-body { padding: 2rem; flex: 1; position: relative; }
.prompt { color: #27c93f; margin-right: 10px; }
.input-group { margin-top: 40px; max-width: 600px; }
.input-wrapper { display: flex; align-items: center; border-bottom: 2px solid #00ff00; transition: border-color 0.5s; }
input { background: transparent; border: none; color: inherit; font-family: inherit; font-size: 1.5rem; width: 100%; outline: none; }
.cursor { animation: blink 1s step-end infinite; font-size: 1.5rem; }
.action-btn { margin-top: 30px; background: #00ff00; color: black; border: none; padding: 12px 24px; font-weight: bold; cursor: pointer; }
.warning-text { color: #ff9800; }
.success-text { color: #2ea043; font-weight: bold; }
.status-log { margin-top: 15px; color: #666; font-style: italic; font-size: 0.85rem; }

/* --- ADS (ADWARE) --- */
.adware-layer {
  position: fixed;
  inset: 0;
  z-index: 9050;
  pointer-events: none;
}
.ad-banner {
  position: absolute;
  width: 200px;
  background: white;
  border: 3px solid red;
  color: black;
  box-shadow: 10px 10px 0px rgba(0,0,0,0.5);
  font-family: Arial, sans-serif;
  animation: bounce-in 0.5s;
  pointer-events: auto;
}
.ad-header { background: red; color: white; font-weight: bold; padding: 2px 5px; display: flex; justify-content: space-between; font-size: 0.8rem; cursor: move; }
.ad-close { cursor: pointer; }
.ad-content { padding: 20px; text-align: center; font-weight: bold; font-size: 1.1rem; color: blue; text-decoration: underline; cursor: pointer; }

/* --- OVERLAYS --- */
.fullscreen-overlay { position: fixed; inset: 0; z-index: 9999; display: flex; flex-direction: column; justify-content: center; align-items: center; color: white; font-family: 'Segoe UI', sans-serif; text-align: center; }
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
.linux-option { margin-top: 15px; padding-top: 15px; border-top: 1px solid #ccc; }
.hint-text { font-size: 0.8rem; color: #666; margin-bottom: 5px; font-style: italic; }
.btn-linux-install { width: 100%; background: #E95420; color: white; border: none; padding: 10px; cursor: pointer; font-weight: bold; }
.btn-primary { width: 100%; background: #0078D7; color: white; border: none; padding: 8px; margin-top: 10px; cursor: pointer; }
.btn-secondary { width: 100%; background: #e1e1e1; border: 1px solid #ccc; padding: 8px; margin-top: 10px; cursor: pointer; }
.icon { font-size: 3rem; margin-bottom: 10px; }

/* BING */
.clippy-popup { width: 320px; background: white; border: 3px solid #0078D7; border-radius: 8px; font-family: 'Segoe UI', sans-serif; box-shadow: 0 15px 40px rgba(0,0,0,0.4); pointer-events: auto; }
.clippy-header { background: linear-gradient(90deg, #0078D7, #00C7FD); color: white; padding: 8px 12px; font-weight: bold; display: flex; justify-content: space-between; font-size: 0.9rem; }
.clippy-body { padding: 20px; font-size: 1rem; color: #333; line-height: 1.4; }
.clippy-actions { display: flex; flex-direction: column; gap: 10px; margin-top: 15px; }
.btn-bing-primary { background: #0078D7; color: white; border: none; padding: 10px; font-weight: bold; cursor: pointer; }
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
