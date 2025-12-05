<template>
  <div class="main-container login-background" :class="{ 'theme-linux': isLinuxInstalled, 'theme-windows': !isLinuxInstalled }">

    <div class="system-bar" v-if="!isLinuxInstalled">
      <div class="debug-area">
          <span style="color: #ccc; opacity: 0.5;">
            Input: {{ brokenMethod === 'NONE' ? 'MIRACLE' : brokenMethod + ' BROKEN' }} | Ads: {{ activeAds.length }} actifs
          </span>
      </div>
      <div class="status-icons">
        <span>{{ currentTime }}</span>
        <i class="icon-wifi"></i>
        <i class="icon-battery"></i>
        <i class="icon-accessibility"></i>
      </div>
    </div>

    <div v-if="isLinuxInstalled" class="linux-desktop gnome-desktop-bg">
      <div class="gnome-top-bar">
        <span class="center-time">{{ currentTime }}</span>
        <div class="status-right">
          <span><i class="icon-wifi"></i> 100%</span>
          <span><i class="icon-volume"></i></span>
          <span><i class="icon-user"></i></span>
        </div>
      </div>

      <div class="login-container">
        <div class="gnome-login-card">
          <img src="https://via.placeholder.com/120/58a6ff/0d1117?text=TUX" alt="Tux Profile" class="profile-pic linux-pic">

          <h1>Tux, le pingouin</h1>

          <p class="success-text">
            Système déverrouillé.<br>Profitez de la liberté.
          </p>

          <button @click="isLinuxInstalled = false" class="btn-primary linux-start-btn">
            Démarrer la session
          </button>
        </div>
      </div>
    </div>


    <div v-if="!isLinuxInstalled" class="login-container">
      <div class="login-card">

        <img src="https://via.placeholder.com/120/0078D7/FFFFFF?text=USER" alt="Profile Picture" class="profile-pic">

        <h1>Mot de passe</h1>

        <p class="warning-text">
          Windows {{ windowsVersion }} {{ currentEdition.name }}
        </p>

        <form @submit.prevent class="input-group">
          <div class="password-wrapper">
            <input
              ref="inputRef"
              id="password-field"
              type="password"
              v-model="inputValue"
              @input="handleInput"
              @keydown.enter="handleAction('ENTER')"
              :disabled="isSystemBusy"
              placeholder="Mot de passe"
              autocomplete="off"
            />

            <button
              type="button"
              class="unlock-btn"
              @mousedown="handleAction('CLICK')"
              :disabled="isSystemBusy"
            >
              <i class="icon-arrow-right"></i>
            </button>
          </div>
        </form>

        <p class="status-log" v-if="lastLog">{{ lastLog }}</p>

      </div>
    </div>


    <div v-if="!isLinuxInstalled && activeAds.length > 0" class="adware-layer-scattered">
      <div
        v-for="ad in activeAds"
        :key="ad.id"
        class="ad-banner-scattered widget-style"
        :style="{ top: ad.top, left: ad.left, right: ad.right, bottom: ad.bottom }"
      >
        <div class="ad-header widget-header">NOTIFICATION SPONSORISÉE <span @click="removeAd(ad.id)" class="ad-close">×</span></div>
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
            <div class="loader-ring"></div>

            <h2>{{ updateMessage }}</h2>

            <div class="progress-bar-wrapper">
              <div class="progress-bar-fill" :style="{ width: progress + '%' }"></div>
            </div>
            <h1>{{ progress }}%</h1>

            <p>N'éteignez pas l'ordinateur. Préparation du système pour les publicités.</p>
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
              <p>Je remarque que vous écrivez un mot de passe !</p>
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
            <span>Erreur Matériel</span>
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
            <span>Activation de Licence Requise</span>
            <button @click="closePaywall">×</button>
          </div>
          <div class="window-body">
            <div class="icon">🔒</div>
            <h3>Accès Bloqué !</h3>
            <p>Votre licence Windows n'est pas à jour. Vous ne pouvez pas vous connecter tant que vous n'avez pas procédé à la mise à niveau suivante :</p>
            <div class="upgrade-card">
              <h4>Passer à : Windows {{ nextWindowsVersion }} {{ nextEditionName }}</h4>
              <p>Inclus : {{ nextFeature }}</p>
              <p class="price">Prix : <strong>{{ nextPrice }}</strong></p>
              <button @click="buyUpgrade" class="btn-primary">Acheter la Licence et Redémarrer</button>
            </div>

            <div v-if="canInstallLinux" class="linux-option">
              <div class="divider">OU</div>
              <p class="hint-text">Dernière chance avant Windows {{ windowsVersion + 1 }}...</p>
              <button @click="installLinux" class="btn-linux-install">
                🐧 Installer Debian GNU/Linux (Gratuit)
              </button>
            </div>

            <button @click="closePaywall" class="btn-secondary link-style">
              Me rappeler plus tard (Verrouillage du PC)
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
const BSOD_ERRORS = ["CRITICAL_PROCESS_DIED", "IRQL_NOT_LESS_OR_EQUAL", "MEMORY_MANAGEMENT", "INACCESSIBLE_BOOT_DEVICE"];
const ADS_TEXTS = ["ACHETEZ UN PC NEUF !", "MAJ BIOS REQUISE", "VPN Gratuit (Pub)", "DÉBLOQUEZ L'ACCÈS PRO"];

