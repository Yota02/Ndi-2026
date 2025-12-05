<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'

const emit = defineEmits(['close'])

// --- Configuration ---
const START_TEMP = 1.20
const MAX_TEMP = 2.00
const SPAWN_RATE = 800 // Une nouvelle entité toutes les 0.8 secondes

// --- État du Jeu ---
const temperature = ref(START_TEMP)
const isGameOver = ref(false)
const gameLoopId = ref<number | null>(null)
const spawnerId = ref<number | null>(null)

// --- Joueur & Objets ---
const player = ref({ x: window.innerWidth / 2, y: window.innerHeight / 2, angle: 0 })
const lasers = ref<{ id: number; x: number; y: number; vx: number; vy: number; angle: number }[]>([])

// Types : 'tree' (Vert, Gentil) ou 'pollution' (Rouge, Méchant)
interface GameEntity {
  id: number;
  x: number;
  y: number;
  type: 'tree' | 'pollution';
  width: number;
}
const entities = ref<GameEntity[]>([])

// --- Clavier ---
const keys = { z: false, q: false, s: false, d: false }

// --- 1. SYSTÈME DE SPAWN (APPARITION) ---
const spawnEntity = () => {
  if (isGameOver.value) return

  // 60% de chance d'avoir de la pollution (rouge), 40% d'arbre (vert)
  const isPollution = Math.random() > 0.4
  const size = 40

  // Position aléatoire mais pas trop près des bords
  const x = Math.random() * (window.innerWidth - 100) + 50
  const y = Math.random() * (window.innerHeight - 100) + 50

  entities.value.push({
    id: Date.now() + Math.random(),
    x,
    y,
    type: isPollution ? 'pollution' : 'tree',
    width: size
  })
}

// --- 2. GESTION DU TIR & MOUVEMENT ---
const handleKeyDown = (e: KeyboardEvent) => {
  const k = e.key.toLowerCase()
  if (k in keys) keys[k as keyof typeof keys] = true
  if (e.key === 'Escape') emit('close')
}
const handleKeyUp = (e: KeyboardEvent) => {
  const k = e.key.toLowerCase()
  if (k in keys) keys[k as keyof typeof keys] = false
}

const updatePlayerRotation = (e: MouseEvent) => {
  if (isGameOver.value) return
  const dx = e.clientX - player.value.x
  const dy = e.clientY - player.value.y
  // Zone morte pour éviter l'effet toupie
  if (Math.sqrt(dx*dx + dy*dy) > 20) {
    player.value.angle = Math.atan2(dy, dx)
  }
}

const shoot = (e: MouseEvent) => {
  if (isGameOver.value) return
  const angle = Math.atan2(e.clientY - player.value.y, e.clientX - player.value.x)
  lasers.value.push({
    id: Date.now(),
    x: player.value.x,
    y: player.value.y,
    vx: Math.cos(angle) * 15, // Vitesse laser
    vy: Math.sin(angle) * 15,
    angle: angle
  })
}

// --- 3. BOUCLE DE JEU & COLLISIONS ---
const update = () => {
  if (isGameOver.value) return

  // Déplacement Joueur
  if (keys.z && player.value.y > 0) player.value.y -= 5
  if (keys.s && player.value.y < window.innerHeight) player.value.y += 5
  if (keys.q && player.value.x > 0) player.value.x -= 5
  if (keys.d && player.value.x < window.innerWidth) player.value.x += 5

  // Mise à jour Lasers
  for (let l = lasers.value.length - 1; l >= 0; l--) {
    const laser = lasers.value[l]
    laser.x += laser.vx
    laser.y += laser.vy

    let hasHit = false

    // Collision avec les entités
    for (let i = entities.value.length - 1; i >= 0; i--) {
      const ent = entities.value[i]

      // Distance simple (cercle vs cercle approximatif pour fluidité)
      // On compense le centre (ent.x + width/2)
      const dist = Math.hypot(laser.x - (ent.x + 20), laser.y - (ent.y + 20))

      if (dist < 30) { // Collision !
        hasHit = true

        // --- LOGIQUE DE TEMPÉRATURE ---
        if (ent.type === 'pollution') {
          // Bravo : on baisse la température
          temperature.value -= 0.01
        } else {
          // Aïe : on a tué un arbre
          temperature.value += 0.01
        }

        // Supprimer l'entité
        entities.value.splice(i, 1)

        // Vérification GAME OVER
        // On utilise toFixed pour éviter les bugs de virgule flottante (ex: 2.0000001)
        if (temperature.value >= MAX_TEMP) {
          temperature.value = MAX_TEMP
          isGameOver.value = true
        }
        // Limite basse (on ne peut pas descendre sous 0 ou la température de départ selon ton choix)
        if (temperature.value < START_TEMP) temperature.value = START_TEMP

        break
      }
    }

    // Supprimer laser hors écran ou après impact
    if (hasHit || laser.x < -50 || laser.x > window.innerWidth + 50 || laser.y < -50 || laser.y > window.innerHeight + 50) {
      lasers.value.splice(l, 1)
    }
  }

  gameLoopId.value = requestAnimationFrame(update)
}

// --- Cycle de vie ---
onMounted(() => {
  // Lancer la boucle de rendu
  gameLoopId.value = requestAnimationFrame(update)

  // Lancer le générateur d'entités
  spawnerId.value = window.setInterval(spawnEntity, SPAWN_RATE)

  window.addEventListener('keydown', handleKeyDown)
  window.addEventListener('keyup', handleKeyUp)
  document.body.style.overflow = 'hidden'
})

