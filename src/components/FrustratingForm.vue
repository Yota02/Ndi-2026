<template>
  <div class="main-container login-background" :class="{ 'theme-linux': isLinuxInstalled, 'theme-windows': !isLinuxInstalled }">

    <transition name="interface-fade" mode="out-in">
      <ContactPage
        :key="isLinuxInstalled"
        :isLinuxInstalled="isLinuxInstalled"
        :windowsVersion="windowsVersion"
        :currentEdition="currentEdition"
        :brokenMethod="brokenMethod"
        :inputValue="inputValue"
        :emailValue="emailValue"
        :lastLog="lastLog"
        :isSystemBusy="isSystemBusy"
        :currentTime="currentTime"
        @update:inputValue="inputValue = $event"
        @update:emailValue="emailValue = $event"
        @trigger-frustration="triggerFrustration"
        @action-trigger="handleAction"
        @start-session="isLinuxInstalled = false"
      />
    </transition>

    <div class="system-bar" v-if="!isLinuxInstalled">
      <div class="debug-area">
          <span style="color: #ccc; opacity: 0.5;">
            Input: {{ brokenMethod === 'NONE' ? 'MIRACLE' : brokenMethod + ' BROKEN' }}
          </span>
      </div>
      <div class="status-icons">
        <span>{{ currentTime }}</span>
        <i class="icon-wifi"></i>
        <i class="icon-battery"></i>
        <i class="icon-accessibility"></i>
      </div>
    </div>

    <Overlays
      :overlayState="overlayState"
      :progress="progress"
      :bsodErrorMsg="bsodErrorMsg"
      :updateMessage="updateMessage"
      :showBingPopup="showBingPopup"
      :showErrorModal="showErrorModal"
      :errorModalText="errorModalText"
      :showPaywall="showPaywall"
      :adQueue="adQueue"
      :nextWindowsVersion="nextWindowsVersion"
      :nextEditionName="nextEditionName"
      :nextPrice="nextPrice"
      :nextFeature="nextFeature"
      :canInstallLinux="canInstallLinux"
      :bingContextValue="emailValue"
      @close-bing="showBingPopup = false"
      @accept-bing="acceptBing"
      @close-error="showErrorModal = false"
      @close-paywall="closePaywall"
      @buy-upgrade="buyUpgrade"
      @install-linux="installLinux"
      @close-ad="closeAdPopup"
    />

  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue';

// Importation des composants
import ContactPage from '../components/ContactPage.vue';
import Overlays from '../components/Overlays.vue';

// --- CONFIGURATION ---
const EDITIONS = [
  { slug: 'home', name: "Famille", price: "145,00 €", feature: "Pubs dans le menu Démarrer" },
  { slug: 'pro', name: "Professionnel", price: "259,00 €", feature: "BitLocker (Clé perdue)" },
  { slug: 'ent', name: "Entreprise", price: "Abonnement Mensuel", feature: "Télémétrie Avancée" },
  { slug: 'ult', name: "Ultimate", price: "439,00 €", feature: "Support Technique par IA" },
  { slug: 'ai', name: "AI Edition", price: "Vos Données Perso", feature: "Enregistrement d'écran 24/7" }
];
const BSOD_ERRORS = ["CRITICAL_PROCESS_DIED", "IRQL_NOT_LESS_OR_EQUAL", "MEMORY_MANAGEMENT", "INACCESSIBLE_BOOT_DEVICE"];
const ADS_TEXTS = ["ACHETEZ UN PC NEUF !", "MAJ BIOS REQUISE", "VPN Gratuit (Pub)", "DÉBLOQUEZ L'ACCÈS PRO"];

