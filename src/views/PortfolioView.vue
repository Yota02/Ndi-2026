<script setup lang="ts">
import { useRouter } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import coverImage from '@/assets/portfolio/cover.jpg'
import cvFile from '@/assets/portfolio/CV.pdf'

const router = useRouter()

function startChapter() {
  router.push('/chapter/1')
}
</script>

<template>
  <NavBar />
  <main class="landing-page">

    <div class="bg-glow glow-1"></div>
    <div class="bg-glow glow-2"></div>

    <div class="content-wrapper">

      <section class="info-section">
        <div class="text-content">
          <span class="subtitle">Portfolio Créatif</span>
          <h1 class="main-title">
            Ma BD <br />
            <span class="highlight">Portfolio</span>
          </h1>
          <p class="description">
            Découvrez mon parcours et mes compétences à travers une expérience narrative unique.
          </p>
        </div>

        <div class="actions-group">
          <button @click="startChapter" class="btn btn-primary">
            <span class="btn-content">
              <span>Lire la BD</span>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </span>
          </button>

          <a :href="cvFile" target="_blank" class="btn btn-secondary">
            <span class="btn-content">
              <span>CV PDF</span>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            </span>
          </a>
        </div>
      </section>

      <section class="visual-section">
        <div class="book-container">
          <div class="book">
            <div class="book-cover">
              <img :src="coverImage" alt="Couverture BD" />
            </div>
            <div class="book-pages"></div>
            <div class="book-back"></div>
          </div>
          <div class="book-shadow"></div>
        </div>
      </section>

    </div>
  </main>
</template>

<style scoped>
/* --- CONFIGURATION GLOBALE --- */
.landing-page {
  position: relative;
  min-height: 100vh;
  width: 100%;
  background-color: #0f172a; /* Bleu nuit profond */
  color: white;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* --- BACKGROUND ANIMÉ --- */
.bg-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  z-index: 0;
  opacity: 0.4;
  animation: float 10s infinite alternate ease-in-out;
}

.glow-1 {
  top: -10%;
  left: -10%;
  width: 50vw;
  height: 50vw;
  background: radial-gradient(circle, #7c3aed 0%, transparent 70%);
}

.glow-2 {
  bottom: -10%;
  right: -10%;
  width: 40vw;
  height: 40vw;
  background: radial-gradient(circle, #2563eb 0%, transparent 70%);
}

@keyframes float {
  0% { transform: translate(0, 0); }
  100% { transform: translate(30px, 50px); }
}

/* --- LAYOUT PRINCIPAL --- */
.content-wrapper {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 1200px;
  padding: 80px 24px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
}

/* --- SECTION GAUCHE (TEXTE) --- */
.info-section {
  display: flex;
  flex-direction: column;
  gap: 30px;
  animation: slideInLeft 0.8s ease-out;
}

.subtitle {
  text-transform: uppercase;
  letter-spacing: 3px;
  font-size: 14px;
  font-weight: 600;
  color: #a78bfa; /* Violet clair */
}

.main-title {
  font-size: 4rem;
  line-height: 1.1;
  font-weight: 800;
  margin: 0;
}

.highlight {
  background: linear-gradient(120deg, #c084fc 0%, #6366f1 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.description {
  font-size: 1.1rem;
  color: #94a3b8; /* Gris bleuté */
  line-height: 1.6;
  max-width: 450px;
  margin: 0;
}

/* --- BOUTONS --- */
.actions-group {
  display: flex;
  gap: 20px;
  margin-top: 10px;
}

.btn {
  padding: 14px 28px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.btn-content {
  display: flex;
  align-items: center;
  gap: 10px;
}

.btn-primary {
  background: white;
  color: #0f172a;
  box-shadow: 0 4px 15px rgba(255, 255, 255, 0.2);
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(255, 255, 255, 0.3);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.05);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: white;
  transform: translateY(-3px);
}

/* --- SECTION DROITE (LIVRE 3D) --- */
.visual-section {
  display: flex;
  justify-content: center;
  perspective: 1500px; /* Clé pour la 3D */
  animation: fadeIn 1s ease-out;
}

.book-container {
  position: relative;
  width: 320px;
  height: 460px; /* Ratio standard BD/Comics */
  z-index: 10;
}

.book {
  position: relative;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
  transform: rotateY(-25deg) rotateX(5deg);
  transition: transform 0.5s ease;
  box-shadow: 20px 20px 50px rgba(0,0,0,0.5);
}

.book-container:hover .book {
  transform: rotateY(-10deg) rotateX(0deg) scale(1.02);
}

.book-cover {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #1e293b;
  border-radius: 4px 8px 8px 4px;
  overflow: hidden;
  transform-origin: left;
  z-index: 2;
}

.book-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Effet des pages sur le côté (épaisseur) */
.book-pages {
  position: absolute;
  top: 4px;
  right: -15px; /* Épaisseur du livre */
  width: 15px;
  height: calc(100% - 8px);
  background: linear-gradient(to right, #ccc, #eee, #ccc);
  transform: rotateY(90deg);
  transform-origin: left;
  z-index: 1;
}

/* Ombre sous le livre */
.book-shadow {
  position: absolute;
  bottom: -30px;
  left: 20px;
  width: 90%;
  height: 20px;
  background: rgba(0,0,0,0.6);
  filter: blur(20px);
  transform: rotateY(-25deg);
  z-index: -1;
  transition: all 0.5s ease;
}

.book-container:hover .book-shadow {
  transform: rotateY(-10deg) scale(0.9);
  opacity: 0.8;
}

/* --- ANIMATIONS D'ENTRÉE --- */
@keyframes slideInLeft {
  from { opacity: 0; transform: translateX(-50px); }
  to { opacity: 1; transform: translateX(0); }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* --- RESPONSIVE --- */
@media (max-width: 968px) {
  .content-wrapper {
    grid-template-columns: 1fr;
    text-align: center;
    gap: 40px;
    padding-top: 100px;
  }

  .info-section {
    align-items: center;
  }

  .description {
    margin: 0 auto;
  }

  .visual-section {
    perspective: 1000px;
    margin-bottom: 40px;
  }

  .book-container {
    width: 260px;
    height: 380px;
  }
}

@media (max-width: 480px) {
  .main-title {
    font-size: 2.8rem;
  }

  .actions-group {
    flex-direction: column;
    width: 100%;
  }

  .btn {
    width: 100%;
  }
}
</style>
