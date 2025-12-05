<template>
  <div
    class="sprite-wrapper"
    :style="wrapperStyle"
    @mouseenter="onMouseEnter"
    @click="resetEmotion"
  >
    <!-- Layer 1 -->
    <div class="sprite-container layer-1" :style="layer1Style"></div>
    <!-- Layer 2 -->
    <div class="sprite-container layer-2" :style="layer2Style"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'

const props = defineProps({
  emotion: {
    type: String,
    default: 'normal',
    validator: (value: string) =>
      [
        'happy',
        'sad',
        'angry',
        'surprised',
        'leveMain',
        'sad2',
        'clinOeil',
        'parleSad',
        'normal',
      ].includes(value),
  },
  frameWidth: {
    type: Number,
    default: 500,
  },
  frameHeight: {
    type: Number,
    default: 500,
  },
  gap: {
    type: Number,
    default: 0,
  },
  speed: {
    type: Number,
    default: 200,
  },
  x: {
    type: Number,
    default: 0,
  },
  y: {
    type: Number,
    default: 0,
  },
  width: {
    type: Number,
    default: 500,
  },
  height: {
    type: Number,
    default: 500,
  },
  transitionDuration: {
    type: Number,
    default: 400,
  },
  waitForCycleEnd: {
    type: Boolean,
    default: true, // Si true, attend la fin du cycle avant de changer
  },
  hoverEmotion: {
    type: String,
    default: 'happy',
    validator: (value: string) =>
      [
        'happy',
        'sad',
        'angry',
        'surprised',
        'leveMain',
        'sad2',
        'clinOeil',
        'parleSad',
        'normal',
      ].includes(value),
  },
})

// États des deux layers
const currentEmotion = ref(props.emotion)
const layer1Emotion = ref(currentEmotion.value)
const layer1Frame = ref(0)
const layer1Opacity = ref(1)

const layer2Emotion = ref(currentEmotion.value)
const layer2Frame = ref(0)
const layer2Opacity = ref(0)

const activeLayer = ref(1) // 1 ou 2
const pendingEmotion = ref<string | null>(null) // Émotion en attente
let intervalId: number | null = null
const imagesPreloaded = ref(false)

const emotionImages: Record<string, string> = {
  happy: '/Ndi-2026/public/assets/tuxHappy-animation.png',
  sad: '/Ndi-2026/public/assets/tuxTriste1Larme.png',
  leveMain: '/Ndi-2026/public/assets/tuxMainDroiteLever.png',
  sad2: '/Ndi-2026/public/assets/tuxTriste2Larme.png',
  clinOeil: '/Ndi-2026/public/assets/tuxClinOeil.png',
  parleSad: '/Ndi-2026/public/assets/tuxParleTriste.png',
  normal: '/Ndi-2026/public/assets/tuxNormal.png',
}

const emotionFrames: Record<string, number> = {
  happy: 4,
  sad: 7,
  leveMain: 4,
  sad2: 9,
  clinOeil: 4,
  parleSad: 2,
  normal: 4,
}

// Préchargement des images
onMounted(() => {
  const promises = Object.values(emotionImages).map((url) => {
    return new Promise((resolve, reject) => {
      const img = new Image()
      img.onload = resolve
      img.onerror = reject
      img.src = url
    })
  })

  Promise.all(promises).then(() => {
    imagesPreloaded.value = true
    startAnimation()
  })
})

const wrapperStyle = computed(() => ({
  position: 'absolute',
  top: `${props.y}px`,
  left: `${props.x}px`,
  width: `${props.width}px`,
  height: `${props.height}px`,
}))

const getSpriteStyle = (emotion: string, frame: number, opacity: number) => {
  const scale = props.width / props.frameWidth
  const frames = emotionFrames[emotion]
  const totalImageWidth = frames * props.frameWidth + (frames - 1) * props.gap
  const positionX = -(frame * (props.frameWidth + props.gap) * scale)

  return {
    width: `${props.width}px`,
    height: `${props.height}px`,
    backgroundImage: `url(${emotionImages[emotion]})`,
    backgroundSize: `${totalImageWidth * scale}px ${props.frameHeight * scale}px`,
    backgroundPosition: `${positionX}px 0px`,
    backgroundRepeat: 'no-repeat',
    opacity: opacity,
  }
}

const layer1Style = computed(() =>
  getSpriteStyle(layer1Emotion.value, layer1Frame.value, layer1Opacity.value),
)

const layer2Style = computed(() =>
  getSpriteStyle(layer2Emotion.value, layer2Frame.value, layer2Opacity.value),
)

const startAnimation = () => {
  if (intervalId) clearInterval(intervalId)

  intervalId = setInterval(() => {
    if (activeLayer.value === 1) {
      const totalFrames = emotionFrames[layer1Emotion.value]
      const nextFrame = (layer1Frame.value + 1) % totalFrames
      layer1Frame.value = nextFrame

      // Si on revient à la frame 0 et qu'il y a une émotion en attente, on fait la transition
      if (nextFrame === 0 && pendingEmotion.value) {
        transitionToEmotion(pendingEmotion.value)
        pendingEmotion.value = null
      }
    } else {
      const totalFrames = emotionFrames[layer2Emotion.value]
      const nextFrame = (layer2Frame.value + 1) % totalFrames
      layer2Frame.value = nextFrame

      // Si on revient à la frame 0 et qu'il y a une émotion en attente, on fait la transition
      if (nextFrame === 0 && pendingEmotion.value) {
        transitionToEmotion(pendingEmotion.value)
        pendingEmotion.value = null
      }
    }
  }, props.speed)
}

const transitionToEmotion = (newEmotion: string) => {
  // Préparer le layer inactif avec la nouvelle émotion
  if (activeLayer.value === 1) {
    // Layer 2 devient actif
    layer2Emotion.value = newEmotion
    layer2Frame.value = 0

    // Crossfade
    layer2Opacity.value = 1
    layer1Opacity.value = 0

    activeLayer.value = 2
  } else {
    // Layer 1 devient actif
    layer1Emotion.value = newEmotion
    layer1Frame.value = 0

    // Crossfade
    layer1Opacity.value = 1
    layer2Opacity.value = 0

    activeLayer.value = 1
  }
}

const onMouseEnter = () => {
  currentEmotion.value = props.hoverEmotion
  transitionToEmotion(currentEmotion.value)
}

const resetEmotion = () => {
  currentEmotion.value = 'normal'
  transitionToEmotion(currentEmotion.value)
}

// Gestion du changement d'émotion avec double buffering
watch(
  () => currentEmotion.value,
  (newEmotion) => {
    if (!imagesPreloaded.value) return

    const currentEmotionValue = activeLayer.value === 1 ? layer1Emotion.value : layer2Emotion.value
    if (newEmotion === currentEmotionValue) return

    if (props.waitForCycleEnd) {
      // Mettre l'émotion en attente, elle sera appliquée à la fin du cycle actuel
      pendingEmotion.value = newEmotion
    } else {
      // Transition immédiate
      transitionToEmotion(newEmotion)
    }
  },
)

onUnmounted(() => {
  if (intervalId) clearInterval(intervalId)
})
</script>

<style scoped>
.sprite-wrapper {
  position: relative;
}

.sprite-container {
  image-rendering: pixelated;
  display: block;
  overflow: hidden;
  position: absolute;
  top: 0;
  left: 0;
  will-change: opacity;
  backface-visibility: hidden;
  transform: translateZ(0);
}
</style>
