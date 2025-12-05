<template>
  <div>
    <div v-if="!overlayState.isLinux && adQueue.length > 0" class="adware-layer-scattered">
      <transition-group name="fade">
        <div
          v-for="(adText, index) in adQueue"
          :key="index"
          v-show="index === 0"
          class="windows-window ad-popup-styled"
          :style="getRandomAdStyle(index)"
        >
          <div class="window-header ad-header-styled">
            <span>NOTIFICATION SPONSORISÉE</span>
            <button @click="$emit('close-ad')" class="ad-close-btn">×</button>
          </div>
          <div class="window-body ad-content-styled">
            <div class="ad-icon">{{ getAdIcon(adText) }}</div>
            <h3>{{ adText }}</h3>
            <p class="ad-info">Pour plus d'informations, cliquez ici.</p>
            <button @click="$emit('close-ad')" class="btn-primary ad-action-btn">
              Ouvrir (Requis)
            </button>
          </div>
        </div>
      </transition-group>
    </div>

    <template v-if="overlayState.active || showPaywall || showErrorModal || showBingPopup">

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
            <div :class="{'loader-ring': !overlayState.isLinux}"></div>

            <h2>{{ updateMessage }}</h2>

            <div class="progress-bar-wrapper">
              <div class="progress-bar-fill" :class="{'linux-bar': overlayState.isLinux}" :style="{ width: progress + '%' }"></div>
            </div>

            <h1 v-if="!overlayState.isLinux">{{ progress }}%</h1>
            <p v-if="!overlayState.isLinux">N'éteignez pas l'ordinateur. Préparation du système pour les publicités.</p>
            <p v-else style="color: white; font-family: 'Fira Code', monospace;">Installation en cours... (ne touchez à rien)</p>
          </div>
        </div>
      </transition>

      <div v-if="showBingPopup" class="modal-backdrop-transparent">
        <transition name="bounce">
          <div class="clippy-popup shake-animation">
            <div class="clippy-header">
              <span>✨ Copilot AI Assistant</span>
              <button @click="$emit('close-bing')">×</button>
            </div>
            <div class="clippy-body">
              <p>Je remarque que vous écrivez: "<strong>{{ bingContextValue }}</strong>".</p>
              <p>L'édition Entreprise inclus l'optimisation neurale de vos pensées.</p>
              <div class="clippy-actions">
                <button @click="$emit('accept-bing')" class="btn-bing-primary">Oui (Générer)</button>
                <button @click="$emit('close-bing')" class="btn-bing-secondary">Non (Refuser le futur)</button>
              </div>
            </div>
          </div>
        </transition>
      </div>

      <div v-if="showErrorModal" class="modal-backdrop">
        <div class="windows-window error-window">
          <div class="window-header error-header">
            <span>Erreur Matériel</span>
            <button @click="$emit('close-error')">×</button>
          </div>
          <div class="window-body">
            <div class="icon">🚫</div>
            <h3>Entrée non reconnue</h3>
            <p>{{ errorModalText }}</p>
            <button @click="$emit('close-error')" class="btn-secondary">Fermer</button>
          </div>
        </div>
      </div>

      <div v-if="showPaywall" class="modal-backdrop">
        <div class="windows-window">
          <div class="window-header">
            <span>Activation de Licence Requise</span>
            <button @click="$emit('close-paywall')">×</button>
          </div>
          <div class="window-body">
            <div class="icon">🔒</div>
            <h3>Accès Bloqué !</h3>
            <p>Votre licence Windows n'est pas à jour. Vous ne pouvez pas soumettre de requête tant que vous n'avez pas procédé à la mise à niveau suivante :</p>
            <div class="upgrade-card">
              <h4>Passer à : Windows {{ nextWindowsVersion }} {{ nextEditionName }}</h4>
              <p>Inclus : {{ nextFeature }}</p>
              <p class="price">Prix : <strong>{{ nextPrice }}</strong></p>
              <button @click="$emit('buy-upgrade')" class="btn-primary">Acheter la Licence et Redémarrer</button>
            </div>

            <div v-if="canInstallLinux" class="linux-option">
              <div class="divider">OU</div>
              <p class="hint-text">Dernière chance avant Windows {{ nextWindowsVersion }}...</p>
              <button @click="$emit('install-linux')" class="btn-linux-install">
                🐧 Installer Debian GNU/Linux (Gratuit)
              </button>
            </div>

            <button @click="$emit('close-paywall')" class="btn-secondary link-style">
              Me rappeler plus tard (Verrouillage du PC)
            </button>
          </div>
        </div>
      </div>

    </template>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, computed } from 'vue';

