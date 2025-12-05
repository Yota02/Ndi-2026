<script setup lang="ts">
/* --- 1. IMPORTS & DEFINITIONS --- */
import { ref, onMounted, onUnmounted, computed, nextTick, type CSSProperties } from 'vue'
import tuxSprite from '@/assets/Tux.png'
import sadTuxSprite from '@/assets/SadTux.png'
import cookedChickenImg from '@/assets/CookedChicken.png'

// Événements émis vers le parent
const emit = defineEmits<{
  (e: 'close'): void
}>()

/* --- 2. CONFIGURATION (CONSTANTES) --- */
const CONFIG = {
  TEMP: { START: 1.2, MAX: 2.0, MIN: 0.0 },
  SPAWN_RATE: 2000,
  ENTITY: { SPEED: 1.5, SIZE: 60 },
  BOT: {
    SPAWN_RATE: 5000,
    SPEED: 2.5,
    SIZE: 40,
    FIRE_RATE: 2500,
    MAX_SPEED: 3.5,
    WANDER_SPEED: 1.5,
    PANIC_DIST: 350,
    FRICTION: 0.95
  },
  BULLET: { SPEED: 7, SIZE: 12 },
  SCORE: { POLLUTION: 100, BOT: 300, NATURE_PENALTY: 50 },
  BEAM: { MAX_LENGTH: 350, SPEED: 40 },
  GUN_OFFSETS: {
    right: { x: 25, y: 23 },
    left: { x: -25, y: -5 },
    down: { x: -10, y: 15 },
    up: { x: 45, y: -8 }
  }
} as const

const BAD_EMOJIS = ['🛢️', '☢️', '🏭', '🚗', '✈️', '🚬', '🗑️', '🔋']
const GOOD_EMOJIS = ['🌳', '🌲', '🌱', '🌿', '🌻', '🌵', '🍄', '🦊', '🐻']

/* --- 3. TYPES --- */
interface GameEntity {
  id: number
  x: number
  y: number
  vx: number
  vy: number
  type: 'tree' | 'pollution'
  emoji: string
  hit: boolean
}

interface BotEntity {
  id: number
  x: number
  y: number
  vx: number
  vy: number
  lastShot: number
  changeDirTimer: number
}

interface Projectile {
  id: number
  x: number
  y: number
  vx: number
  vy: number
}

/* --- 4. ÉTAT DU JEU (REFS) --- */
// Conteneur et Dimensions
const containerRef = ref<HTMLDivElement | null>(null)
const gameBounds = ref({ w: 1000, h: 800 }) // Valeurs par défaut

// État Global
const temperature = ref(CONFIG.TEMP.START)
const score = ref(0)
const isGameOver = ref(false)
const isGameStarted = ref(false)
const countdown = ref(3)
const gameOverMessage = ref("")

// Timers
const gameLoopId = ref<number | null>(null)
const spawnerId = ref<number | null>(null)
const botSpawnerId = ref<number | null>(null)

// Joueur
const player = ref({ x: 0, y: 0, angle: 0, radius: 25 })
const mousePos = ref({ x: 0, y: 0 })
const currentSprite = ref(tuxSprite)
const animState = ref({ frameIndex: 0, directionRow: 0, flipX: false, lastFrameTime: 0 })
const keys = { z: false, q: false, s: false, d: false }

// Arme
const beam = ref({
  active: false,
  head: 0,
  tail: 0,
  state: 'idle' as 'idle' | 'shooting' | 'finishing',
  angle: 0,
  startX: 0,
  startY: 0
})

// Collections d'entités
const entities = ref<GameEntity[]>([])
const bots = ref<BotEntity[]>([])
const enemyProjectiles = ref<Projectile[]>([])

/* --- 5. COMPUTED PROPERTIES --- */
const spriteStyle = computed<CSSProperties>(() => {
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
    backgroundImage: `url(${currentSprite.value})`,
    width: `${frameW}px`,
    height: `${frameH}px`,
    backgroundSize: `${sheetW}px ${sheetH}px`,
    backgroundPosition: `${xPos}px ${yPos}px`,
    position: 'absolute',
    top: '50%',
    left: '50%',
    transformOrigin: 'center center',
    transform: `translate(-50%, -50%) scale(${scaleX}, ${scale})`,
    imageRendering: 'pixelated',
    zIndex: 0
  }
})

const laserZIndex = computed(() => (animState.value.directionRow === 0 ? -1 : 10))