onUnmounted(() => {
  if (gameLoopId.value) cancelAnimationFrame(gameLoopId.value)
  if (spawnerId.value) clearInterval(spawnerId.value)

  window.removeEventListener('keydown', handleKeyDown)
  window.removeEventListener('keyup', handleKeyUp)
  document.body.style.overflow = 'auto'
})

// Couleur dynamique de la température (Vert -> Rouge)
const tempColor = computed(() => {
  // Si on est proche de 2.0, c'est rouge, sinon vert/blanc
  const ratio = (temperature.value - START_TEMP) / (MAX_TEMP - START_TEMP)
  if (ratio > 0.8) return '#ff0000' // Rouge critique
  if (ratio > 0.5) return '#ffaa00' // Orange attention
  return '#ffffff' // Blanc tout va bien
})
</script>

<template>
  <div class="laser-overlay" @mousemove="updatePlayerRotation" @mousedown="shoot">

    <div class="hud-temp" :style="{ color: tempColor }">
      Temp: +{{ temperature.toFixed(2) }}°C
      <div class="temp-bar">
        <div
          class="temp-fill"
          :style="{ width: ((temperature - 1) * 100) + '%', background: tempColor }"
        ></div>
      </div>
    </div>

    <div v-if="isGameOver" class="game-over">
      <h1>🌍 PLANÈTE BRÛLÉE 🔥</h1>
      <p>Vous avez atteint +2.0°C</p>
      <button @click="emit('close')" class="quit-btn">Quitter</button>
    </div>

    <div class="instructions" v-else>
      Tirez sur les ROUGES (Pollution) | Évitez les VERTS (Arbres)
    </div>

    <div
      class="player-wrapper"
      :style="{ transform: `translate(${player.x}px, ${player.y}px)` }"
    >
      <div class="player-rotator" :style="{ transform: `rotate(${player.angle}rad)` }">
        <div class="tank-body"></div>
        <div class="tank-turret"></div>
        <div class="tank-barrel"></div>
      </div>
    </div>

    <div
      v-for="ent in entities"
      :key="ent.id"
      class="entity"
      :class="ent.type"
      :style="{ transform: `translate(${ent.x}px, ${ent.y}px)` }"
    >
      <span v-if="ent.type === 'pollution'">🛢️</span>
      <span v-else>🌳</span>
    </div>

    <div
      v-for="laser in lasers"
      :key="laser.id"
      class="laser"
      :style="{ transform: `translate(${laser.x}px, ${laser.y}px) rotate(${laser.angle}rad)` }"
    ></div>

  </div>
</template>

<style scoped>
.laser-overlay {
  position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
  z-index: 9999; cursor: crosshair; background: rgba(0, 0, 0, 0.8); /* Fond plus sombre pour l'ambiance */
  user-select: none;
}

/* --- HUD Température --- */
.hud-temp {
  position: absolute;
  top: 20px;
  right: 20px;
  font-family: 'Courier New', monospace;
  font-size: 2rem;
  font-weight: bold;
  text-shadow: 0 0 10px rgba(0,0,0,0.8);
  z-index: 200;
  background: rgba(0,0,0,0.5);
  padding: 15px;
  border-radius: 8px;
  text-align: right;
}

.temp-bar {
  width: 100%;
  height: 5px;
  background: #333;
  margin-top: 5px;
  border-radius: 2px;
}
.temp-fill {
  height: 100%;
  transition: width 0.2s, background 0.2s;
}

/* --- Game Over --- */
.game-over {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(0,0,0,0.9);
  padding: 40px;
  text-align: center;
  color: white;
  border: 4px solid red;
  border-radius: 20px;
  z-index: 300;
}
.game-over h1 { margin: 0 0 20px; color: #ff4444; font-size: 3rem; }
.quit-btn {
  margin-top: 20px; padding: 10px 30px; font-size: 1.2rem;
  background: white; border: none; cursor: pointer;
}

/* --- Entités --- */
.entity {
  position: absolute;
  top: 0; left: 0;
  width: 40px; height: 40px;
  display: flex; justify-content: center; align-items: center;
  font-size: 30px;
  will-change: transform;
}

/* Animation d'apparition */
.entity { animation: popIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); }

@keyframes popIn {
  from { transform: scale(0); }
  to { transform: scale(1); }
}

.entity.pollution {
  /* On pourrait ajouter un filtre rouge si besoin */
  filter: drop-shadow(0 0 5px red);
}
.entity.tree {
  filter: drop-shadow(0 0 5px #42b883);
}

/* --- Joueur (Tank) - Copié du code précédent --- */
.player-wrapper { position: absolute; top: 0; left: 0; width: 0; height: 0; pointer-events: none; will-change: transform; z-index: 50; }
.player-rotator { position: absolute; top: 0; left: 0; width: 0; height: 0; display: flex; align-items: center; justify-content: center; }
.tank-body { position: absolute; width: 40px; height: 34px; background-color: #2c3e50; border-radius: 4px; box-shadow: 0 0 10px rgba(0,0,0,0.5); border: 2px solid #42b883; transform: translate(-50%, -50%); }
.tank-turret { position: absolute; width: 20px; height: 20px; background-color: #42b883; border-radius: 50%; transform: translate(-50%, -50%); z-index: 2; }
.tank-barrel { position: absolute; left: 0; top: -4px; width: 35px; height: 8px; background-color: #333; z-index: 1; border-radius: 0 4px 4px 0; }
.laser { position: absolute; top: 0; left: 0; margin-top: -2px; width: 20px; height: 4px; background: #ff4444; box-shadow: 0 0 8px #ff4444; pointer-events: none; border-radius: 2px; }

.instructions { position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); color: #ccc; font-family: sans-serif; background: rgba(0,0,0,0.5); padding: 5px 15px; border-radius: 20px; pointer-events: none; }
</style>
