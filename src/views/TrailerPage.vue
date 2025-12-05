<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import FadeText from '@/components/trailer/FadeText.vue';

const router = useRouter();

// ==========================================
// CONFIGURATION - Les images sont dans /public/trailer/
// ==========================================
const introText = "Bienvenue dans l'expérience.";

const cinematicSentences: { text: string; image: string | null }[] = [
  {
    text: "Aujourd'hui, le réchauffement climatique menace notre planète...",
    image: null
  },
  {
    text: "La banquise fond sous le poids de nos clics et du matériel jugé trop vite obsolète.",
    image: "/trailer/banquise.jpg"
  },
  {
    text: "Mais vous suivrez les aventures de Tuxy le pingouin dans ces péripéties.",
    image: null
  },
  {
    text: "Ensemble, nous reprendrons le contrôle pour offrir un avenir respirable à notre planète.",
    image: "/trailer/mondeMeilleur.jpg"
  },
  {
    text: "Vous découvrirez la voie du NIRD : un Numérique Inclusif, Responsable et Durable.",
    image: null
  },
  {
    text: "Vous y trouverez les clés pour comprendre, partager et reprendre le pouvoir.",
    image: "/trailer/clesDuMonde.jpg"
  },
  {
    text: "Votre résistance commencera ici : êtes-vous prêts ?",
    image: null
  },
];

const SENTENCE_DISPLAY_DURATION = 5000;
const FADE_DURATION = 1000;

// ==========================================
// ÉTATS
// ==========================================
const step = ref<'intro' | 'cinematic' | 'end'>('intro');
const introVisible = ref(false);
const introSlidingUp = ref(false);
const showScrollHint = ref(false);
const currentSentenceIndex = ref(0);
const showCinematicText = ref(false);
const showBackground = ref(false);
const showVignette = ref(false);
const currentImage = ref<string | null>(null);

const currentSentence = computed(() => cinematicSentences[currentSentenceIndex.value]);

// ==========================================
// LIFECYCLE
// ==========================================
onMounted(() => {
  // Précharger les images
  cinematicSentences.forEach(sentence => {
    if (sentence.image) {
      const img = new Image();
      img.src = sentence.image;
    }
  });

  setTimeout(() => {
    introVisible.value = true;
  }, 200);

  setTimeout(() => {
    showScrollHint.value = true;
    addScrollListeners();
  }, 1500);
});

onUnmounted(() => {
  removeScrollListeners();
});

// ==========================================
// GESTION DU SCROLL INITIAL
// ==========================================
const addScrollListeners = () => {
  window.addEventListener('wheel', handleInitialScroll);
  window.addEventListener('touchmove', handleInitialScroll);
  window.addEventListener('keydown', handleInitialKeydown);
};

const removeScrollListeners = () => {
  window.removeEventListener('wheel', handleInitialScroll);
  window.removeEventListener('touchmove', handleInitialScroll);
  window.removeEventListener('keydown', handleInitialKeydown);
};

const handleInitialScroll = () => {
  if (step.value === 'intro' && !introSlidingUp.value) {
    startCinematic();
  }
};

const handleInitialKeydown = (e: KeyboardEvent) => {
  if ((e.key === 'ArrowDown' || e.key === ' ' || e.key === 'Enter') && step.value === 'intro' && !introSlidingUp.value) {
    startCinematic();
  }
};

// ==========================================
// LANCEMENT DE LA CINÉMATIQUE
// ==========================================
const startCinematic = () => {
  introSlidingUp.value = true;
  showScrollHint.value = false;
  removeScrollListeners();

  setTimeout(() => {
    step.value = 'cinematic';
    playSentence();
  }, 800);
};

// ==========================================
// LECTURE AUTOMATIQUE DES PHRASES
// ==========================================
const playSentence = () => {
  if (currentSentenceIndex.value >= cinematicSentences.length) {
    showBackground.value = false;
    setTimeout(() => {
      step.value = 'end';
    }, FADE_DURATION);
    return;
  }

  const sentence = cinematicSentences[currentSentenceIndex.value];
  if (!sentence) return;

  // Mettre à jour l'image
  currentImage.value = sentence.image;
  showBackground.value = !!sentence.image;
  showVignette.value = !!sentence.image;

  // Afficher le texte
  setTimeout(() => {
    showCinematicText.value = true;
  }, 300);

  // Masquer le texte et le fond
  setTimeout(() => {
    showCinematicText.value = false;
    showBackground.value = false;

    // La vignette disparaît seulement après que l'image soit partie (fond noir complet)
    setTimeout(() => {
      showVignette.value = false;

      setTimeout(() => {
        currentSentenceIndex.value++;
        playSentence();
      }, 200); // Petit délai après disparition de la vignette
    }, FADE_DURATION);
  }, SENTENCE_DISPLAY_DURATION);
};

// ==========================================
// PASSER L'INTRO / BOUTON FINAL
// ==========================================
const skipIntro = () => {
  sessionStorage.setItem('trailer_seen', 'true');
  router.push('/home');
};

const enterSite = () => {
  sessionStorage.setItem('trailer_seen', 'true');
  router.push('/home');
};
</script>