const screenBackground = computed(() => {
  const opacity = 0.85
  let r = 0, b = 0
  if (temperature.value > CONFIG.TEMP.START) {
    r = Math.floor((temperature.value - CONFIG.TEMP.START) / (CONFIG.TEMP.MAX - CONFIG.TEMP.START) * 150)
  } else {
    b = Math.floor((CONFIG.TEMP.START - temperature.value) / CONFIG.TEMP.START * 150)
  }
  return `rgba(${r}, 0, ${b}, ${opacity})`
})

const tempColor = computed(() => {
  if (temperature.value >= 1.8) return '#ff4444'
  if (temperature.value <= 0.5) return '#4444ff'
  return '#ffffff'
})

/* --- 6. MÉTHODES DE JEU --- */

// Met à jour les dimensions du jeu
const updateBounds = () => {
  if (containerRef.value) {
    gameBounds.value.w = containerRef.value.clientWidth
    gameBounds.value.h = containerRef.value.clientHeight
  }
}

// Spawners
const spawnEntity = () => {
  if (isGameOver.value || !isGameStarted.value) return
  const isPollution = Math.random() > 0.6
  const list = isPollution ? BAD_EMOJIS : GOOD_EMOJIS
  const emoji = list[Math.floor(Math.random() * list.length)]

  const x = Math.random() * (gameBounds.value.w - CONFIG.ENTITY.SIZE)
  const y = Math.random() * (gameBounds.value.h - CONFIG.ENTITY.SIZE)
  const angle = Math.random() * Math.PI * 2

  entities.value.push({
    id: performance.now() + Math.random(),
    x, y,
    vx: Math.cos(angle) * CONFIG.ENTITY.SPEED,
    vy: Math.sin(angle) * CONFIG.ENTITY.SPEED,
    type: isPollution ? 'pollution' : 'tree',
    emoji,
    hit: false
  })
}

const spawnBot = () => {
  if (isGameOver.value || !isGameStarted.value) return
  const { w, h } = gameBounds.value

  // Apparaître sur les bords ou aléatoirement
  const x = Math.random() > 0.5 ? Math.random() * w : (Math.random() > 0.5 ? 0 : w)
  const y = Math.random() * h

  bots.value.push({
    id: performance.now() + Math.random(),
    x: Math.min(Math.max(x, 0), w - CONFIG.BOT.SIZE),
    y: Math.min(Math.max(y, 0), h - CONFIG.BOT.SIZE),
    vx: 0, vy: 0,
    lastShot: performance.now(),
    changeDirTimer: 0
  })
}

// Gestion des Inputs
const handleKeyDown = (e: KeyboardEvent) => {
  const k = e.key.toLowerCase()
  if (k in keys) keys[k as keyof typeof keys] = true
  if (e.key === 'Escape') emit('close')
}
const handleKeyUp = (e: KeyboardEvent) => {
  const k = e.key.toLowerCase()
  if (k in keys) keys[k as keyof typeof keys] = false
}
const handleMouseMove = (e: MouseEvent) => {
  // Calculer la position relative au conteneur si possible
  if (containerRef.value) {
    const rect = containerRef.value.getBoundingClientRect()
    mousePos.value.x = e.clientX - rect.left
    mousePos.value.y = e.clientY - rect.top
  } else {
    mousePos.value.x = e.clientX
    mousePos.value.y = e.clientY
  }
}

// Logique de Tir
const shoot = () => {
  if (isGameOver.value || beam.value.active || !isGameStarted.value) return

  const dx = mousePos.value.x - player.value.x
  const dy = mousePos.value.y - player.value.y
  const aimAngle = Math.atan2(dy, dx)
  player.value.angle = aimAngle

  const deg = aimAngle * (180 / Math.PI)
  let offset = CONFIG.GUN_OFFSETS.right

  if (deg > 45 && deg <= 135) offset = CONFIG.GUN_OFFSETS.down
  else if (deg > -135 && deg <= -45) offset = CONFIG.GUN_OFFSETS.up
  else if (deg > 135 || deg <= -135) offset = CONFIG.GUN_OFFSETS.left

  beam.value.active = true
  beam.value.state = 'shooting'
  beam.value.head = 0
  beam.value.tail = 0
  beam.value.angle = aimAngle
  beam.value.startX = offset.x
  beam.value.startY = offset.y
}

