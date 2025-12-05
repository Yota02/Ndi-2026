<script setup lang="ts">
/* --- 1. IMPORTS --- */
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import tuxSprite from '@/assets/Tux.png'

const router = useRouter()

// --- CONFIGURATION ---
const BEAM_MAX_LENGTH = 350
const BEAM_SPEED = 60
const SCROLL_MARGIN = 150
const SCROLL_SPEED = 12
const MAP_HEIGHT = 1500
const ENTITY_SIZE = 60 // Taille approx visuelle pour cohérence

// --- OFFSETS DU CANON (IDENTIQUES AU MODE SURVIE) ---
const GUN_OFFSETS = {
  right: { x: 25, y: 23 },
  left:  { x: -25, y: -5 },
  down:  { x: -10, y: 15 },
  up:    { x: 45, y: -8 }
};

// --- DONNÉES DU QUIZ ---
interface Question {
  id: number; x: number; y: number; prefix: string; opt1: string; opt2: string; suffix: string;
  isOption1: boolean; correctIsOption1: boolean; lastHit: number;
}

const w = window.innerWidth
const colLeft = w * 0.15
const colRight = w * 0.55

const questions = ref<Question[]>([
  { id: 1, x: colLeft,  y: 150, prefix: "Les LLMs sont ", opt1: "mauvais", opt2: "bons", suffix: " pour la planète.", isOption1: true, correctIsOption1: true, lastHit: 0 },
  { id: 2, x: colRight, y: 280, prefix: "Un mail + PJ c'est ", opt1: "lourd", opt2: "léger", suffix: " en CO2.", isOption1: false, correctIsOption1: true, lastHit: 0 },
  { id: 3, x: colLeft,  y: 410, prefix: "Le streaming c'est ", opt1: "1%", opt2: "60%", suffix: " du web.", isOption1: true, correctIsOption1: false, lastHit: 0 },
  { id: 4, x: colRight, y: 540, prefix: "Vieux smartphone : ", opt1: "Réparer", opt2: "Jeter", suffix: ".", isOption1: false, correctIsOption1: true, lastHit: 0 },
  { id: 5, x: colLeft,  y: 670, prefix: "La 4G consomme ", opt1: "moins", opt2: "plus", suffix: " que le Wifi.", isOption1: true, correctIsOption1: false, lastHit: 0 },
  { id: 6, x: colRight, y: 800, prefix: "Mode sombre OLED : ", opt1: "Utile", opt2: "Inutile", suffix: ".", isOption1: false, correctIsOption1: true, lastHit: 0 },
  { id: 7, x: colLeft,  y: 930, prefix: "Numérique vs Aviation : ", opt1: "Autant", opt2: "Moins", suffix: " de CO2.", isOption1: false, correctIsOption1: true, lastHit: 0 },
])

// --- ÉTAT DU JEU ---
const player = ref({ x: window.innerWidth / 2, y: 250, angle: -Math.PI / 2 })
const mousePos = ref({ x: 0, y: 0 })

// Animation Tux
const animState = ref({
  frameIndex: 0,
  directionRow: 0,
  flipX: false,
  lastFrameTime: 0
})

const beam = ref({
  active: false, head: 0, tail: 0, state: 'idle' as 'idle' | 'shooting' | 'finishing', angle: 0,
  startX: 0, startY: 0 // Offset visuel
})

const validationMessage = ref("")
const isSuccess = ref(false)

const containerRef = ref<HTMLDivElement | null>(null)
const wordRefs = ref<(HTMLElement | null)[]>([])

const keys = { z: false, q: false, s: false, d: false }
const gameLoopId = ref<number | null>(null)

// --- COMPUTED: STYLE DU SPRITE ---
const spriteStyle = computed(() => {
  const sheetW = 714
  const sheetH = 349
  const cols = 5
  const rows = 4

  const frameW = sheetW / cols
  const frameH = sheetH / rows

  const xPos = -(animState.value.frameIndex * frameW)
  const yPos = -(animState.value.directionRow * frameH)

  const scale = 0.9
  const scaleX = animState.value.flipX ? -scale : scale

  return {
    backgroundImage: `url(${tuxSprite})`,
    width: `${frameW}px`,
    height: `${frameH}px`,
    backgroundSize: `${sheetW}px ${sheetH}px`,
    backgroundPosition: `${xPos}px ${yPos}px`,
    position: 'absolute' as const,
    top: '50%', left: '50%',
    transformOrigin: 'center center',
    transform: `translate(-50%, -50%) scale(${scaleX}, ${scale})`,
    imageRendering: 'pixelated' as const,
    zIndex: 0
  }
})