// --- ÉTAT GLOBAL (REACTIF) ---
const windowsVersion = ref(10);
const editionIndex = ref(0);
const isLinuxInstalled = ref(false);
const brokenMethod = ref('CLICK');
const currentTime = ref(new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' }));

const inputValue = ref('');
const emailValue = ref(''); // NOUVEAU: Champ Email
const keyPressCount = ref(0);
const lastLog = ref('');

// Overlays (Écrans pleins)
const overlayState = reactive({
  active: false,
  type: null, // 'UPDATE', 'BSOD', 'INSTALL'
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
const adQueue = ref([]);
const showAdPopup = computed(() => adQueue.value.length > 0);


// --- PROPRIÉTÉS CALCULÉES (COMPUTED) ---
const currentEdition = computed(() => EDITIONS[editionIndex.value]);
const isEndOfCycle = computed(() => editionIndex.value === EDITIONS.length - 1);
const nextEditionIndex = computed(() => (editionIndex.value + 1) % EDITIONS.length);
const nextWindowsVersion = computed(() => isEndOfCycle.value ? windowsVersion.value + 1 : windowsVersion.value);
const nextEditionName = computed(() => EDITIONS[nextEditionIndex.value].name);
const nextPrice = computed(() => EDITIONS[nextEditionIndex.value].price);
const nextFeature = computed(() => EDITIONS[nextEditionIndex.value].feature);
const canInstallLinux = computed(() => true);
const isSystemBusy = computed(() => overlayState.active || showPaywall.value || showErrorModal.value || showBingPopup.value);


// --- LOGIQUE CORE ---

const rotateBrokenMethod = () => {
  const rand = Math.random();
  if (rand < 0.45) brokenMethod.value = 'CLICK';
  else if (rand < 0.90) brokenMethod.value = 'ENTER';
  else brokenMethod.value = 'NONE';
  console.log(`[SYSTEM] New Input Config: ${brokenMethod.value} broken.`);
};

// Logique de Frustration (Déclenchée par les deux inputs)
const triggerFrustration = () => {
  keyPressCount.value++;

  let aiThreshold = 1.0;
  if (editionIndex.value === 2) aiThreshold = 0.7;
  else if (editionIndex.value > 2) aiThreshold = 0.9;

  if (Math.random() > aiThreshold && !showBingPopup.value) {
    showBingPopup.value = true;
  }

  if (keyPressCount.value % (Math.floor(Math.random() * 3) + 5) === 0) {
    triggerSystemInterruption();
  }
};

// Logique pour l'action de soumission
const handleAction = (method) => {
  if (method === brokenMethod.value) {
    errorModalText.value = method === 'ENTER'
      ? "Clavier non détecté. Veuillez acheter un clavier Surface."
      : "Souris incompatible. Clic sur le bouton d'accès désactivé.";
    showErrorModal.value = true;
  } else {
    showPaywall.value = true;
  }
};

const triggerAdPopup = (count) => {
  for (let i = 0; i < count; i++) {
    adQueue.value.push(ADS_TEXTS[Math.floor(Math.random() * ADS_TEXTS.length)]);
  }
};

const closeAdPopup = () => {
  adQueue.value.shift();
};

const triggerSystemInterruption = () => {
  progress.value = 0;
  overlayState.active = true;
  overlayState.isLinux = false;
  overlayState.type = 'UPDATE';

  const msgs = [
    "Optimisation...",
    "Nettoyage du disque...",
    "Configuration des mouchards...",
    "Téléchargement des pubs...",
    "Téléchargement des pubs..."
  ];

  updateMessage.value = msgs[Math.floor(Math.random() * msgs.length)];
  const isAdDownload = updateMessage.value === "Téléchargement des pubs...";

  const willCrash = Math.random() < 0.25;
  const crashPoint = Math.floor(Math.random() * 20) + 75;

  const interval = setInterval(() => {
    progress.value += Math.floor(Math.random() * 5) + 1;

    if (willCrash && progress.value >= crashPoint) {
      clearInterval(interval);
      triggerBSOD();
      return;
    }

    if (progress.value >= 100) {
      progress.value = 100;
      clearInterval(interval);
      setTimeout(() => {
        resetOverlay();
        if (isAdDownload) {
          triggerAdPopup(Math.floor(Math.random() * 2) + 2);
        }
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
    lastLog.value = `[FATAL] System halted at address 0xFFFA. Accès refusé.`;
  }, 4000);
};

const resetOverlay = () => {
  overlayState.active = false;
  overlayState.type = null;
  rotateBrokenMethod();
};

const acceptBing = () => {
  window.open('https://www.bing.com', '_blank');
  showBingPopup.value = false;
};

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
  const updateMsg = isLinux ? "Installation de la liberté..." : `Préparation de Windows ${nextWindowsVersion.value} pour l'activation...`;
  updateMessage.value = updateMsg;

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
    } else {
      editionIndex.value++;
      if (editionIndex.value >= EDITIONS.length) {
        editionIndex.value = 0;
        windowsVersion.value++;
      }
      alert(`Activation réussie pour Windows ${windowsVersion.value} ${currentEdition.value.name}. Contactez-nous.`);

      inputValue.value = "";
      emailValue.value = "";
    }
  }, 1000);
};

// Initialisation de l'heure
onMounted(() => {
  setInterval(() => {
    currentTime.value = new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
  }, 1000);
});
</script>

<style>
/* CSS GLOBAL ET PARTAGÉ */
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&family=Segoe+UI:wght@300;400;600;700&display=swap');

/* Style de transition global pour le composant ContactPage */
.interface-fade-enter-active,
.interface-fade-leave-active {
  transition: opacity 0.5s ease, transform 0.5s ease;
  position: absolute; /* Permet le cross-fade */
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
}
.interface-fade-enter-from {
  opacity: 0;
  transform: scale(0.95);
}
.interface-fade-leave-to {
  opacity: 0;
  transform: scale(1.05);
}

.main-container {
  min-height: 100vh;
  font-family: 'Segoe UI', Arial, sans-serif;
  transition: all 1s ease;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

/* Fond Windows */
.login-background {
  background-color: #0078D7;
  background-image: linear-gradient(180deg, rgba(0, 120, 215, 0.8), rgba(0, 50, 100, 0.8));
  color: white;
  text-align: center;
}

/* --- STYLES COMMUNS AUX OVERLAYS --- */
.fullscreen-overlay { position: fixed; inset: 0; z-index: 9999; display: flex; flex-direction: column; justify-content: center; align-items: center; color: white; font-family: 'Segoe UI', sans-serif; text-align: center; }
.bsod-bg { background-color: #0078D7; align-items: flex-start; padding: 0 15%; text-align: left; }
.windows-blue-bg { background-color: #0078D7; }
.linux-install-bg { background-color: #222; font-family: 'Fira Code', monospace; color: #00ff00; }
.sad-face { font-size: 8rem; margin-bottom: 20px; }
.qr-section { display: flex; gap: 20px; margin-top: 30px; align-items: center; }
.qr-placeholder { width: 80px; height: 80px; background: white; color: #0078D7; display: flex; align-items: center; justify-content: center; font-weight: bold; }
.loader-ring { width: 40px; height: 40px; border: 4px solid #fff; border-top-color: transparent; border-radius: 50%; margin: 0 auto 20px; animation: spin 1s linear infinite; }
.progress-bar-wrapper { width: 300px; height: 6px; background: rgba(255,255,255,0.2); margin: 20px auto 0 auto; border-radius: 3px; overflow: hidden; }
.progress-bar-fill { height: 100%; background: white; transition: width 0.2s; }
.modal-backdrop, .modal-backdrop-transparent { position: fixed; inset: 0; background: rgba(0,0,0,0.6); z-index: 9000; display: flex; justify-content: center; align-items: center; }
.modal-backdrop-transparent { background: rgba(0,0,0,0.1); z-index: 8500; }
.windows-window { background: #f0f0f0; width: 450px; border: 1px solid #999; box-shadow: 0 20px 50px rgba(0,0,0,0.5); font-family: 'Segoe UI', sans-serif; color: black; border-radius: 8px; }
.window-header { background: white; padding: 8px 12px; display: flex; justify-content: space-between; border-bottom: 1px solid #ccc; font-size: 0.9rem; border-top-left-radius: 8px; border-top-right-radius: 8px; }
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
.clippy-popup { width: 320px; background: white; border: 3px solid #0078D7; border-radius: 8px; font-family: 'Segoe UI', sans-serif; box-shadow: 0 15px 40px rgba(0,0,0,0.4); pointer-events: auto; }
.clippy-header { background: linear-gradient(90deg, #0078D7, #00C7FD); color: white; padding: 8px 12px; font-weight: bold; display: flex; justify-content: space-between; font-size: 0.9rem; }
.clippy-body { padding: 20px; font-size: 1rem; color: #333; line-height: 1.4; }
.clippy-actions { display: flex; flex-direction: column; gap: 10px; margin-top: 15px; }
.btn-bing-primary { background: #0078D7; color: white; border: none; padding: 10px; font-weight: bold; cursor: pointer; }
.btn-bing-secondary { background: transparent; border: 1px solid #ccc; color: #666; padding: 8px; cursor: pointer; font-size: 0.8rem; }
@keyframes spin { 100% { transform: rotate(360deg); } }
@keyframes blink { 50% { opacity: 0; } }
.shake-animation { animation: shake 0.5s cubic-bezier(.36,.07,.19,.97) both; }
@keyframes shake { 10%, 90% { transform: translate3d(-1px, 0, 0); } 20%, 80% { transform: translate3d(2px, 0, 0); } 30%, 50%, 70% { transform: translate3d(-4px, 0, 0); } 40%, 60% { transform: translate3d(4px, 0, 0); } }
.fade-enter-active, .fade-leave-active { transition: opacity 0.5s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
.bounce-enter-active { animation: bounce-in 0.5s; }
@keyframes bounce-in { 0% { transform: scale(0); } 50% { transform: scale(1.1); } 100% { transform: scale(1); } }
</style>
