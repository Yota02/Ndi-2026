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
  <div class="cover-page">

    <div class="content-container">
      <!-- IMAGE DE COUVERTURE -->
      <div class="cover-container">
        <div class="cover-wrapper">
          <img :src="coverImage" alt="Couverture de la BD" class="cover-img" />
        </div>
        <h1 class="title">Ma BD Portfolio</h1>
      </div>

      <!-- BOUTONS D'ACTION -->
      <div class="actions-container">
        <button @click="startChapter" class="action-btn start-btn">
          <span class="btn-text">Commencer la BD</span>
        </button>

        <a :href="cvFile" target="_blank" class="action-btn cv-btn">
          <span class="btn-text">Voir mon CV</span>
        </a>
      </div>
    </div>

  </div>
</template>

<style scoped>
.cover-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 40px 20px;
  background: #1a1a1a;
  box-sizing: border-box;
}

.content-container {
  width: 100%;
  max-width: 600px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 40px;
}

/* Section couverture */
.cover-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 25px;
  width: 100%;
}

.cover-wrapper {
  position: relative;
  width: 100%;
  max-width: 480px;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0,0,0,0.4);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  background: white;
  padding: 12px;
}

.cover-wrapper:hover {
  transform: translateY(-10px) scale(1.02);
  box-shadow: 0 30px 80px rgba(0,0,0,0.5);
}

.cover-img {
  width: 100%;
  height: auto;
  display: block;
  border-radius: 12px;
}

.title {
  font-size: 42px;
  font-weight: bold;
  color: white;
  text-align: center;
  text-shadow: 2px 4px 8px rgba(0,0,0,0.3);
  margin: 0;
  letter-spacing: 1px;
}

/* Section boutons */
.actions-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 100%;
  max-width: 400px;
  align-items: center;
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  width: 100%;
  font-size: 20px;
  font-weight: 600;
  padding: 16px 32px;
  border-radius: 12px;
  border: none;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 6px 20px rgba(0,0,0,0.2);
  position: relative;
  overflow: hidden;
}

.action-btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255,255,255,0.2);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.action-btn:hover::before {
  width: 300px;
  height: 300px;
}

.btn-icon {
  font-size: 24px;
  z-index: 1;
}

.btn-text {
  z-index: 1;
}

/* Bouton commencer */
.start-btn {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  color: white;
}

.start-btn:hover {
  background: linear-gradient(135deg, #218838 0%, #1aa179 100%);
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(40,167,69,0.4);
}

.start-btn:active {
  transform: translateY(-1px);
  box-shadow: 0 5px 15px rgba(40,167,69,0.3);
}

/* Bouton CV */
.cv-btn {
  background: linear-gradient(135deg, #007BFF 0%, #0056b3 100%);
  color: white;
}

.cv-btn:hover {
  background: linear-gradient(135deg, #0056b3 0%, #004085 100%);
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(0,123,255,0.4);
}

.cv-btn:active {
  transform: translateY(-1px);
  box-shadow: 0 5px 15px rgba(0,123,255,0.3);
}

/* Responsive design */
@media (max-width: 768px) {
  .content-container {
    gap: 35px;
  }

  .title {
    font-size: 36px;
  }

  .action-btn {
    font-size: 18px;
    padding: 14px 28px;
  }

  .btn-icon {
    font-size: 22px;
  }
}

@media (max-width: 480px) {
  .cover-page {
    padding: 30px 15px;
  }

  .content-container {
    gap: 30px;
  }

  .title {
    font-size: 30px;
  }

  .action-btn {
    font-size: 16px;
    padding: 12px 24px;
  }

  .btn-icon {
    font-size: 20px;
  }

  .cover-wrapper {
    padding: 10px;
  }
}

/* Animation d'entrée */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.cover-container,
.actions-container {
  animation: fadeInUp 0.8s ease-out;
}

.actions-container {
  animation-delay: 0.2s;
}
</style>