// --- ÉTAT GLOBAL (REACTIF) ---
const windowsVersion = ref(10);
const editionIndex = ref(0);
const isLinuxInstalled = ref(false);
const brokenMethod = ref('CLICK');
const currentTime = ref(new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' }));
const commandOutput = ref('');

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

// MODIFIÉ: Rétabli le tableau pour les pop-ups dispersés
const activeAds = ref([]);
const showAdPopup = computed(() => activeAds.value.length > 0);

// --- PROPRIÉTÉS CALCULÉES (COMPUTED) ---
const currentEdition = computed(() => EDITIONS[editionIndex.value]);
const isEndOfCycle = computed(() => editionIndex.value === EDITIONS.length - 1);
const nextEditionIndex = computed(() => (editionIndex.value + 1) % EDITIONS.length);
const nextWindowsVersion = computed(() => isEndOfCycle.value ? windowsVersion.value + 1 : windowsVersion.value);
const nextEditionName = computed(() => EDITIONS[nextEditionIndex.value].name);
const nextPrice = computed(() => EDITIONS[nextEditionIndex.value].price);
const nextFeature = computed(() => EDITIONS[nextEditionIndex.value].feature);
const canInstallLinux = computed(() => isEndOfCycle.value);

// MODIFIÉ: Retrait des ads de la liste bloquante (ils sont non-bloquants visuellement)
const isSystemBusy = computed(() => overlayState.active || showPaywall.value || showErrorModal.value || showBingPopup.value);

const headerTitle = computed(() =>
  isLinuxInstalled.value
    ? 'Linux Desktop'
    : `Windows ${windowsVersion.value} Login`
);

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
  setInterval(() => {
    currentTime.value = new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
  }, 1000);
});

// --- LOGIQUE ADWARE (Pop-ups dispersés) ---

const spawnAds = (count) => {
  for (let i = 0; i < count; i++) {
    const isTop = Math.random() > 0.5;
    const isLeft = Math.random() > 0.5;

    activeAds.value.push({
      id: Date.now() + i,
      text: ADS_TEXTS[Math.floor(Math.random() * ADS_TEXTS.length)],
      top: isTop ? `${Math.random() * 20 + 5}%` : 'auto',
      bottom: !isTop ? `${Math.random() * 20 + 5}%` : 'auto',
      left: isLeft ? `${Math.random() * 20 + 5}%` : 'auto',
      right: !isLeft ? `${Math.random() * 20 + 5}%` : 'auto'
    });
  }
};

