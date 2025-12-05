<template>
  <div>
    <div v-if="adQueue.length > 0" class="adware-layer-scattered">
      <div
        v-for="(adText, index) in adQueue"
        :key="index"
        v-show="index === 0"
        class="ad-banner-scattered widget-style"
        :style="getRandomAdStyle(index)"
      >
        <div class="ad-header widget-header">NOTIFICATION SPONSORISÉE <span @click="$emit('close-ad')" class="ad-close">×</span></div>
        <div class="ad-content">{{ adText }}</div>
      </div>
    </div>

    <template v-if="!overlayState.isLinux">

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
              <button @click="$emit('close-bing')">×</button>
            </div>
            <div class="clippy-body">
              <p>Je remarque que vous écrivez un mot de passe !</p>
              <p>L'édition Entreprise inclut l'optimisation neurale de vos pensées.</p>
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
            <p>Votre licence Windows n'est pas à jour. Vous ne pouvez pas vous connecter tant que vous n'avez pas procédé à la mise à niveau suivante :</p>
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
  // Si index > 0, l'ad n'est pas visible (v-show), mais nous devons maintenir la position dans la liste
  if (index > 0) return {};

  // Logique de positionnement aléatoire (utilisée uniquement pour le premier élément affiché)
  const isTop = Math.random() > 0.5;
  const isLeft = Math.random() > 0.5;

  return {
    top: isTop ? `${Math.random() * 20 + 5}%` : 'auto',
    bottom: !isTop ? `${Math.random() * 20 + 5}%` : 'auto',
    left: isLeft ? `${Math.random() * 20 + 5}%` : 'auto',
    right: !isLeft ? `${Math.random() * 20 + 5}%` : 'auto'
  };
};
</script>

<style scoped>
/* --- ADS (ADWARE - Pop-ups dispersés) --- */
.adware-layer-scattered {
  position: fixed;
  inset: 0;
  z-index: 9050;
  pointer-events: none;
}
.ad-banner-scattered {
  position: fixed;
  width: 280px;
  background: rgba(43, 43, 43, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
  font-family: 'Segoe UI', sans-serif;
  animation: bounce-in 0.5s;
  pointer-events: auto;
  border-radius: 8px;
  overflow: hidden;
  z-index: 9060;
}
.widget-header { background: rgba(31, 31, 31, 0.8); color: #ccc; font-weight: 600; padding: 5px 10px; display: flex; justify-content: space-between; font-size: 0.8rem; cursor: default; }
.ad-close { cursor: pointer; }
.ad-content { padding: 15px; text-align: left; font-weight: 400; font-size: 1rem; color: #ffcc00; cursor: pointer; }
</style>
