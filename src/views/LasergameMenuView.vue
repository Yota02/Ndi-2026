<script setup lang="ts">
import { useRouter } from 'vue-router'
import NavBar from '../components/NavBar.vue'

// Plus besoin d'importer les composants de jeu ici !
const router = useRouter()

// Navigation vers le Quiz
const goToQuiz = () => {
  router.push('/laser-game/quiz')
}

// Navigation vers la Survie
const goToSurvival = () => {
  router.push('/laser-game/survival')
}

const goToPuzzle = () => {
  router.push('/laser-game/puzzle')
}
</script>

<template>
  <NavBar/>

  <div class="hub-container">

    <div class="menu-screen">
      <h1 class="main-title">🐧 ARCADE TUXY 🐧</h1>
      <p class="subtitle">Choisissez votre mission pour sauver la planète</p>

      <div class="button-group">

        <button @click="goToQuiz" class="game-card quiz-card">
          <div class="card-icon">🧠</div>
          <h2>Quiz Laser</h2>
          <p>Répondez juste ou tirez sur les erreurs !</p>
        </button>

        <button @click="goToSurvival" class="game-card survival-card">
          <div class="card-icon">🔥</div>
          <h2>Tir de Survie</h2>
          <p>Détruisez la pollution, protégez la nature !</p>
        </button>

        <button @click="goToPuzzle" class="game-card puzzle-card">
          <div class="card-icon">💎</div>
          <h2>Fibre Optique</h2>
          <p>Aidez Tuxy à rediriger le signal vers la maison !</p>
        </button>


      </div>
    </div>

  </div>
</template>

<style scoped>
.hub-container {
  width: 100vw;
  height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  position: relative;
}

/* STYLES DU MENU */
.menu-screen { text-align: center; z-index: 1; }

.main-title {
  font-size: 3.5rem;
  margin-bottom: 0.5rem;
  background: -webkit-linear-gradient(#42b883, #35495e);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-transform: uppercase;
  letter-spacing: 4px;
}

.subtitle { color: #a0a0a0; margin-bottom: 3rem; font-size: 1.2rem; }

.button-group { display: flex; gap: 30px; justify-content: center; flex-wrap: wrap; }

.game-card {
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 30px;
  width: 250px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
  text-align: center;
}
.game-card h2 { margin-top: 10px; font-size: 1.5rem; }
.game-card p { margin-top: 10px; font-size: 0.9rem; color: #ccc; }

.game-card:hover { transform: translateY(-5px); background: rgba(255, 255, 255, 0.1); }
.quiz-card:hover { border-color: #42b883; box-shadow: 0 0 15px rgba(66, 184, 131, 0.4); }
.survival-card:hover { border-color: #ff4444; box-shadow: 0 0 15px rgba(255, 68, 68, 0.4); }
.card-icon { font-size: 4rem; margin-bottom: 15px; }

.puzzle-card:hover { border-color: #00bcd4; box-shadow: 0 0 15px rgba(0, 188, 212, 0.4); }
</style>
