<template>
  <div class="login-container">
    <div class="contact-card" :class="{ 'windows-mode': !isLinuxInstalled, 'linux-mode': isLinuxInstalled }">

      <img
        :src="isLinuxInstalled ? 'https://via.placeholder.com/120/58a6ff/0d1117?text=TUX' : 'https://via.placeholder.com/120/0078D7/FFFFFF?text=SUPPORT'"
        alt="Profile Picture"
        class="profile-pic"
        :class="{ 'linux-pic': isLinuxInstalled }"
      >

      <h1 v-if="!isLinuxInstalled">Nous contacter.</h1>
      <h1 v-else>Nous contacter !</h1>

      <p :class="{ 'warning-text': !isLinuxInstalled, 'success-text': isLinuxInstalled }">
                <span v-if="!isLinuxInstalled">
                    Windows {{ windowsVersion }} {{ currentEdition.name }}
                </span>

        <span v-else>
            L'équipe de support est joignable via les canaux suivants. Remplissez le formulaire ci-dessous pour nous contacter sans aucune interruption.
        </span>
      </p>

      <form @submit.prevent class="input-group" v-if="!isLinuxInstalled">

        <div class="input-wrapper-extended">
          <input
            type="email"
            :value="emailValue"
            @input="$emit('update:emailValue', $event.target.value); $emit('trigger-frustration')"
            :disabled="isSystemBusy"
            placeholder="Votre adresse email"
            required
            class="form-input"
          />
        </div>

        <div class="input-wrapper-extended">
          <input
            ref="inputRef"
            id="contact-field"
            type="text"
            :value="inputValue"
            @input="$emit('update:inputValue', $event.target.value); $emit('trigger-frustration')"
            @keydown.enter="$emit('action-trigger', 'ENTER')"
            :disabled="isSystemBusy"
            placeholder="Décrivez votre problème ici..."
            autocomplete="off"
            class="form-input"
          />

          <button
            type="button"
            class="submit-btn"
            @mousedown="$emit('action-trigger', 'CLICK')"
            :disabled="isSystemBusy"
          >
            <i class="icon-send"></i>
          </button>
        </div>
      </form>

      <form v-else @submit.prevent="submitLinuxQuery" class="input-group linux-form-style">
        <div class="input-wrapper-extended">
          <input
            type="email"
            placeholder="Votre email (pour la réponse)"
            class="form-input linux-input-field"
            :value="emailValue"
            @input="$emit('update:emailValue', $event.target.value)"
            required
          />
        </div>
        <div class="input-wrapper-extended">
                    <textarea
                      placeholder="Décrivez votre requête stable..."
                      class="form-input linux-textarea"
                      :value="inputValue"
                      @input="$emit('update:inputValue', $event.target.value)"
                      rows="4"
                      required
                    ></textarea>
        </div>
        <button type="submit" class="btn-primary linux-submit-btn">Soumettre la requête</button>
      </form>

      <p class="status-log" v-if="lastLog && !isLinuxInstalled">{{ lastLog }}</p>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, ref } from 'vue';

const props = defineProps({
  isLinuxInstalled: Boolean,
  windowsVersion: Number,
  currentEdition: Object,
  brokenMethod: String,
  inputValue: String,
  emailValue: String,
  lastLog: String,
  isSystemBusy: Boolean,
  currentTime: String,
});

// Événements mis à jour
defineEmits(['update:inputValue', 'update:emailValue', 'trigger-frustration', 'action-trigger', 'start-session']);

const inputRef = ref(null);

const submitLinuxQuery = () => {
  // Dans le vrai monde, on enverrait les données ici.
  alert(`Requête soumise par ${props.emailValue}. Merci pour votre patience stable !`);
  // Réinitialiser les champs après soumission réussie
  props.emailValue = '';
  props.inputValue = '';
};
</script>

<style scoped>
/* --- STYLES CARD COMMUNS --- */
.login-container { flex: 1; display: flex; justify-content: center; align-items: center; padding-bottom: 80px; }
.contact-card { display: flex; flex-direction: column; align-items: center; padding: 40px; border-radius: 4px; backdrop-filter: blur(10px); width: 500px; max-width: 90%; }
.profile-pic { width: 120px; height: 120px; border-radius: 50%; margin-bottom: 20px; border: 4px solid rgba(255, 255, 255, 0.5); background-color: #0078D7; }
.contact-card h1 { font-weight: 300; margin-bottom: 5px; }
.input-group { width: 100%; display: flex; flex-direction: column; align-items: center; gap: 15px; }

/* Wrappers pour les inputs */
.input-wrapper-extended {
  width: 380px;
  max-width: 100%;
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  border-bottom: 2px solid transparent;
  transition: border-bottom-color 0.3s;
}
.input-wrapper-extended:focus-within { border-bottom-color: white; }

.form-input {
  background: transparent;
  border: none;
  color: white;
  font-size: 1.2rem;
  padding: 10px 15px;
  flex-grow: 1;
  outline: none;
  width: 100%;
  box-sizing: border-box; /* S'assure que padding n'augmente pas la largeur */
  resize: vertical; /* Permet de redimensionner le textarea verticalement */
  min-height: 40px;
}

/* --- MODE WINDOWS (Frustration) --- */
.windows-mode {
  background: rgba(0, 0, 0, 0.15);
}
.warning-text {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 30px;
  color: #ffcc00;
  text-align: center;
}

.submit-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  padding: 10px 15px;
  font-size: 1.2rem;
  cursor: pointer;
  transition: background 0.2s;
  height: 100%;
}
.submit-btn:hover { background: rgba(255, 255, 255, 0.4); }
.submit-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.status-log { margin-top: 20px; font-style: italic; font-size: 0.9rem; opacity: 0.7; max-width: 300px; }
.windows-reset-btn { background: rgba(255, 255, 255, 0.15); border: 1px solid rgba(255, 255, 255, 0.3); }
.icon-send::before { content: '>'; font-weight: bold; }


/* --- MODE LINUX (Libération / Contact Simple) --- */
.linux-mode {
  background: rgba(43, 43, 43, 0.8);
  border: 1px solid #58a6ff;
  color: #fff;
}
.linux-pic {
  border-color: #58a6ff !important;
}
.success-text {
  color: #58a6ff;
  font-weight: 400;
  font-size: 1.1rem;
  margin-bottom: 25px;
  text-align: center;
}

.linux-start-btn {
  background: #58a6ff;
  color: #1e1e1e;
  font-weight: bold;
  margin-top: 30px;
  padding: 10px 20px;
  border-radius: 5px;
}

/* Styles spécifiques au Formulaire Linux */
.linux-form-style .input-wrapper-extended {
  /* Style pour le fond foncé Linux */
  background: rgba(255, 255, 255, 0.1);
  border-bottom: 2px solid #58a6ff;
}
.linux-form-style .input-wrapper-extended:focus-within {
  border-bottom-color: #58a6ff;
}
.linux-input-field {
  color: #58a6ff;
}
.linux-textarea {
  min-height: 100px; /* Plus grand pour le texte de requête */
}
.linux-submit-btn {
  width: 380px;
  max-width: 100%;
  margin-top: 10px;
  background: #238636;
  color: white;
}
</style>
