<template>
  <div class="sprite-container" :style="spriteStyle"></div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'

// Définition des propriétés pour rendre le composant flexible
const props = defineProps({
  imageUrl: {
    type: String,
    required: true,
  },
  frameWidth: {
    type: Number,
    default: 500, // Largeur d'un pingouin
  },
  frameHeight: {
    type: Number,
    default: 500, // Hauteur du pingouin (à ajuster selon votre image réelle)
  },
  gap: {
    type: Number,
    default: 20, // L'espace entre chaque pingouin
  },
  totalFrames: {
    type: Number,
    default: 4, // Il y a 4 pingouins sur votre image
  },
  speed: {
    type: Number,
    default: 200, // Vitesse en millisecondes entre chaque frame
  },
  x: {
    type: Number,
    default: 0, // Coordonnée X pour le positionnement absolu
  },
  y: {
    type: Number,
    default: 0, // Coordonnée Y pour le positionnement absolu
  },
  width: {
    type: Number,
    default: 500, // Largeur du composant, par défaut égale à frameWidth
  },
  height: {
    type: Number,
    default: 500, // Hauteur du composant, par défaut égale à frameHeight
  },
})

const currentFrame = ref(0)
let intervalId = null

// Calcul dynamique de la position de l'image de fond
const spriteStyle = computed(() => {
  // Calcul du facteur d'échelle basé sur la largeur
  const scale = props.width / props.frameWidth

  // Largeur totale de l'image (frames + écarts)
  const totalImageWidth = props.totalFrames * props.frameWidth + (props.totalFrames - 1) * props.gap

  // Position X ajustée à l'échelle
  const positionX = -(currentFrame.value * (props.frameWidth + props.gap) * scale)

  return {
    width: `${props.width}px`,
    height: `${props.height}px`,
    backgroundImage: `url(${props.imageUrl})`,
    backgroundSize: `${totalImageWidth * scale}px ${props.frameHeight * scale}px`,
    backgroundPosition: `${positionX}px 0px`,
    backgroundRepeat: 'no-repeat',
    position: 'absolute',
    top: `${props.y}px`,
    left: `${props.x}px`,
  }
})

// Lancement de l'animation
const startAnimation = () => {
  intervalId = setInterval(() => {
    // On passe à la frame suivante, et on revient à 0 après la dernière
    currentFrame.value = (currentFrame.value + 1) % props.totalFrames
  }, props.speed)
}

// Hooks du cycle de vie Vue
onMounted(() => {
  startAnimation()
})

onUnmounted(() => {
  // Nettoyage impératif pour éviter les fuites de mémoire
  if (intervalId) clearInterval(intervalId)
})
</script>

<style scoped>
.sprite-container {
  /* Assure que l'image s'affiche net (pixel art) si on redimensionne,
     bien que ce ne soit pas le cas ici */
  image-rendering: pixelated;

  /* Pour centrer ou ajouter des bordures si nécessaire */
  display: inline-block;
  overflow: hidden; /* Sécurité pour ne pas voir le voisin */
}
</style>