const removeAd = (id) => {
  // 50% de chance d'ouvrir une AUTRE pub au lieu de fermer
  if (Math.random() > 0.5) {
    spawnAds(1);
  } else {
    activeAds.value = activeAds.value.filter(ad => ad.id !== id);
  }
};

// --- LOGIQUE WINDOWS ---

// 1. Gestion de la frappe et IA (Bing/Clippy)
const handleInput = () => {
  if (isLinuxInstalled.value) return;
  keyPressCount.value++;

  let aiThreshold = 1.0;
  if (editionIndex.value === 2) aiThreshold = 0.7;
  else if (editionIndex.value > 2) aiThreshold = 0.9;

  if (Math.random() > aiThreshold && !showBingPopup.value) {
    showBingPopup.value = true;
    inputRef.value?.blur();
  }

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
        // MODIFIÉ: Ajoute 2 ou 3 pubs dispersées
        if (isAdDownload) {
          spawnAds(Math.floor(Math.random() * 2) + 2);
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

  nextTick(() => inputRef.value?.focus());
};

// 3. Actions (Connexion)
const handleAction = (method) => {
  if (isLinuxInstalled.value) {
    return;
  }

  if (method === brokenMethod.value) {
    errorModalText.value = method === 'ENTER'
      ? "Clavier non détecté. Veuillez acheter un clavier Surface."
      : "Souris incompatible. Clic sur le bouton d'accès désactivé.";
    showErrorModal.value = true;
  } else {
    showPaywall.value = true;
  }
};

// 4. Boucle d'Installation/Upgrade
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
  updateMessage.value = isLinux ? "Installation de la liberté..." : `Préparation de Windows ${nextWindowsVersion.value} pour l'activation...`;

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
      // Les publicités disparaissent en mode Linux
      activeAds.value = [];
      alert("Installation Linux terminée. Le système est déverrouillé.");
    } else {
      editionIndex.value++;
      if (editionIndex.value >= EDITIONS.length) {
        editionIndex.value = 0;
        windowsVersion.value++;
      }
      alert(`Activation réussie pour Windows ${windowsVersion.value} ${currentEdition.value.name}. Essayez de vous connecter à nouveau.`);
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
/* --- FONT & RESET --- */
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&family=Segoe+UI:wght@300;400;600;700&display=swap');

/* --- LAYOUT GLOBAL & THEME --- */
.main-container {
  min-height: 100vh;
  font-family: 'Segoe UI', Arial, sans-serif;
  transition: all 1s ease;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

/* Fond Windows (style Win 10/11) */
.login-background {
  background-color: #0078D7;
  background-image: linear-gradient(180deg, rgba(0, 120, 215, 0.8), rgba(0, 50, 100, 0.8));
  color: white;
  text-align: center;
}

/* --- INTERFACE LINUX (GNOME Login) --- */
.linux-desktop {
  flex: 1;
  background: #333d47;
  background-image: linear-gradient(180deg, #333d47, #1e242a);
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 10;
  color: white;
}

/* GNOME Top Bar */
.gnome-top-bar {
  background: rgba(0, 0, 0, 0.2);
  height: 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 10px;
  font-size: 0.9rem;
  position: absolute;
  top: 0;
  width: 100%;
}
.center-time { font-weight: bold; margin: 0 auto; }
.status-right span { margin-left: 15px; }

/* GNOME Card Styling */
.gnome-login-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: rgba(0, 0, 0, 0.25);
  padding: 60px 40px;
  border-radius: 12px;
  backdrop-filter: blur(5px);
  width: 350px;
  max-width: 90%;
}

.linux-pic {
  border-color: #58a6ff !important;
}

.linux-start-btn {
  background: #58a6ff;
  color: #1e1e1e;
  font-weight: bold;
  margin-top: 30px;
  padding: 10px 20px;
  border-radius: 5px;
}

/* --- BARRE D'ÉTAT WINDOWS --- */
.system-bar {
  position: absolute; bottom: 0; left: 0; right: 0; padding: 10px 40px; display: flex; justify-content: space-between; align-items: center; font-size: 0.9rem; background: rgba(0, 0, 0, 0.1); z-index: 100;
}
.debug-area { font-family: 'Fira Code', monospace; }
.status-icons i { font-size: 1.1rem; margin-left: 15px; display: inline-block; width: 1em; height: 1em; border: 1px solid white; border-radius: 2px; line-height: 1; text-align: center; }
.icon-wifi::before { content: 'W'; font-size: 0.7em; }
.icon-battery::before { content: 'B'; font-size: 0.7em; }
.icon-accessibility::before { content: 'A'; font-size: 0.7em; }
.icon-arrow-right::before { content: '>'; font-weight: bold; }

/* --- CARTE DE CONNEXION WINDOWS --- */
.login-container { flex: 1; display: flex; justify-content: center; align-items: center; padding-bottom: 80px; }
.login-card { display: flex; flex-direction: column; align-items: center; background: rgba(0, 0, 0, 0.15); padding: 40px; border-radius: 4px; backdrop-filter: blur(10px); width: 400px; max-width: 90%; }
.profile-pic { width: 120px; height: 120px; border-radius: 50%; margin-bottom: 20px; border: 4px solid rgba(255, 255, 255, 0.5); background-color: #0078D7; }
.login-card h1 { font-weight: 300; margin-bottom: 5px; }
.warning-text { font-size: 1.1rem; font-weight: 600; margin-bottom: 30px; color: #ffcc00; }
.input-group { width: 100%; display: flex; flex-direction: column; align-items: center; }
.password-wrapper { display: flex; align-items: center; width: 300px; max-width: 100%; margin-top: 15px; background: rgba(255, 255, 255, 0.1); border-radius: 3px; border-bottom: 2px solid transparent; transition: border-bottom-color 0.3s; }
.password-wrapper:focus-within { border-bottom-color: white; }
#password-field { background: transparent; border: none; color: white; font-size: 1.2rem; padding: 10px 15px; flex-grow: 1; outline: none; }
.unlock-btn { background: rgba(255, 255, 255, 0.2); border: none; color: white; padding: 10px 15px; font-size: 1.2rem; cursor: pointer; transition: background 0.2s; }
.unlock-btn:hover { background: rgba(255, 255, 255, 0.4); }
.unlock-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.status-log { margin-top: 20px; font-style: italic; font-size: 0.9rem; opacity: 0.7; max-width: 300px; }

/* --- ADS (ADWARE - Pop-ups dispersés) --- */
.adware-layer-scattered {
  position: fixed;
  inset: 0;
  z-index: 9050; /* Au-dessus de la carte de connexion */
  pointer-events: none; /* Permet le clic à travers la couche pour atteindre la carte */
}
.ad-banner-scattered {
  position: fixed; /* Utilise fixed pour la dispersion sur l'écran */
  width: 280px;
  background: rgba(43, 43, 43, 0.7); /* Fond légèrement transparent */
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
  font-family: 'Segoe UI', sans-serif;
  animation: bounce-in 0.5s;
  pointer-events: auto; /* Rétablit l'interactivité pour fermer la pub */
  border-radius: 8px;
  overflow: hidden;
  z-index: 9060; /* Assure que les ads sont au-dessus du login */
}
.widget-header { background: rgba(31, 31, 31, 0.8); color: #ccc; font-weight: 600; padding: 5px 10px; display: flex; justify-content: space-between; font-size: 0.8rem; cursor: default; }
.ad-close { cursor: pointer; }
.ad-content { padding: 15px; text-align: left; font-weight: 400; font-size: 1rem; color: #ffcc00; cursor: pointer; }


/* --- OVERLAYS & MODALS --- */
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
