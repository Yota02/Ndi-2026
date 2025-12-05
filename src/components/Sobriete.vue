<script setup lang="ts">
import { ref, computed } from 'vue'

import Tuxy from '@/assets/img/tux-detective.png'
import TuxAnimation from './TuxAnimation.vue'

const scrollToStory = () => {
  const story = document.getElementById('story')
  if (story !== null) {
    story.scrollIntoView({ behavior: 'smooth' })
  }
}

// Logique du Quiz
const questions = [
  {
    text: "La 4G consomme moins d'énergie que le Wifi.",
    answer: false,
    feedback:
      "Faux ! Le Wifi consomme beaucoup moins d'énergie pour transporter les données que le réseau mobile 4G/5G.",
  },
  {
    text: "Un PC sous Linux peut durer 5 ans de plus qu'un PC sous Windows.",
    answer: true,
    feedback:
      "Vrai ! Linux est beaucoup plus léger et continue d'être mis à jour sur du vieux matériel.",
  },
  {
    text: "Le mode 'sombre' économise de la batterie sur tous les écrans.",
    answer: false,
    feedback: "C'est un piège ! Ça ne marche vraiment que sur les écrans OLED.",
  },
]

const qIndex = ref(0)
const showResult = ref(false)
const tuxEmotion = ref('normal')

const currentQuestion = computed(() => questions[qIndex.value])

const answer = (userChoice: boolean) => {
  showResult.value = true
  if (userChoice === currentQuestion.value?.answer) {
    tuxEmotion.value = 'leveMain' // Utiliser 'leveMain' pour une bonne réponse
  } else {
    tuxEmotion.value = 'sad' // Utiliser 'sad' pour une mauvaise réponse
  }
}

const nextQuestion = () => {
  if (qIndex.value < questions.length - 1) {
    qIndex.value++
    showResult.value = false
    tuxEmotion.value = 'normal' // Remettre à 'normal' entre les questions
  } else {
    alert('Mission accomplie ! Tu es prêt.')

    qIndex.value = 0
    showResult.value = false
    tuxEmotion.value = 'normal' // Remettre à 'normal' à la fin du quiz
  }
}
</script>