const props = defineProps({
  overlayState: Object,
  progress: Number,
  bsodErrorMsg: String,
  updateMessage: String,
  showBingPopup: Boolean,
  showErrorModal: Boolean,
  errorModalText: String,
  showPaywall: Boolean,
  adQueue: Array,
  nextWindowsVersion: Number,
  nextEditionName: String,
  nextPrice: String,
  nextFeature: String,
  canInstallLinux: Boolean,
  bingContextValue: String,
});

defineEmits([
  'close-bing', 'accept-bing', 'close-error', 'close-paywall',
  'buy-upgrade', 'install-linux', 'close-ad'
]);

const overlayClass = computed(() => {
  if (props.overlayState.type === 'BSOD') return 'bsod-bg';
  if (props.overlayState.isLinux) return 'linux-install-bg';
  return 'windows-blue-bg';
});

// Génère un style aléatoire (position) pour chaque popup Adware
const getRandomAdStyle = (index) => {
  if (index > 0) return {};

  const isTop = Math.random() > 0.5;
  const isLeft = Math.random() > 0.5;

  return {
    top: isTop ? `${Math.random() * 20 + 5}%` : 'auto',
    bottom: !isTop ? `${Math.random() * 20 + 5}%` : 'auto',
    left: isLeft ? `${Math.random() * 20 + 5}%` : 'auto',
    right: !isLeft ? `${Math.random() * 20 + 5}%` : 'auto',
    // Z-index ajusté
    zIndex: 95
  };
};

// Fonction pour les icônes basées sur le texte de la pub
const getAdIcon = (adText) => {
  if (adText.includes('PC NEUF')) return '💻';
  if (adText.includes('BIOS')) return '⚙️';
  if (adText.includes('VPN')) return '🛡️';
  if (adText.includes('PRO')) return '🔑';
  return '📢';
};
</script>

<style scoped>
/* --- ADS (ADWARE - Pop-ups dispersés) --- */
.adware-layer-scattered {
  position: fixed;
  inset: 0;
  z-index: 90; /* Abaissé pour être sous la NavBar (100) */
  pointer-events: none;
}
.ad-banner-scattered {
  /* Styles retirés - utilisant maintenant .windows-window */
}

/* Styles pour les pop-ups basés sur .windows-window */
.ad-popup-styled {
  position: fixed;
  width: 300px;
  max-width: 90%;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  pointer-events: auto;
  z-index: 95; /* Abaissé pour être sous la NavBar (100) */
  background: white;
  border-radius: 8px;
  overflow: hidden;
  color: black;
}
.ad-header-styled {
  background: #0078D7;
  color: white;
  font-weight: bold;
  padding: 8px 12px;
  display: flex;
  justify-content: space-between;
  border-bottom: none;
}
.ad-close-btn {
  background: transparent;
  border: none;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  line-height: 1;
}
.ad-content-styled {
  padding: 15px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}
.ad-icon {
  font-size: 3rem;
  margin-bottom: 10px;
}
.ad-content-styled h3 {
  margin: 0 0 10px 0;
  font-weight: 600;
  font-size: 1.1rem;
}
.ad-info {
  font-size: 0.8rem;
  color: #666;
  margin-bottom: 15px;
}
.ad-action-btn {
  width: 80%;
  margin-top: 0;
  padding: 6px;
  background: #0078D7;
  color: white;
  border: none;
}

/* Style de barre de progression Linux/Update */
.linux-bar {
  background: #00ff00 !important;
}

.update-content h1 {
  font-size: 2.5rem;
  margin: 10px 0;
}
</style>
