<template>
  <div class="chapter">

    <!-- BOUTONS NAVIGATION TOP -->
    <div class="top-buttons">
      <button class="top-nav-button" @click="goToPortfolio" aria-label="Voir le portfolio">
        📄
      </button>
      <button class="top-nav-button" @click="goHome" aria-label="Retour à l'accueil">
        🏠
      </button>
    </div>

    <!-- FLECHE GAUCHE ⬅️ -->
    <button v-if="showPrev" class="nav-arrow prev" @click="goPrev" aria-label="Page précédente">
      <span>⬅️</span>
    </button>

    <!-- CONTENU -->
    <div v-if="!isEnd" class="content-wrapper">
      <div class="chapter-content">
        <h2 class="chapter-text">{{ chapterText }}</h2>
        <div class="grid-container" :class="{ 
          'grid-four': chapterImages.length === 4, 
          'grid-three': chapterImages.length === 3,
          'grid-two': chapterImages.length === 2 
        }">
          <div v-for="i in 4" :key="i" class="grid-item">
            <div v-if="chapterImages[i-1]" class="image-wrapper">
              <img :src="chapterImages[i-1]" :alt="`Chapitre ${chapterId} - Image ${i}`" class="chapter-img"/>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="end-wrapper">
      <div class="end-content">
        <img :src="endImage" alt="Fin de la BD" class="end-img" />
      </div>
    </div>

    <!-- FLECHE DROITE ➡️ -->
    <button v-if="showNext && !isEnd" class="nav-arrow next" @click="goNext" aria-label="Page suivante">
      <span>➡️</span>
    </button>

  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

// Import images
import chap1_1 from '@/assets/portfolio/chap1_1.png'
import chap1_2 from '@/assets/portfolio/chap1_2.png'
import chap1_3 from '@/assets/portfolio/chap1_3.png'
import chap2_1 from '@/assets/portfolio/chap2_1.png'
import chap2_2 from '@/assets/portfolio/chap2_2.png'
import chap3_1 from '@/assets/portfolio/chap3_1.png'
import chap3_2 from '@/assets/portfolio/chap3_2.png'
import chap3_3 from '@/assets/portfolio/chap3_3.png'
import chap3_4 from '@/assets/portfolio/chap3_4.png'
import chap4_1 from '@/assets/portfolio/chap4_1.png'
import chap4_2 from '@/assets/portfolio/chap4_2.png'
import chap4_3 from '@/assets/portfolio/chap4_3.png'
import endImage from '@/assets/portfolio/end.jpg'

const route = useRoute()
const router = useRouter()

const chapters = {
  1: [chap1_1, chap1_2, chap1_3],
  2: [chap2_1, chap2_2],
  3: [chap3_1, chap3_2, chap3_3, chap3_4],
  4: [chap4_1, chap4_2, chap4_3]
}

const chapterTexts = {
  1: "Tuxy vivait paisiblement avec sa famille dans la banquise Unix",
  2: "La banquise fond à cause de la Big Tech, surtout Windows et Apple",
  3: "La banquise de Tuxy continue à fondre, et rencontre Nirdie",
  4: "Tuxy et Nirdie vont dans les établissements scolaires pour sensibiliser sur le numérique libre et écocitoyen"
}

const chapterId = ref(Number(route.params.id))
const chapterImages = ref(chapters[chapterId.value])
const chapterText = ref(chapterTexts[chapterId.value])
const isEnd = ref(false)

watch(() => route.params.id, (newId) => {
  chapterId.value = Number(newId)
  chapterImages.value = chapters[chapterId.value]
  chapterText.value = chapterTexts[chapterId.value]
  isEnd.value = false
})

const showPrev = () => chapterId.value > 0
const showNext = () => chapterId.value <= 4

function goPrev() {
  if (isEnd.value) {
    isEnd.value = false
  } else if (chapterId.value === 1) {
    router.push('/')
  } else {
    router.push(`/chapter/${chapterId.value - 1}`)
  }
}

function goNext() {
  if (chapterId.value < 4) {
    router.push(`/chapter/${chapterId.value + 1}`)
  } else if (chapterId.value === 4) {
    isEnd.value = true
  }
}

function goHome() {
  router.push('/')
}

function goToPortfolio() {
  router.push('/portfolio')
}
</script>