<template>
  <div class="page-container">
    <header class="hero-section glass-panel">
      <div class="ambient-glow"></div>

      <div class="hero-content">
        <span class="badge-nird">Mission : Sauver les PC</span>
        <h1 class="main-title">
          Rejoins la <span class="text-gradient">Résistance Numérique</span>
        </h1>
        <p class="subtitle">
          L'Empire Big Tech nous force à jeter. Nous disons <strong>NON</strong>. <br />Incarne le
          changement avec la démarche NIRD.
        </p>
        <button class="btn-glow" @click="scrollToStory">Lancer l'enquête 🕵️‍♂️</button>
      </div>

      <div class="hero-visual">
        <div class="glow-circle"></div>
        <img src="@/assets/img/tux-detective.png" alt="Tux Détective" class="tux-hero floating" />
      </div>
    </header>

    <section id="story" class="threats-section">
      <div class="story-header">
        <div class="tux-container">
          <!-- Remplacer l'img statique par TuxAnimation avec emotion="leveMain" et props ajustées -->
          <TuxAnimation
            emotion="leveMain"
            :width="150"
            :height="150"
            :x="0"
            :y="0"
            :frameWidth="500"
            :frameHeight="500"
            :speed="200"
            style="position: relative"
            class="tux-avatar"
          />
        </div>
        <div class="speech-bubble">
          <h3>🕵️‍♂️ Rapport d'enquête #2025</h3>
          <p>
            "Salut cadet ! J'ai inspecté le réseau du lycée et c'est pire que ce que je pensais.
            J'ai identifié <strong>3 coupables</strong> qui nous forcent à jeter du matériel
            fonctionnel. <br /><br />
            <span class="highlight">Passe ta souris sur les fiches des suspects</span> pour voir
            leur vrai visage !"
          </p>
        </div>
      </div>

      <div class="threats-grid">
        <div class="flip-card">
          <div class="flip-card-inner">
            <div class="flip-card-front">
              <div class="icon-circle red-bg">🤖</div>
              <h3>Le Général Obsolescence</h3>
              <p class="threat-desc">
                <strong>Tuxy :</strong> "Ce robot cruel déclare que ton PC est 'trop vieux' juste
                parce qu'il a 4 ans !"
              </p>
              <div class="status-badge red-badge">🔴 Ennemi Public N°1</div>
            </div>
            <div class="flip-card-back">
              <h3>La Preuve du Crime</h3>
              <p class="impact-text">
                La fabrication représente <strong>80% de l'impact écologique</strong>. <br />Le
                jeter, c'est gâcher toute cette énergie.
              </p>
              <div class="solution-box">
                <span>✅ La riposte NIRD :</span>
                <strong>Le Réemploi & La Réparation</strong>
              </div>
            </div>
          </div>
        </div>

        <div class="flip-card">
          <div class="flip-card-inner">
            <div class="flip-card-front">
              <div class="icon-circle orange-bg">🐌</div>
              <h3>Baron Bloatware</h3>
              <p class="threat-desc">
                <strong>Tuxy :</strong> "Il gave nos ordis de mises à jour inutiles jusqu'à ce
                qu'ils n'avancent plus."
              </p>
              <div class="status-badge orange-badge">🟠 Saboteur de Vitesse</div>
            </div>
            <div class="flip-card-back">
              <h3>La Preuve du Crime</h3>
              <p class="impact-text">
                L'obésité logicielle (OS trop lourds) est la première cause de renouvellement
                prématuré du matériel.
              </p>
              <div class="solution-box">
                <span>✅ La riposte NIRD :</span>
                <strong>Linux (Système léger)</strong>
              </div>
            </div>
          </div>
        </div>

        <div class="flip-card">
          <div class="flip-card-inner">
            <div class="flip-card-front">
              <div class="icon-circle grey-bg">☁️</div>
              <h3>Le Faux Nuage</h3>
              <p class="threat-desc">
                <strong>Tuxy :</strong> "Il se fait passer pour un nuage léger... mais regardez
                derrière la fumée !"
              </p>
              <div class="status-badge red-badge">🔴 Pollueur Masqué</div>
            </div>
            <div class="flip-card-back">
              <h3>La Preuve du Crime</h3>
              <p class="impact-text">
                Ce n'est pas magique, c'est physique ! Les Data Centers consomment énormément d'eau
                et d'électricité H24.
              </p>
              <div class="solution-box">
                <span>✅ La riposte NIRD :</span>
                <strong>Sobriété des données</strong>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="lifecycle-section">
      <div class="lifecycle-header">
        <h2>L'Odyssée d'un Ordi Portable</h2>
        <p class="subtitle-lifecycle">
          De la mine à la déchèterie : pourquoi le jeter est un crime contre la planète.
        </p>
      </div>

      <div class="timeline">
        <div class="step">
          <div class="step-icon">⛏️</div>
          <h4>1. Extraction</h4>
          <p>
            Pour fabriquer un PC de <strong>2 kg</strong>, il faut excaver
            <strong>800 kg</strong> de matières premières.
          </p>
        </div>
        <div class="arrow">➡️</div>
        <div class="step">
          <div class="step-icon">🏭</div>
          <h4>2. Fabrication</h4>
          <p>
            Les composants font <strong>3 fois le tour du monde</strong> avant d'être assemblés.
          </p>
        </div>
        <div class="arrow">➡️</div>
        <div class="step warning-step">
          <div class="step-icon">🛑</div>
          <h4>3. Le Piège Logiciel</h4>
          <p>
            Au bout de 5 ans, <strong>Le Géant</strong> dit :
            <em>"Ton Windows n'est plus supporté !"</em>
          </p>
        </div>
        <div class="arrow">➡️</div>
        <div class="step bad-end">
          <div class="step-icon">🗑️</div>
          <h4>4. La Fin (Évitable)</h4>
          <p>Le PC finit à la poubelle. Un gâchis immense.</p>
        </div>
      </div>

      <div class="tux-intervention">
        <div class="tux-avatar">
          <!-- Remplacer l'img statique par TuxAnimation avec emotion="sad" et props ajustées -->
          <TuxAnimation
            emotion="sad"
            :width="150"
            :height="150"
            :x="0"
            :y="0"
            :frameWidth="500"
            :frameHeight="500"
            :speed="200"
            style="position: relative"
            class="tux-triste"
          />
        </div>
        <div class="speech-bubble">
          <h3>✋ Stop ! On peut changer la fin de l'histoire !</h3>
          <p>
            Si on remplace le système "périmé" par <strong>Linux</strong>, l'ordinateur repart pour
            5 ou 10 ans ! C'est ça, être <strong>NIRD</strong>.
          </p>
        </div>
      </div>
    </section>

    <section class="resistance-section">
      <h2>L'Arsenal de la Résistance NIRD</h2>
      <p>Heureusement, le village résiste ! Voici nos armes pour vaincre les monstres.</p>

      <div class="solutions-deck">
        <div class="solution-card green-theme">
          <div class="card-header">
            <h3>🛡️ L'Arme Absolue : LINUX</h3>
          </div>
          <div class="card-body">
            <p>Contre l'obsolescence, on installe un système léger et libre.</p>
            <ul>
              <li>Redonne vie aux vieux PC</li>
              <li>Pas de licence à payer</li>
              <li>Respecte la vie privée</li>
            </ul>
          </div>
        </div>

        <div class="solution-card orange-theme">
          <div class="card-header">
            <h3>🧹 La Technique : LE NETTOYAGE</h3>
          </div>
          <div class="card-body">
            <p>On allège le cartable numérique.</p>
            <ul>
              <li>On vide ses emails</li>
              <li>On compresse ses images</li>
              <li>On éteint le Wifi la nuit</li>
            </ul>
          </div>
        </div>

        <div class="solution-card blue-theme">
          <div class="card-header">
            <h3>🤝 La Force : LE PARTAGE</h3>
          </div>
          <div class="card-body">
            <p>La démarche NIRD, c'est faire ensemble.</p>
            <ul>
              <li>Ateliers de réparation (Repair Café)</li>
              <li>Partage de ressources libres</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <section class="interactive-check">
      <h2>Test d'aptitude "Résistant Numérique"</h2>
      <div class="quiz-container">
        <div class="question-box" v-if="currentQuestion">
          <p>{{ currentQuestion.text }}</p>

          <div class="buttons">
            <button
              @click="answer(true)"
              :class="{ success: showResult && currentQuestion.answer }"
            >
              VRAI
            </button>
            <button
              @click="answer(false)"
              :class="{ success: showResult && !currentQuestion.answer }"
            >
              FAUX
            </button>
          </div>

          <p v-if="showResult" class="feedback">{{ currentQuestion.feedback }}</p>
          <button v-if="showResult" @click="nextQuestion" class="btn-next">Suivant ➡️</button>
        </div>

        <div v-else class="end-screen">
          <p>Quiz terminé ! 🎉</p>
        </div>

        <div class="tux-judge">
          <!-- Remplacer l'img par TuxAnimation, avec émotion dynamique et props ajustées pour s'adapter au conteneur -->
          <TuxAnimation
            :emotion="tuxEmotion"
            :width="80"
            :height="80"
            :x="0"
            :y="0"
            :frameWidth="500"
            :frameHeight="500"
            :speed="200"
            style="position: relative"
          />
        </div>
      </div>
    </section>

    <footer class="nird-footer">
      <h3>Rejoins le mouvement !</h3>
      <p>Ton établissement peut devenir un Village Numérique Résistant.</p>
      <a href="https://nird.forge.apps.education.fr/" target="_blank" class="btn-final"
        >Accéder au QG NIRD</a
      >
    </footer>
  </div>
