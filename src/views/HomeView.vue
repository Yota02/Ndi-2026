<script setup lang="ts">
import NavBar from '@/components/NavBar.vue';
</script>

<template>
  <div class="home-page">
    <NavBar />

    <main class="hero">
      <h1 class="hero-title">Bienvenue sur la page d'accueil</h1>
    </main>
  </div>
</template>

<style scoped>
.home-page {
  min-height: 100vh;
  background-color: #000;
  color: white;
}

.hero {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  padding: 0 20px;
}

.hero-title {
  font-size: 3rem;
  font-weight: 300;
  letter-spacing: 3px;
  text-align: center;
  opacity: 0;
  animation: fadeIn 1.5s ease forwards;
}

@keyframes fadeIn {
  to {
    opacity: 1;
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 1.8rem;
  }
}
</style>
