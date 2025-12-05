<script setup lang="ts">
import { ref } from 'vue' // Import nécessaire pour la réactivité
import { RouterLink } from 'vue-router'
import SpriteAnimation from '@/components/TuxAnimation.vue'

// État pour gérer l'ouverture/fermeture du menu
const isMenuOpen = ref(false)

// Fonction pour basculer l'état
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

// Fonction pour fermer le menu quand on clique sur un lien
const closeMenu = () => {
  isMenuOpen.value = false
}
</script>

<template>
  <nav class="navbar">
    <div class="navbar-container">
      <RouterLink to="/home" class="navbar-logo" @click="closeMenu">
        <SpriteAnimation
          ref="tuxRef"
          :x="20"
          :y="12"
          :width="50"
          :height="50"
          :emotion="'happy'"
          :hoverEmotion="'happy'"
          :clickEmotion="'clinOeil'"
          :enableHover="true"
          :enableClick="true"
          :resetOnMouseLeave="true"
        />
      </RouterLink>

      <div class="hamburger" :class="{ active: isMenuOpen }" @click="toggleMenu">
        <span class="bar"></span>
        <span class="bar"></span>
        <span class="bar"></span>
      </div>

      <ul class="navbar-menu" :class="{ active: isMenuOpen }">
        <li><RouterLink to="/home" class="navbar-link" @click="closeMenu">Accueil</RouterLink></li>
        <li>
          <RouterLink to="/portfolio" class="navbar-link" @click="closeMenu">Portfolio</RouterLink>
        </li>
        <li>
          <RouterLink to="/sobriete-numerique" class="navbar-link" @click="closeMenu"
            >Sobriété numérique</RouterLink
          >
        </li>
        <li>
          <RouterLink to="/laser-game" class="navbar-link" @click="closeMenu"
            >Laser Game</RouterLink
          >
        </li>
        <li>
          <RouterLink to="/contact" class="navbar-link" @click="closeMenu">Contact</RouterLink>
        </li>
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
  background-color: black;
  height: 80px; /* Fixer une hauteur aide pour l'alignement */
}

.navbar-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 40px;
  height: 100%;
}

.navbar-logo {
  font-size: 1.5rem;
  font-weight: 600;
  color: white;
  text-decoration: none;
  letter-spacing: 2px;
  z-index: 101; /* Pour rester au-dessus du menu mobile si besoin */
}

/* Styles par défaut (Desktop) */
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

.navbar-link:hover,
.navbar-link.router-link-active {
  color: white;
}

/* Hamburger caché par défaut */
.hamburger {
  display: none;
  cursor: pointer;
}

.bar {
  display: block;
  width: 25px;
  height: 3px;
  margin: 5px auto;
  transition: all 0.3s ease-in-out;
  background-color: white;
}

/* --- RESPONSIVE / MOBILE --- */
@media (max-width: 768px) {
  .navbar-container {
    padding: 0 20px;
  }

  /* Afficher le burger */
  .hamburger {
    display: block;
    z-index: 101; /* Au-dessus du menu déroulant */
  }

  /* Animation du Burger en Croix (X) */
  .hamburger.active .bar:nth-child(2) {
    opacity: 0;
  }
  .hamburger.active .bar:nth-child(1) {
    transform: translateY(8px) rotate(45deg);
  }
  .hamburger.active .bar:nth-child(3) {
    transform: translateY(-8px) rotate(-45deg);
  }

  /* Transformation du menu en panneau latéral/plein écran */
  .navbar-menu {
    position: fixed;
    left: -100%; /* Caché hors de l'écran à gauche */
    top: 0; /* Commence tout en haut (sous la barre noire si on ajoute top: 80px, ou par dessus) */
    top: 80px; /* Juste en dessous de la navbar */
    flex-direction: column;
    background-color: black; /* Même couleur que la nav */
    width: 100%;
    height: calc(100vh - 80px); /* Hauteur restante */
    text-align: center;
    transition: 0.3s;
    gap: 30px;
    padding-top: 40px;
    box-shadow: 0 10px 27px rgba(0, 0, 0, 0.05);
  }

  /* Quand le menu est actif, on le ramène à 0 */
  .navbar-menu.active {
    left: 0;
  }

  .navbar-link {
    font-size: 1.2rem; /* Liens plus gros sur mobile */
  }
}
</style>