const laserZIndex = computed(() => {
  // Si Tux est de dos (Row 0), le laser est derrière (-1)
  if (animState.value.directionRow === 0) return -1
  return 10
})

// --- ACTIONS ---
const validate = () => {
  let errors = 0
  questions.value.forEach(q => { if (q.isOption1 !== q.correctIsOption1) errors++ })

  if (errors === 0) {
    isSuccess.value = true
    validationMessage.value = "EXCELLENT ! 100% Correct ! 🌍✨"
  } else {
    isSuccess.value = false
    validationMessage.value = `Encore ${errors} erreur(s) à corriger !`
    setTimeout(() => validationMessage.value = "", 3000)
  }
}

// --- TIR AVEC OFFSET ---
const shoot = () => {
  if (beam.value.active) return

  // Calcul de la position souris DANS LE MONDE (avec scroll)
  const scrollTop = containerRef.value ? containerRef.value.scrollTop : 0
  const worldMouseY = mousePos.value.y + scrollTop

  const dx = mousePos.value.x - player.value.x
  const dy = worldMouseY - player.value.y
  const aimAngle = Math.atan2(dy, dx)

  // 1. Orienter le joueur vers la cible
  player.value.angle = aimAngle

  // 2. Calculer l'offset (Haut/Bas/Gauche/Droite)
  const deg = aimAngle * (180 / Math.PI)
  let offset = { x: 0, y: 0 }

  if (deg > -45 && deg <= 45) {
    offset = GUN_OFFSETS.right
  } else if (deg > 45 && deg <= 135) {
    offset = GUN_OFFSETS.down
  } else if (deg > -135 && deg <= -45) {
    offset = GUN_OFFSETS.up
  } else {
    offset = GUN_OFFSETS.left
  }

  // 3. Activer le tir
  beam.value.active = true
  beam.value.state = 'shooting'
  beam.value.head = 0
  beam.value.tail = 0
  beam.value.angle = aimAngle
  beam.value.startX = offset.x
  beam.value.startY = offset.y
}

// --- MISE A JOUR DIRECTION VISUELLE ---
const updateSpriteDirection = () => {
  const deg = player.value.angle * (180 / Math.PI)
  if (deg > -45 && deg <= 45) {
    animState.value.directionRow = 2; animState.value.flipX = false
  } else if (deg > 45 && deg <= 135) {
    animState.value.directionRow = 1; animState.value.flipX = false
  } else if (deg > -135 && deg <= -45) {
    animState.value.directionRow = 0; animState.value.flipX = false
  } else {
    animState.value.directionRow = 2; animState.value.flipX = true
  }
}

// --- LOGIQUE & COLLISION ---
const checkCollision = (index: number) => {
  const el = wordRefs.value[index]
  if (!el || !containerRef.value) return false

  const rect = el.getBoundingClientRect()
  const scrollTop = containerRef.value.scrollTop

  const boxLeft = rect.left
  const boxRight = rect.right
  const boxTop = rect.top + scrollTop
  const boxBottom = rect.bottom + scrollTop

  // Origine réelle du tir = Joueur + Offset Canon
  const originX = player.value.x + beam.value.startX
  const originY = player.value.y + beam.value.startY

  const endX = originX + Math.cos(beam.value.angle) * beam.value.head
  const endY = originY + Math.sin(beam.value.angle) * beam.value.head

  const margin = 10
  return (
    endX >= boxLeft - margin &&
    endX <= boxRight + margin &&
    endY >= boxTop - margin &&
    endY <= boxBottom + margin
  )
}

