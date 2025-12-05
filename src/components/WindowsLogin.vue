<template>
  <div class="login-container">
    <div class="system-bar-windows">
      <div class="debug-area">
                <span style="color: #ccc; opacity: 0.5; font-family: 'Fira Code', monospace;">
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

    <div class="login-card">
      <img src="https://via.placeholder.com/120/0078D7/FFFFFF?text=USER" alt="Profile Picture" class="profile-pic">

      <h1>Mot de passe</h1>

      <p class="warning-text">
        Windows {{ windowsVersion }} {{ currentEdition.name }}
        <br>
        {{ currentEdition.feature }}
      </p>

      <form @submit.prevent class="input-group">
        <div class="password-wrapper">
          <input
            ref="inputRef"
            id="password-field"
            type="password"
            :value="inputValue"
            @input="$emit('update:inputValue', $event.target.value); $emit('input-change')"
            @keydown.enter="$emit('action-trigger', 'ENTER')"
            :disabled="isSystemBusy"
            placeholder="Mot de passe"
            autocomplete="off"
          />

          <button
            type="button"
            class="unlock-btn"
            @mousedown="$emit('action-trigger', 'CLICK')"
            :disabled="isSystemBusy"
          >
            <i class="icon-arrow-right"></i>
          </button>
        </div>
      </form>

      <p class="status-log" v-if="lastLog">{{ lastLog }}</p>

    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, ref } from 'vue';

// Définition des props reçues du composant App.vue
defineProps({
  windowsVersion: Number,
  currentEdition: Object,
  brokenMethod: String,
  inputValue: String,
  lastLog: String,
  isSystemBusy: Boolean,
  currentTime: String,
});

// Définition des événements émis au composant parent (App.vue)
defineEmits(['update:inputValue', 'input-change', 'action-trigger']);

// Exposer une référence pour le focus (si nécessaire, mais géré par App.vue)
const inputRef = ref(null);
</script>

<style scoped>
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

/* --- BARRE D'ÉTAT WINDOWS (Adaptation locale) --- */
.system-bar-windows {
  position: absolute; bottom: 0; left: 0; right: 0; padding: 10px 40px; display: flex; justify-content: space-between; align-items: center; font-size: 0.9rem; background: rgba(0, 0, 0, 0.1); z-index: 100;
}
.debug-area { font-family: 'Fira Code', monospace; }
.status-icons i { font-size: 1.1rem; margin-left: 15px; display: inline-block; width: 1em; height: 1em; border: 1px solid white; border-radius: 2px; line-height: 1; text-align: center; }
.icon-wifi::before { content: 'W'; font-size: 0.7em; }
.icon-battery::before { content: 'B'; font-size: 0.7em; }
.icon-accessibility::before { content: 'A'; font-size: 0.7em; }
.icon-arrow-right::before { content: '>'; font-weight: bold; }
</style>