const updateSpriteDirection = () => {
  const deg = player.value.angle * (180 / Math.PI)
  if (deg > -45 && deg <= 45) { animState.value.directionRow = 2; animState.value.flipX = false }
  else if (deg > 45 && deg <= 135) { animState.value.directionRow = 1; animState.value.flipX = false }
  else if (deg > -135 && deg <= -45) { animState.value.directionRow = 0; animState.value.flipX = false }
  else { animState.value.directionRow = 2; animState.value.flipX = true }
}

// Collisions
const checkLaserCollision = (targetX: number, targetY: number, radius: number) => {
  const originX = player.value.x + beam.value.startX
  const originY = player.value.y + beam.value.startY
  const startX = originX + Math.cos(beam.value.angle) * beam.value.tail
  const startY = originY + Math.sin(beam.value.angle) * beam.value.tail
  const endX = originX + Math.cos(beam.value.angle) * beam.value.head
  const endY = originY + Math.sin(beam.value.angle) * beam.value.head

  const dx = endX - startX
  const dy = endY - startY

  if (dx === 0 && dy === 0) return false

  const t = Math.max(0, Math.min(1, ((targetX - startX) * dx + (targetY - startY) * dy) / (dx * dx + dy * dy)))
  const nearestX = startX + t * dx
  const nearestY = startY + t * dy

  return Math.hypot(nearestX - targetX, nearestY - targetY) < (radius + 10)
}

const checkCircleCollision = (c1: {x: number, y: number, r: number}, c2: {x: number, y: number, r: number}) => {
  const dist = Math.hypot(c1.x - c2.x, c1.y - c2.y)
  return dist < (c1.r + c2.r)
}