const update = (timestamp: number) => {
  const scrollTop = containerRef.value ? containerRef.value.scrollTop : 0
  const containerHeight = window.innerHeight

  // 1. Mouvement
  let dx = 0
  let dy = 0
  if (keys.z && player.value.y > 0) dy -= 1
  if (keys.s && player.value.y < MAP_HEIGHT) dy += 1
  if (keys.q && player.value.x > 0) dx -= 1
  if (keys.d && player.value.x < window.innerWidth) dx += 1

  const isMoving = dx !== 0 || dy !== 0

  // Vitesse constante même en diagonale
  const speed = 5
  if (isMoving) {
    const moveSpeed = (dx !== 0 && dy !== 0) ? speed / 1.414 : speed
    player.value.x += dx * moveSpeed
    player.value.y += dy * moveSpeed
  }

  // 2. Scroll Auto (Gameplay spécifique au Quiz)
  if (containerRef.value) {
    const playerScreenY = player.value.y - scrollTop
    if (playerScreenY > containerHeight - SCROLL_MARGIN) containerRef.value.scrollTop += SCROLL_SPEED
    if (playerScreenY < SCROLL_MARGIN && scrollTop > 0) containerRef.value.scrollTop -= SCROLL_SPEED
  }

  // 3. Orientation : Priorité Tir > Mouvement
  if (!beam.value.active && isMoving) {
    player.value.angle = Math.atan2(dy, dx)
  }

  // 4. Animation Marche
  if (isMoving) {
    if (timestamp - animState.value.lastFrameTime > 120) {
      animState.value.frameIndex = (animState.value.frameIndex + 1) % 5
      animState.value.lastFrameTime = timestamp
    }
  } else {
    animState.value.frameIndex = 0
  }

  // 5. Mise à jour Sprite
  updateSpriteDirection()

  // 6. Animation Laser
  if (beam.value.active) {
    if (beam.value.state === 'shooting') {
      beam.value.head += BEAM_SPEED
      if (beam.value.head >= BEAM_MAX_LENGTH) {
        beam.value.head = BEAM_MAX_LENGTH
        beam.value.state = 'finishing'
      }
    } else {
      beam.value.tail += BEAM_SPEED
      if (beam.value.tail >= beam.value.head) {
        beam.value.active = false
        beam.value.state = 'idle'
      }
    }

    const now = Date.now()
    questions.value.forEach((q, i) => {
      if (now - q.lastHit > 500 && checkCollision(i)) {
        q.isOption1 = !q.isOption1
        q.lastHit = now
        beam.value.state = 'finishing'
      }
    })
  }
  gameLoopId.value = requestAnimationFrame(update)
}

// --- LISTENERS ---
const handleKeyDown = (e: KeyboardEvent) => { if(e.key.toLowerCase() in keys) keys[e.key.toLowerCase() as keyof typeof keys] = true }
const handleKeyUp = (e: KeyboardEvent) => { if(e.key.toLowerCase() in keys) keys[e.key.toLowerCase() as keyof typeof keys] = false }
const handleMouseMove = (e: MouseEvent) => { mousePos.value = { x: e.clientX, y: e.clientY } }

onMounted(() => {
  gameLoopId.value = requestAnimationFrame(update)
  window.addEventListener('keydown', handleKeyDown)
  window.addEventListener('keyup', handleKeyUp)
  if(window.innerWidth < 800) questions.value.forEach(q => q.x = 20)
})

onUnmounted(() => {
  if (gameLoopId.value) cancelAnimationFrame(gameLoopId.value)
  window.removeEventListener('keydown', handleKeyDown)
  window.removeEventListener('keyup', handleKeyUp)
})
</script>

<template>
  <div class="quiz-container" ref="containerRef" @mousemove="handleMouseMove" @mousedown="shoot">

    <div class="fixed-ui-layer">
      <div class="header-panel">

        <button @click="router.push('/')" @mousedown.stop class="back-btn">⬅ Retour</button>
        <h1 class="title">QUIZ LASER 🐧</h1>
        <p class="subtitle">Utilisez ZQSD pour vous déplacer !</p>
      </div>

      <div v-if="validationMessage" class="feedback" :class="{ 'success': isSuccess }">
        {{ validationMessage }}
      </div>

      <div class="bottom-bar">
        <button @click.stop="validate" @mousedown.stop class="validate-btn">✅ VÉRIFIER</button>
      </div>
    </div>

    <div class="world-layer" :style="{ height: MAP_HEIGHT + 'px' }">
      <div
        v-for="(q, index) in questions"
        :key="q.id"
        class="question-item"
        :style="{ top: q.y + 'px', left: q.x + 'px' }"
      >
        <span class="text-base">{{ q.prefix }}</span>
        <span
          :ref="(el) => wordRefs[index] = (el as HTMLElement)"
          class="target-word"
          :class="q.isOption1 ? 'opt-red' : 'opt-green'"
        >
          {{ q.isOption1 ? q.opt1 : q.opt2 }}
        </span>
        <span class="text-base">{{ q.suffix }}</span>
      </div>

      <div class="player-wrapper" :style="{ transform: `translate(${player.x}px, ${player.y}px)` }">

        <div
          class="laser-pivot"
          :style="{
             transform: `translate(${beam.startX}px, ${beam.startY}px) rotate(${beam.angle}rad)`,
             zIndex: laserZIndex
          }"
        >
          <div v-if="beam.active" class="laser-beam" :style="{ left: beam.tail + 'px', width: (beam.head - beam.tail) + 'px' }">
            <div class="laser-core"></div>
            <div class="laser-glow"></div>
          </div>
        </div>

        <div :style="spriteStyle"></div>

      </div>
    </div>

  </div>
