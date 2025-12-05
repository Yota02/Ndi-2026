<template>
  <div class="sprite-container" :style="spriteStyle"></div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'

// Définition des propriétés pour rendre le composant flexible
const props = defineProps({
  emotion: {
    type: String,
    required: true,
    validator: (value: string) => ['happy', 'sad', 'angry', 'surprised'].includes(value),
  },
  frameWidth: {
    type: Number,
    default: 500, // Largeur d'un pingouin
  },
  frameHeight: {
    type: Number,
    default: 500, // Hauteur du pingouin
  },
  gap: {
    type: Number,
    default: 0, // L'espace entre chaque pingouin
  },
  speed: {
    type: Number,
    default: 100, // Vitesse en millisecondes entre chaque frame
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
    default: 500, // Largeur du composant
  },
  height: {
    type: Number,
    default: 500, // Hauteur du composant
  },
})

const currentFrame = ref(0)
let intervalId: number | null = null

// Mapping des émotions vers les URLs des images
const emotionImages: Record<string, string> = {
  happy: '/Ndi-2026/public/assets/tuxHappy-animation.png',
  sad: '/Ndi-2026/public/assets/tuxTriste1Larme.png',
  leveMain: '/Ndi-2026/public/assets/tuxMainDroiteLever.png',
  sad2: '/Ndi-2026/public/assets/tuxTriste2Larme.png',
  clinOeil: '/Ndi-2026/public/assets/tuxClinOeil.png',
  parleSad: '/Ndi-2026/public/assets/tuxParleTriste.png',
  normal: '/Ndi-2026/public/assets/tuxNormal.png',
}

// Mapping des émotions vers le nombre de frames
const emotionFrames: Record<string, number> = {
  happy: 4,
  sad: 7,
  leveMain: 4,
  sad2: 9,
  clinOeil: 4,
  parleSad: 2,
  normal: 4,
}

// Récupération de l'URL de l'image basée sur l'émotion
const imageUrl = computed(() => emotionImages[props.emotion])

// Calcul du nombre total de frames basé sur l'émotion
const totalFrames = computed(() => emotionFrames[props.emotion])

// Calcul dynamique de la position de l'image de fond
const spriteStyle = computed(() => {
  // Calcul du facteur d'échelle basé sur la largeur
  const scale = props.width / props.frameWidth

  // Largeur totale de l'image (frames + écarts)
  const totalImageWidth = totalFrames.value * props.frameWidth + (totalFrames.value - 1) * props.gap

  // Position X ajustée à l'échelle
  const positionX = -(currentFrame.value * (props.frameWidth + props.gap) * scale)

  return {
    width: `${props.width}px`,
    height: `${props.height}px`,
    backgroundImage: `url(${imageUrl.value})`,
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
    currentFrame.value = (currentFrame.value + 1) % totalFrames.value
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
  /* Assure que l'image s'affiche net (pixel art) si on redimensionne */
  image-rendering: pixelated;
  display: inline-block;
  overflow: hidden; /* Sécurité pour ne pas voir le voisin */
}
</style>