// Boucle Principale
const update = (timestamp: number) => {
  if (isGameOver.value) return
  if (!containerRef.value) return // Sécurité

  // Gestion pré-game (Tux suit la souris)
  if (!isGameStarted.value) {
    const dx = mousePos.value.x - player.value.x
    const dy = mousePos.value.y - player.value.y
    player.value.angle = Math.atan2(dy, dx)
    updateSpriteDirection()
    gameLoopId.value = requestAnimationFrame(update)
    return
  }

  const { w, h } = gameBounds.value

  // 1. Check Température & Sprite
  if (temperature.value >= 1.5) {
    if (currentSprite.value !== sadTuxSprite) currentSprite.value = sadTuxSprite
  } else if (temperature.value <= 1.4) {
    if (currentSprite.value !== tuxSprite) currentSprite.value = tuxSprite
  }

  // 2. Déplacement Joueur
  let pdx = 0, pdy = 0
  if (keys.z) pdy -= 1
  if (keys.s) pdy += 1
  if (keys.q) pdx -= 1
  if (keys.d) pdx += 1

  const isMoving = pdx !== 0 || pdy !== 0
  if (!beam.value.active && isMoving) player.value.angle = Math.atan2(pdy, pdx)

  if (isMoving) {
    const speed = 5
    const moveSpeed = (pdx !== 0 && pdy !== 0) ? speed / 1.414 : speed
    const nx = player.value.x + pdx * moveSpeed
    const ny = player.value.y + pdy * moveSpeed

    // Limites de la carte
    if (nx > 0 && nx < w) player.value.x = nx
    if (ny > 0 && ny < h) player.value.y = ny

    if (timestamp - animState.value.lastFrameTime > 120) {
      animState.value.frameIndex = (animState.value.frameIndex + 1) % 5
      animState.value.lastFrameTime = timestamp
    }
  } else {
    animState.value.frameIndex = 0
  }
  updateSpriteDirection()

  // 3. Laser Logic
  if (beam.value.active) {
    if (beam.value.state === 'shooting') {
      beam.value.head += CONFIG.BEAM.SPEED
      if (beam.value.head >= CONFIG.BEAM.MAX_LENGTH) {
        beam.value.head = CONFIG.BEAM.MAX_LENGTH
        beam.value.state = 'finishing'
      }
    } else if (beam.value.state === 'finishing') {
      beam.value.tail += CONFIG.BEAM.SPEED
      if (beam.value.tail >= beam.value.head) {
        beam.value.active = false
        beam.value.state = 'idle'
      }
    }
  }

  // 4. Entités (Pollution / Nature)
  for (let i = entities.value.length - 1; i >= 0; i--) {
    const ent = entities.value[i]
    ent.x += ent.vx
    ent.y += ent.vy

    // Rebond sur les murs
    if (ent.x < 0 || ent.x > w - CONFIG.ENTITY.SIZE) ent.vx *= -1
    if (ent.y < 0 || ent.y > h - CONFIG.ENTITY.SIZE) ent.vy *= -1

    // Collision Laser
    if (beam.value.active && !ent.hit && checkLaserCollision(ent.x + CONFIG.ENTITY.SIZE/2, ent.y + CONFIG.ENTITY.SIZE/2, CONFIG.ENTITY.SIZE/2)) {
      ent.hit = true
      if (ent.type === 'pollution') {
        temperature.value -= 0.1
        score.value += CONFIG.SCORE.POLLUTION
      } else {
        temperature.value += 0.1
        score.value = Math.max(0, score.value - CONFIG.SCORE.NATURE_PENALTY)
      }
      entities.value.splice(i, 1)
    }
  }

  // 5. Bots (Ennemis)
  for (let i = bots.value.length - 1; i >= 0; i--) {
    const bot = bots.value[i]
    const dx = bot.x - player.value.x
    const dy = bot.y - player.value.y
    const dist = Math.hypot(dx, dy)

    // Comportement : Panique ou Errance
    if (dist < CONFIG.BOT.PANIC_DIST) {
      const force = 0.2
      bot.vx += (dx / dist) * force
      bot.vy += (dy / dist) * force
    } else {
      if (timestamp - bot.changeDirTimer > 1000) {
        const randAngle = Math.random() * Math.PI * 2
        bot.vx += Math.cos(randAngle) * 0.5
        bot.vy += Math.sin(randAngle) * 0.5
        bot.changeDirTimer = timestamp
      }
    }

    // Gestion collision murs (Bots)
    const margin = 100
    const wallForce = 0.8
    if (bot.x < margin) bot.vx += wallForce
    if (bot.x > w - margin) bot.vx -= wallForce
    if (bot.y < margin) bot.vy += wallForce
    if (bot.y > h - margin) bot.vy -= wallForce

    bot.vx *= CONFIG.BOT.FRICTION
    bot.vy *= CONFIG.BOT.FRICTION

    const speed = Math.hypot(bot.vx, bot.vy)
    const maxSpeed = (dist < CONFIG.BOT.PANIC_DIST) ? CONFIG.BOT.MAX_SPEED : CONFIG.BOT.WANDER_SPEED

    if (speed > maxSpeed) {
      bot.vx = (bot.vx / speed) * maxSpeed
      bot.vy = (bot.vy / speed) * maxSpeed
    }
    bot.x += bot.vx
    bot.y += bot.vy

    // Tir des bots
    if (timestamp - bot.lastShot > CONFIG.BOT.FIRE_RATE) {
      const aimX = (player.value.x - bot.x)
      const aimY = (player.value.y - bot.y)
      const aimDist = Math.hypot(aimX, aimY)

      enemyProjectiles.value.push({
        id: performance.now() + Math.random(),
        x: bot.x + CONFIG.BOT.SIZE/2,
        y: bot.y + CONFIG.BOT.SIZE/2,
        vx: (aimX / aimDist) * CONFIG.BULLET.SPEED,
        vy: (aimY / aimDist) * CONFIG.BULLET.SPEED
      })
      bot.lastShot = timestamp
    }

    // Bot touché par laser
    if (beam.value.active && checkLaserCollision(bot.x + CONFIG.BOT.SIZE/2, bot.y + CONFIG.BOT.SIZE/2, CONFIG.BOT.SIZE/2)) {
      bots.value.splice(i, 1)
      score.value += CONFIG.SCORE.BOT
    }
  }

  // 6. Projectiles Ennemis
  for (let i = enemyProjectiles.value.length - 1; i >= 0; i--) {
    const proj = enemyProjectiles.value[i]
    proj.x += proj.vx
    proj.y += proj.vy

    // Hors limites
    if (proj.x < -50 || proj.x > w + 50 || proj.y < -50 || proj.y > h + 50) {
      enemyProjectiles.value.splice(i, 1)
      continue
    }

    // Touche le joueur
    if (checkCircleCollision({x: proj.x, y: proj.y, r: CONFIG.BULLET.SIZE/2}, {x: player.value.x, y: player.value.y, r: player.value.radius})) {
      temperature.value += 0.1
      enemyProjectiles.value.splice(i, 1)
    }
  }

  // 7. Conditions Game Over
  temperature.value = Math.round(temperature.value * 100) / 100
  if (temperature.value >= CONFIG.TEMP.MAX) {
    isGameOver.value = true
    const MESSAGES = [
      "Le numérique émet autant de CO2 que l'aviation civile mondiale.",
      "La 4G consomme 23x plus que le Wifi. Utilisez le Wifi !",
      "La fabrication représente 70% de l'impact carbone d'un appareil.",
      "Le streaming vidéo = 60% du flux Internet mondial.",
      "Nettoyez votre boîte mail : 1Mo = 19g de CO2."
    ]
    gameOverMessage.value = MESSAGES[Math.floor(Math.random() * MESSAGES.length)]
  }

  if (temperature.value < CONFIG.TEMP.MIN) temperature.value = CONFIG.TEMP.MIN

  gameLoopId.value = requestAnimationFrame(update)
}