</template>

<style scoped>
.quiz-container {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  width: 100vw; height: 100vh;
  background-color: #111;
  color: white;
  overflow-y: auto;
  z-index: 9999;
  cursor: crosshair;
  user-select: none;
}

/* UI Fixe */
.fixed-ui-layer { position: sticky; top: 0; left: 0; width: 100%; height: 0; z-index: 100; pointer-events: none; }
.header-panel { pointer-events: auto; background: rgba(17, 17, 17, 0.95); padding: 10px; border-bottom: 2px solid #42b883; }
.back-btn { float: left; background: transparent; border: 1px solid white; color: white; padding: 5px 15px; cursor: pointer; border-radius: 4px; font-family: sans-serif; }
.back-btn:hover { background: white; color: black; }
.title { text-align: center; margin: 0; color: #42b883; font-size: 1.5rem; text-transform: uppercase; letter-spacing: 2px; }
.subtitle { text-align: center; color: #888; margin: 0; font-size: 0.9rem; }

.bottom-bar { position: fixed; bottom: 20px; width: 100%; display: flex; justify-content: center; pointer-events: none; }
.validate-btn { pointer-events: auto; padding: 15px 40px; font-size: 1.5rem; background: #42b883; color: white; border: none; border-radius: 50px; cursor: pointer; box-shadow: 0 5px 15px rgba(0,0,0,0.3); font-weight: bold; transition: transform 0.2s; }
.validate-btn:hover { background: #3aa876; transform: scale(1.1); }
.feedback { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(0,0,0,0.95); padding: 40px; border-radius: 15px; font-size: 2rem; border: 4px solid #ff4444; pointer-events: none; text-align: center; }
.feedback.success { border-color: #42b883; color: #42b883; }

/* Monde */
.world-layer { position: relative; width: 100%; }

/* --- STYLE DES TEXTES --- */
.question-item {
  position: absolute;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  white-space: nowrap;
  display: flex;
  align-items: center;
}

.text-base { font-size: 1.3rem; color: #ccc; }

.target-word {
  display: inline-block;
  padding: 5px 10px;
  margin: 0 5px;
  font-weight: 800; /* Gras */
  font-size: 1.5rem;
  cursor: crosshair;
  transition: transform 0.2s, color 0.2s, text-shadow 0.2s;
}

.target-word:hover { transform: scale(1.1); }

.opt-red { color: #ff5555; text-shadow: 0 0 10px rgba(255, 85, 85, 0.6), 0 0 20px rgba(255, 85, 85, 0.3); }
.opt-green { color: #42b883; text-shadow: 0 0 10px rgba(66, 184, 131, 0.6), 0 0 20px rgba(66, 184, 131, 0.3); }

/* JOUEUR & LASER */
.player-wrapper { position: absolute; top: 0; left: 0; pointer-events: none; z-index: 50; will-change: transform; }
.laser-pivot { position: absolute; top: 0; left: 0; width: 0; height: 0; }
.laser-beam { position: absolute; top: -15px; height: 0; z-index: 10; pointer-events: none; }
.laser-core { position: absolute; top: -3px; left: 0; width: 100%; height: 6px; background-color: white; border-radius: 3px; box-shadow: 0 0 5px white; }
.laser-glow { position: absolute; top: -8px; left: 0; width: 100%; height: 16px; background: transparent; box-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff; border-radius: 8px; opacity: 0.6; }
</style>