<template>
  <div class="trailer-container">
    <!-- Image de fond avec transition -->
    <Transition name="fade">
      <img
        v-if="showBackground && currentImage"
        :src="currentImage"
        alt=""
        class="background-image"
      />
    </Transition>

    <!-- Vignette overlay (disparaît après l'image) -->
    <div v-if="showVignette && currentImage" class="vignette-overlay"></div>

    <!-- Étape 1 : Intro -->
    <div
      class="intro-layer"
      :class="{ 'slide-up': introSlidingUp }"
      v-if="step === 'intro' || introSlidingUp"
    >
      <div class="content-center">
        <h1 class="intro-title" :class="{ visible: introVisible }">{{ introText }}</h1>

        <div v-if="showScrollHint" class="scroll-hint">
          <div class="arrow"></div>
          <div class="arrow"></div>
        </div>
      </div>
    </div>

    <!-- Étape 2 : Cinématique -->
    <div v-if="step === 'cinematic'" class="content-center cinematic-layer">
      <FadeText
        v-if="currentSentence"
        :text="currentSentence.text"
        :visible="showCinematicText"
      />
    </div>

    <!-- Étape 3 : Bouton final -->
    <div v-if="step === 'end'" class="content-center end-layer">
      <button @click="enterSite" class="enter-btn">
        Entrer sur le site
      </button>
    </div>

    <!-- Bouton passer l'intro (visible dès les flèches) -->
    <button
      v-if="showScrollHint || step === 'cinematic'"
      @click="skipIntro"
      class="skip-btn"
    >
      Passer l'intro
    </button>
  </div>
</template>

<style scoped>
.trailer-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: black;
  overflow: hidden;
  z-index: 9999;
  color: white;
}

/* --- Image de fond --- */
.background-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transform: scale(1.02);
  z-index: 0;
}

/* Vignette : flou noir sur les bords */
.vignette-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(
    ellipse at center,
    transparent 60%,
    rgba(0, 0, 0, 0.6) 75%,
    rgba(0, 0, 0, 0.95) 100%
  );
  pointer-events: none;
  z-index: 1;
  /* Flou sur les bords via box-shadow inset */
  box-shadow: inset 0 0 150px 60px rgba(0, 0, 0, 0.8);
}

/* Transition fondu */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 1s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.content-center {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
  z-index: 2;
}

/* --- Intro Layer --- */
.intro-layer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: black;
  transition: transform 1s cubic-bezier(0.65, 0.05, 0.36, 1);
  z-index: 10;
}

.intro-layer.slide-up {
  transform: translateY(-100%);
}

.intro-title {
  font-size: 3rem;
  opacity: 0;
  transition: opacity 1.5s ease, transform 1.5s ease;
  transform: translateY(20px);
  font-weight: 300;
  letter-spacing: 2px;
}

.intro-title.visible {
  opacity: 1;
  transform: translateY(0);
}

/* --- Flèches de scroll --- */
.scroll-hint {
  position: absolute;
  bottom: 50px;
  display: flex;
  flex-direction: column;
  gap: 5px;
  opacity: 0;
  animation: fadeIn 1s ease forwards;
}

@keyframes fadeIn {
  to { opacity: 0.8; }
}

.arrow {
  width: 20px;
  height: 20px;
  border-right: 3px solid white;
  border-bottom: 3px solid white;
  transform: rotate(45deg);
  animation: arrow-anim 2s infinite;
}

.arrow:nth-child(2) {
  animation-delay: 0.2s;
}

@keyframes arrow-anim {
  0% { opacity: 0; transform: rotate(45deg) translate(-5px, -5px); }
  50% { opacity: 1; }
  100% { opacity: 0; transform: rotate(45deg) translate(5px, 5px); }
}

/* --- Layers --- */
.cinematic-layer,
.end-layer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

/* --- Bouton final --- */
.enter-btn {
  padding: 15px 40px;
  font-size: 1.5rem;
  background: transparent;
  color: white;
  border: 2px solid white;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 2px;
  opacity: 0;
  animation: fadeInBtn 1s ease forwards;
}

.enter-btn:hover {
  background: white;
  color: black;
}

@keyframes fadeInBtn {
  to { opacity: 1; }
}

/* --- Bouton passer l'intro --- */
.skip-btn {
  position: absolute;
  bottom: 30px;
  right: 30px;
  padding: 10px 20px;
  font-size: 0.9rem;
  background: transparent;
  color: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.4);
  cursor: pointer;
  transition: all 0.3s ease;
  letter-spacing: 1px;
  z-index: 100;
  opacity: 0;
  animation: fadeInSkip 1s ease forwards;
}

.skip-btn:hover {
  color: white;
  border-color: white;
  background: rgba(255, 255, 255, 0.1);
}

@keyframes fadeInSkip {
  to { opacity: 1; }
}

/* --- Responsive --- */
@media (max-width: 768px) {
  .intro-title {
    font-size: 1.8rem;
    padding: 0 20px;
  }

  .enter-btn {
    font-size: 1.2rem;
    padding: 12px 30px;
  }

  .skip-btn {
    bottom: 20px;
    right: 20px;
    font-size: 0.8rem;
    padding: 8px 15px;
  }
}
</style>