/* --- 7. CYCLE DE VIE --- */
onMounted(async () => {
  await nextTick()
  updateBounds()

  // Centrer le joueur au démarrage
  if (containerRef.value) {
    player.value.x = gameBounds.value.w / 2
    player.value.y = gameBounds.value.h / 2
  }

  gameLoopId.value = requestAnimationFrame(update)

  window.addEventListener('keydown', handleKeyDown)
  window.addEventListener('keyup', handleKeyUp)

  // Préchargement images
  new Image().src = sadTuxSprite
  new Image().src = cookedChickenImg

  // Compte à rebours
  const interval = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(interval)
      isGameStarted.value = true
      spawnerId.value = window.setInterval(spawnEntity, CONFIG.SPAWN_RATE)
      botSpawnerId.value = window.setInterval(spawnBot, CONFIG.BOT.SPAWN_RATE)
    }
  }, 1000)
})

onUnmounted(() => {
  if (gameLoopId.value) cancelAnimationFrame(gameLoopId.value)
  if (spawnerId.value) clearInterval(spawnerId.value)
  if (botSpawnerId.value) clearInterval(botSpawnerId.value)

  window.removeEventListener('keydown', handleKeyDown)
  window.removeEventListener('keyup', handleKeyUp)
})
</script>

<template>
  <div
    class="laser-overlay"
    ref="containerRef"
    :style="{ background: screenBackground }"
    @mousedown="shoot"
    @mousemove="handleMouseMove"
  >

    <div class="hud-score">SCORE: {{ score }}</div>
    <div class="hud-temp" :style="{ color: tempColor }">
      Temp: +{{ temperature.toFixed(1) }}°C
      <div class="temp-bar">
        <div class="temp-fill" :style="{ width: (temperature / CONFIG.TEMP.MAX * 100) + '%', background: tempColor }"></div>
      </div>
    </div>

    <div v-if="isGameOver" class="game-over">
      <h1>🌍 CUI' CUIT 🔥</h1>
      <p class="final-score">Score Final : {{ score }}</p>
      <img :src="cookedChickenImg" alt="Poulet Cuit" class="chicken-img" />
      <p class="game-over-message">{{ gameOverMessage }}</p>
      <button @click="emit('close')" class="quit-btn">Quitter</button>
    </div>

    <div v-else-if="!isGameStarted" class="countdown-overlay">
      <div class="countdown-number">{{ countdown }}</div>
      <div class="countdown-text">Préparez-vous !</div>
    </div>

    <div class="instructions" v-else>ZQSD bouger | CLIC tirer | Évitez les balles rouges !</div>

    <div class="player-wrapper" :style="{ transform: `translate(${player.x}px, ${player.y}px)` }">
      <div
        class="laser-pivot"
        :style="{ transform: `translate(${beam.startX}px, ${beam.startY}px) rotate(${beam.angle}rad)`, zIndex: laserZIndex }"
      >
        <div v-if="beam.active" class="laser-beam" :style="{ left: beam.tail + 'px', width: (beam.head - beam.tail) + 'px' }">
          <div class="laser-core"></div>
          <div class="laser-glow"></div>
        </div>
      </div>
      <div :style="spriteStyle"></div>
    </div>

    <div
      v-for="ent in entities"
      :key="ent.id"
      class="entity"
      :class="ent.type"
      :style="{ transform: `translate(${ent.x}px, ${ent.y}px)`, width: CONFIG.ENTITY.SIZE + 'px', height: CONFIG.ENTITY.SIZE + 'px' }"
    >
      {{ ent.emoji }}
    </div>

    <div v-for="bot in bots" :key="bot.id" class="bot" :style="{ transform: `translate(${bot.x}px, ${bot.y}px)` }"></div>
    <div v-for="proj in enemyProjectiles" :key="proj.id" class="enemy-projectile" :style="{ transform: `translate(${proj.x}px, ${proj.y}px)` }"></div>

  </div>