</template>

<style scoped>
/* =========================================
   1. CONFIGURATION GLOBALE DARK
   ========================================= */
.page-container {
  font-family:
    'Inter',
    system-ui,
    -apple-system,
    sans-serif;
  color: #e5e7eb; /* Gris clair */
  background-color: #111827; /* Fond bleu nuit */
  overflow-x: hidden;
  line-height: 1.6;
  padding-top: 5%;
}

h1,
h2,
h3,
h4 {
  font-weight: 800;
  margin: 0;
  color: #f3f4f6;
}
button {
  cursor: pointer;
  font-family: inherit;
  border: none;
  outline: none;
}

/* Variables pour le Hero */
:root {
  --primary: #10b981;
  --glass-border: rgba(255, 255, 255, 0.1);
}

/* =========================================
   2. HERO SECTION (STYLE PREMIUM)
   ========================================= */
.hero-section {
  position: relative;
  /* Fond dégradé subtil pour le Hero seulement */
  background:
    radial-gradient(at 0% 0%, rgba(16, 185, 129, 0.1) 0px, transparent 50%),
    radial-gradient(at 100% 100%, rgba(245, 158, 11, 0.05) 0px, transparent 50%);
  margin: 1rem;
  border-radius: 2rem;
  padding: 5rem 3rem;
  display: flex;
  flex-direction: column-reverse;
  align-items: center;
  justify-content: space-between;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Glassmorphism Panel */
.glass-panel {
  backdrop-filter: blur(10px);
  background: rgba(30, 41, 59, 0.4);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.hero-content {
  max-width: 600px;
  text-align: center;
  z-index: 2;
  margin-top: 2rem;
}

.badge-nird {
  background: rgba(16, 185, 129, 0.2);
  color: #6ee7b7;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-weight: bold;
  text-transform: uppercase;
  font-size: 0.8rem;
  letter-spacing: 1px;
  display: inline-block;
  margin-bottom: 1rem;
}

.main-title {
  font-size: 3rem;
  line-height: 1.1;
  margin-bottom: 1rem;
  color: white;
}

.text-gradient {
  background: linear-gradient(to right, #34d399, #60a5fa);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.subtitle {
  font-size: 1.2rem;
  color: #94a3b8;
  margin-bottom: 2rem;
}

/* Bouton Néon */
.btn-glow {
  background: #10b981;
  color: #022c22;
  font-weight: 800;
  padding: 1rem 2.5rem;
  border-radius: 50px;
  font-size: 1.1rem;
  animation: pulse-glow 2s infinite;
  transition: transform 0.2s;
}
.btn-glow:hover {
  transform: scale(1.05);
}

/* Visuel Hero */
.hero-visual {
  position: relative;
  width: 300px;
  display: flex;
  justify-content: center;
}
.tux-hero {
  width: 100%;
  max-width: 250px;
  z-index: 2;
  position: relative;
}
.floating {
  animation: float 6s ease-in-out infinite;
}

.glow-circle {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 250px;
  height: 250px;
  background: radial-gradient(circle, rgba(16, 185, 129, 0.4) 0%, transparent 70%);
  z-index: 1;
}

/* =========================================
   3. REST OF PAGE (CLEAN DARK STYLE)
   ========================================= */

/* --- THREATS SECTION --- */
.threats-section {
  padding: 5rem 2rem;
  background-color: #111827;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.story-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2rem;
  margin-bottom: 4rem;
  max-width: 900px;
  flex-wrap: wrap;
}

.tux-avatar {
  width: 150px;
  animation: float 3s ease-in-out infinite;
  filter: drop-shadow(0, 10px, 20px, rgba(0, 0, 0, 0.5));
}

.speech-bubble {
  background: #1f2937;
  padding: 2rem;
  border-radius: 2rem;
  border-top-left-radius: 0;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  max-width: 500px;
  position: relative;
  border: 1px solid #374151;
}
.speech-bubble::before {
  content: '';
  position: absolute;
  top: 0;
  left: -20px;
  width: 20px;
  height: 20px;
  background: #1f2937;
  clip-path: polygon(100% 0, 0 0, 100% 100%);
}
.speech-bubble h3 {
  color: #10b981;
  margin-bottom: 0.5rem;
  font-size: 1.4rem;
}
.highlight {
  color: #f59e0b;
  font-weight: bold;
}

/* GRILLE */
.threats-grid {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 2rem;
}

/* FLIP CARDS */
.flip-card {
  width: 300px;
  height: 400px;
  perspective: 1000px;
  cursor: pointer;
}
.flip-card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  text-align: center;
  transition: transform 0.6s cubic-bezier(0.4, 0.2, 0.2, 1);
  transform-style: preserve-3d;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  border-radius: 1.5rem;
}
.flip-card:hover .flip-card-inner {
  transform: rotateY(180deg);
}

.flip-card-front,
.flip-card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  border-radius: 1.5rem;
  padding: 2rem;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* RECTO DARK */
.flip-card-front {
  background-color: #1f2937;
  border: 1px solid #374151;
}
.icon-circle {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  margin-bottom: 1.5rem;
}
.red-bg {
  background: rgba(239, 68, 68, 0.2);
}
.orange-bg {
  background: rgba(245, 158, 11, 0.2);
}
.grey-bg {
  background: rgba(107, 114, 128, 0.2);
}
.threat-desc {
  color: #9ca3af;
  font-style: italic;
  margin-bottom: 2rem;
  line-height: 1.4;
}
.status-badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: bold;
  font-size: 0.8rem;
  text-transform: uppercase;
}
.red-badge {
  background: rgba(239, 68, 68, 0.1);
  color: #fca5a5;
  border: 1px solid rgba(239, 68, 68, 0.3);
}
.orange-badge {
  background: rgba(245, 158, 11, 0.1);
  color: #fdba74;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

/* VERSO DARK */
.flip-card-back {
  background: linear-gradient(135deg, #064e3b 0%, #065f46 100%);
  transform: rotateY(180deg);
  border: 1px solid #047857;
}
.flip-card-back h3 {
  border-bottom: 2px solid rgba(255, 255, 255, 0.3);
  padding-bottom: 0.5rem;
  margin-bottom: 1.5rem;
}
.solution-box {
  background: #111827;
  color: #34d399;
  padding: 1rem;
  border-radius: 1rem;
  width: 100%;
  border: 1px solid #065f46;
}
.solution-box span {
  display: block;
  font-size: 0.8rem;
  text-transform: uppercase;
  color: #9ca3af;
}
.solution-box strong {
  font-size: 1.1rem;
}

/* --- TIMELINE --- */
.lifecycle-section {
  padding: 5rem 2rem;
  background: #1f2937;
  text-align: center;
}
.subtitle-lifecycle {
  color: #9ca3af;
  font-style: italic;
  margin-bottom: 3rem;
}
.timeline {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  gap: 1rem;
  flex-wrap: wrap;
}
.step {
  background: #1f2937;
  padding: 1.5rem;
  border-radius: 1rem;
  width: 220px;
  transition: transform 0.3s;
  border: 1px solid #374151;
}
.step:hover {
  transform: translateY(-5px);
  border-color: #4b5563;
}
.step-icon {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}
.step h4 {
  color: #f3f4f6;
  margin-bottom: 0.5rem;
}
.step p {
  font-size: 0.9rem;
  color: #d1d5db;
}
.warning-step {
  border: 2px solid #f59e0b;
  background: rgba(245, 158, 11, 0.05);
}
.bad-end {
  border: 2px solid #ef4444;
  background: rgba(239, 68, 68, 0.05);
  opacity: 0.9;
}
.arrow {
  font-size: 2rem;
  color: #4b5563;
  align-self: center;
  display: none;
}
.tux-intervention {
  margin-top: 4rem;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2rem;
  flex-direction: column;
}
.tux-triste {
  width: 150px;
  height: auto;
}

/* --- SOLUTIONS --- */
.resistance-section {
  padding: 5rem 2rem;
  background: #111827;
  text-align: center;
}
.solutions-deck {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2rem;
  margin-top: 3rem;
}
.solution-card {
  background: #1f2937;
  width: 300px;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
  text-align: left;
  transition: transform 0.3s;
  border: 1px solid #374151;
}
.solution-card:hover {
  transform: translateY(-5px);
  border-color: #6b7280;
}
.card-header {
  padding: 1.5rem;
  color: white;
  font-weight: bold;
}
.green-theme .card-header {
  background: #059669;
}
.orange-theme .card-header {
  background: #d97706;
}
.blue-theme .card-header {
  background: #2563eb;
}
.card-body {
  padding: 1.5rem;
}
.card-body ul {
  padding-left: 1.2rem;
  color: #d1d5db;
}

/* --- QUIZ --- */
.interactive-check {
  padding: 4rem 2rem;
  background: #1f2937;
  color: white;
  text-align: center;
}
.quiz-container {
  background: #1f2937;
  max-width: 700px;
  margin: 2rem auto;
  padding: 2rem;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 2rem;
  border: 1px solid #374151;
}
.question-box {
  flex: 1;
  text-align: left;
}
.buttons button {
  margin-right: 10px;
  padding: 10px 25px;
  border-radius: 8px;
  font-weight: bold;
}
.buttons button.success {
  background: #10b981;
  color: white;
}
.buttons button.error {
  background: #ef4444;
  color: white;
}
.feedback {
  color: #34d399;
  font-weight: bold;
  margin-top: 1rem;
}
.btn-next {
  background: #374151;
  color: white;
  margin-top: 1rem;
  border: 1px solid #4b5563;
  padding: 0.5rem 1rem;
  border-radius: 5px;
}
.tux-judge {
  background: rgba(255, 255, 255, 0.05);
  width: 100px;
  height: 100px;
  border-radius: 50%;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}
.emoji-judge {
  font-size: 3rem;
}

.tux-mood-img {
  width: 80%; /* Ajuste selon tes préférences */
  height: auto;
  object-fit: contain;
}

/* --- FOOTER --- */
.nird-footer {
  text-align: center;
  padding: 3rem 1rem;
  background: #064e3b;
  color: white;
  border-top: 1px solid #047857;
}
.btn-final {
  display: inline-block;
  background: white;
  color: #064e3b;
  padding: 12px 30px;
  text-decoration: none;
  border-radius: 50px;
  font-weight: bold;
  margin-top: 1.5rem;
}
.btn-final:hover {
  background: #d1fae5;
}

/* --- ANIMATIONS GLOBALES --- */
@keyframes float {
  0% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-15px);
  }
  100% {
    transform: translateY(0px);
  }
}
@keyframes pulse-glow {
  0% {
    box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4);
  }
  70% {
    box-shadow: 0 0 0 15px rgba(16, 185, 129, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
  }
}

@media (min-width: 768px) {
  .hero-section {
    flex-direction: row;
    text-align: left;
  }
  .hero-content {
    margin-top: 0;
    text-align: left;
  }
  .arrow {
    display: block;
  }
  .tux-intervention {
    flex-direction: row;
  }
}

@media (max-width: 767px) {
  .story-header {
    flex-direction: column;
    text-align: center;
  }
  .speech-bubble::before {
    top: -10px;
    left: 50%;
    transform: translateX(-50%) rotate(90deg);
  }
  .quiz-container {
    flex-direction: column-reverse;
  }
}
</style>
