<script setup lang="ts">
import { RouterLink } from 'vue-router';
</script>

<template>
  <nav class="navbar">
    <div class="navbar-container">
      <RouterLink to="/home" class="navbar-logo">
        Logo
      </RouterLink>

      <ul class="navbar-menu">
        <li><RouterLink to="/home" class="navbar-link">Accueil</RouterLink></li>
        <li><RouterLink to="/portfolio" class="navbar-link">Portfolio</RouterLink></li>
        <li><RouterLink to="/sobriete-numerique" class="navbar-link">Sobriété numérique</RouterLink></li>
        <li><RouterLink to="/laser-game" class="navbar-link">Laser Game</RouterLink></li>
        <li><RouterLink to="/contact" class="navbar-link">Contact</RouterLink></li>
      </ul>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 100;
  background: transparent;
}

.navbar-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px 40px;
}

.navbar-logo {
  font-size: 1.5rem;
  font-weight: 600;
  color: white;
  text-decoration: none;
  letter-spacing: 2px;
}

.navbar-menu {
  display: flex;
  list-style: none;
  gap: 40px;
  margin: 0;
  padding: 0;
}

.navbar-link {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  font-size: 0.95rem;
  letter-spacing: 1px;
  transition: color 0.3s ease;
}

.navbar-link:hover {
  color: white;
}

.navbar-link.router-link-active {
  color: white;
}

@media (max-width: 768px) {
  .navbar-container {
    padding: 15px 20px;
  }

  .navbar-menu {
    gap: 20px;
  }

  .navbar-link {
    font-size: 0.85rem;
  }
}
</style>
