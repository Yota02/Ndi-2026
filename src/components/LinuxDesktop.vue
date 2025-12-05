<template>
  <div class="linux-desktop gnome-desktop-bg">

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

        <button @click="$emit('start-session')" class="btn-primary linux-start-btn">
          Démarrer la session
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

defineProps({
  currentTime: String,
});

defineEmits(['start-session']);
</script>

<style scoped>
/* --- INTERFACE LINUX --- */
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
.icon-volume::before { content: 'V'; }
.icon-user::before { content: 'U'; }

/* GNOME Card Styling */
.login-container { flex: 1; display: flex; justify-content: center; align-items: center; padding-bottom: 80px; }
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
.profile-pic { width: 120px; height: 120px; border-radius: 50%; margin-bottom: 20px; border: 4px solid rgba(255, 255, 255, 0.5); background-color: #0078D7; }
.success-text { font-size: 1.1rem; font-weight: 600; margin-bottom: 30px; color: #58a6ff; }

/* Placeholders (Doivent correspondre à WindowsLogin) */
.icon-wifi::before { content: 'W'; font-size: 0.7em; }
.icon-battery::before { content: 'B'; font-size: 0.7em; }
.icon-accessibility::before { content: 'A'; font-size: 0.7em; }
</style>