</template>

<style scoped>
/* CONTENEUR PRINCIPAL */
.laser-overlay {
  position: absolute; /* S'adapte au parent */
  top: 0; left: 0; right: 0; bottom: 0;
  width: 100%; height: 100%;
  z-index: 1000;
  cursor: crosshair;
  user-select: none;
  overflow: hidden;
}

/* HUD */
.hud-temp, .hud-score {
  position: absolute;
  top: 20px;
  font-family: monospace;
  font-size: 2rem;
  font-weight: bold;
  background: rgba(0,0,0,0.5);
  padding: 15px;
  border-radius: 8px;
  z-index: 200;
}
.hud-temp { right: 20px; }
.hud-score {
  left: 20px;
  color: #ffd700;
  text-shadow: 2px 2px 0 #000;
}
.temp-bar { width: 100%; height: 8px; background: #333; margin-top: 5px; border-radius: 4px; overflow: hidden; }
.temp-fill { height: 100%; transition: width 0.3s; }

/* GAME OVER */
.game-over {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(0,0,0,0.95);
  padding: 40px;
  text-align: center;
  border: 4px solid red;
  border-radius: 20px;
  color: white;
  z-index: 300;
  min-width: 400px;
}
.game-over h1 { margin: 0 0 5px 0; font-size: 2.5rem; color: #ff4444; }
.final-score { font-size: 1.5rem; color: #ffd700; font-weight: bold; margin: 0 0 15px 0; }
.game-over-message { font-family: sans-serif; font-size: 1.1rem; color: #ddd; margin: 10px 0 20px 0; font-style: italic; }

/* COUNTDOWN */
.countdown-overlay {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  z-index: 400;
  pointer-events: none;
}
.countdown-number { font-size: 8rem; font-weight: bold; color: #fff; text-shadow: 0 0 20px rgba(0,0,0,0.8); animation: pulse 1s infinite; }
.countdown-text { font-size: 2rem; color: #42b883; text-shadow: 0 0 10px black; margin-top: -20px; }

@keyframes pulse {
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.2); opacity: 0.8; }
  100% { transform: scale(1); opacity: 1; }
}

.chicken-img { width: 150px; height: auto; display: block; margin: 0 auto 10px auto; filter: drop-shadow(0 0 10px rgba(255, 68, 68, 0.8)); animation: shake 0.5s infinite alternate; }
@keyframes shake { from { transform: rotate(-5deg); } to { transform: rotate(5deg); } }

.quit-btn { margin-top: 10px; padding: 10px 30px; font-size: 1.2rem; cursor: pointer; }

/* ENTITIES & PLAYER */
.player-wrapper { position: absolute; top: 0; left: 0; width: 0; height: 0; z-index: 50; pointer-events: none; }
.laser-pivot { position: absolute; top: 0; left: 0; width: 0; height: 0; }
.laser-beam { position: absolute; top: -15px; height: 0; z-index: 10; }
.laser-core { position: absolute; top: -3px; left: 0; width: 100%; height: 6px; background: white; box-shadow: 0 0 5px white; }
.laser-glow { position: absolute; top: -8px; left: 0; width: 100%; height: 16px; box-shadow: 0 0 10px #00ffff; opacity: 0.6; }

.entity { position: absolute; display: flex; justify-content: center; align-items: center; font-size: 45px; transition: transform 0s linear; }
.entity.pollution { filter: drop-shadow(0 0 10px red); }
.entity.tree { filter: drop-shadow(0 0 10px #42b883); }

/* BOTS & PROJECTILES */
.bot { position: absolute; top: 0; left: 0; width: 40px; height: 40px; background: radial-gradient(circle, #ff4444 0%, #990000 100%); border-radius: 50%; box-shadow: 0 0 10px red; border: 2px solid white; }
.enemy-projectile { position: absolute; top: 0; left: 0; width: 12px; height: 12px; background: #ffaa00; border-radius: 50%; box-shadow: 0 0 5px orange, 0 0 10px yellow; }

.instructions { position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); color: #ccc; background: rgba(0,0,0,0.5); padding: 5px 15px; border-radius: 20px; }
</style>