<style scoped>
.chapter {
  position: relative;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 20px;
  background: #1a1a1a;
  box-sizing: border-box;
}

/* Wrapper pour le contenu principal */
.content-wrapper {
  width: 100%;
  max-width: 1400px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.chapter-content {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px;
}

.chapter-text {
  font-size: 28px;
  font-weight: 600;
  color: #ffffff;
  text-align: center;
  margin: 0;
  padding: 0 20px;
  max-width: 900px;
  line-height: 1.4;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
}

/* GRID - système flexible */
.grid-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 30px;
  width: 100%;
  max-width: 1200px;
  padding: 20px;
}

/* Alignement pour 4 images - GRID */
.grid-container.grid-four {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  justify-items: center;
}

/* Alignement pour 3 images - GRID */
.grid-container.grid-three {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  justify-items: center;
}

/* Centrage pour 2 images - GRID */
.grid-container.grid-two {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  justify-items: center;
  max-width: 700px;
}

.grid-item {
  width: 100%;
  max-width: 280px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.image-wrapper {
  width: 100%;
  position: relative;
  overflow: hidden;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  background: white;
  padding: 8px;
}

.image-wrapper:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 32px rgba(0,0,0,0.25);
}

.chapter-img {
  width: 100%;
  height: auto;
  display: block;
  border-radius: 8px;
}

/* Page de fin */
.end-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.end-content {
  text-align: center;
  max-width: 800px;
}

.end-img {
  width: 100%;
  max-width: 700px;
  border-radius: 16px;
  box-shadow: 0 12px 40px rgba(0,0,0,0.5);
}

/* Flèches de navigation */
.nav-arrow {
  position: fixed;
  top: 50%;
  transform: translateY(-50%);
  font-size: 48px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 10px;
  z-index: 100;
  transition: all 0.3s ease;
}

.nav-arrow:hover {
  transform: translateY(-50%) scale(1.2);
}

.nav-arrow:active {
  transform: translateY(-50%) scale(1);
}

.prev { 
  left: 30px; 
}

.next { 
  right: 30px; 
}

/* Bouton Home */
.home-button {
  position: fixed;
  top: 20px;
  right: 20px;
  font-size: 32px;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 50%;
  cursor: pointer;
  padding: 12px 16px;
  z-index: 100;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

.home-button:hover {
  transform: scale(1.15);
  background: rgba(255, 255, 255, 1);
  box-shadow: 0 6px 20px rgba(0,0,0,0.4);
}

.home-button:active {
  transform: scale(1);
}

/* Boutons de navigation en haut */
.top-buttons {
  position: fixed;
  top: 20px;
  right: 20px;
  display: flex;
  gap: 15px;
  z-index: 100;
}

.top-nav-button {
  font-size: 32px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 10px;
  transition: all 0.3s ease;
}

.top-nav-button:hover {
  transform: scale(1.2);
}

.top-nav-button:active {
  transform: scale(1);
}

/* Responsive design */
@media (max-width: 1200px) {
  .grid-container.grid-four,
  .grid-container.grid-three {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .grid-item {
    max-width: 320px;
  }
}

@media (max-width: 768px) {
  .chapter {
    padding: 30px 15px;
  }
  
  .chapter-text {
    font-size: 22px;
    padding: 0 15px;
  }
  
  .grid-container {
    gap: 25px;
    max-width: 400px;
  }
  
  .grid-container.grid-four,
  .grid-container.grid-three,
  .grid-container.grid-two {
    grid-template-columns: 1fr;
  }
  
  .grid-item {
    max-width: 100%;
  }
  
  .nav-arrow {
    font-size: 36px;
    padding: 8px;
  }
  
  .prev { left: 15px; }
  .next { right: 15px; }
  
  .top-buttons {
    top: 15px;
    right: 15px;
    gap: 12px;
  }
  
  .top-nav-button {
    font-size: 28px;
    padding: 8px;
  }
}

@media (max-width: 480px) {
  .chapter-text {
    font-size: 18px;
  }
  
  .nav-arrow {
    font-size: 28px;
    padding: 6px;
  }
  
  .prev { left: 10px; }
  .next { right: 10px; }
  
  .top-buttons {
    top: 10px;
    right: 10px;
    gap: 10px;
  }
  
  .top-nav-button {
    font-size: 24px;
    padding: 6px;
  }
}
</style>