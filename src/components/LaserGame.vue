<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

// Référence vers l'élément <canvas> du DOM
const gameCanvas = ref<HTMLCanvasElement | null>(null)

// --- Configuration du Jeu ---
const playerSize = 20
const playerSpeed = 5
const laserSpeed = 10

// --- État du Jeu ---
// Position du joueur (x, y)
const player = ref({ x: 300, y: 300 })

// Tableau qui contiendra tous les lasers actifs
// Chaque laser aura : x, y, vx (vitesse X), vy (vitesse Y)
const lasers = ref<{ x: number; y: number; vx: number; vy: number }[]>([])

// Touches enfoncées (pour gérer le déplacement fluide)
const keys = {
  z: false,
  q: false,
  s: false,
  d: false
}

// --- Gestion des Entrées (Clavier) ---
const handleKeyDown = (e: KeyboardEvent) => {
  const key = e.key.toLowerCase()
  if (key in keys) keys[key as keyof typeof keys] = true
}

const handleKeyUp = (e: KeyboardEvent) => {
  const key = e.key.toLowerCase()
  if (key in keys) keys[key as keyof typeof keys] = false
}

// --- Gestion du Tir (Souris) ---
const shoot = (e: MouseEvent) => {
  if (!gameCanvas.value) return

  // 1. Calculer l'angle entre le joueur et la souris
  // On utilise Math.atan2(y, x) pour obtenir l'angle en radians
  const rect = gameCanvas.value.getBoundingClientRect()
  const mouseX = e.clientX - rect.left
  const mouseY = e.clientY - rect.top

  const angle = Math.atan2(mouseY - player.value.y, mouseX - player.value.x)

  // 2. Créer le vecteur de vitesse basé sur l'angle
  // cos pour l'axe X, sin pour l'axe Y
  const velocityX = Math.cos(angle) * laserSpeed
  const velocityY = Math.sin(angle) * laserSpeed

  // 3. Ajouter le laser au tableau
  lasers.value.push({
    x: player.value.x,
    y: player.value.y,
    vx: velocityX,
    vy: velocityY
  })
}

// --- Boucle de Jeu (Game Loop) ---
const update = () => {
  if (keys.z) player.value.y -= playerSpeed
  if (keys.s) player.value.y += playerSpeed
  if (keys.q) player.value.x -= playerSpeed
  if (keys.d) player.value.x += playerSpeed

  for (let i = lasers.value.length - 1; i >= 0; i--) {
    const laser = lasers.value[i]

    if (!laser) continue

    laser.x += laser.vx
    laser.y += laser.vy

    // Suppression si dehors de l'écran
    if (
      laser.x < 0 ||
      laser.x > (gameCanvas.value?.width || 0) ||
      laser.y < 0 ||
      laser.y > (gameCanvas.value?.height || 0)
    ) {
      lasers.value.splice(i, 1)
    }
  }
}

const draw = (ctx: CanvasRenderingContext2D) => {
  // 1. Effacer tout l'écran (pour redessiner la frame suivante)
  ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height)

  // 2. Dessiner le Joueur (Carré vert)
  ctx.fillStyle = '#42b883' // Vue Green
  ctx.fillRect(
    player.value.x - playerSize / 2,
    player.value.y - playerSize / 2,
    playerSize,
    playerSize
  )

  ctx.strokeStyle = '#ff4444' // Couleur du laser
  ctx.lineWidth = 4
  ctx.beginPath()
  for (const laser of lasers.value) {
    ctx.moveTo(laser.x, laser.y)
    ctx.lineTo(laser.x - laser.vx * 2, laser.y - laser.vy * 2)
  }
  ctx.stroke()
}

// La fonction qui tourne en boucle 60 fois par seconde
const loop = () => {
  const ctx = gameCanvas.value?.getContext('2d')
  if (ctx) {
    update() // Mettre à jour les maths
    draw(ctx) // Dessiner le résultat
  }
  requestAnimationFrame(loop)
}

// --- Cycle de vie Vue ---
onMounted(() => {
  if (gameCanvas.value) {
    // Mettre le canvas en plein écran
    gameCanvas.value.width = window.innerWidth
    gameCanvas.value.height = window.innerHeight

    // Démarrer la boucle
    requestAnimationFrame(loop)
  }

  window.addEventListener('keydown', handleKeyDown)
  window.addEventListener('keyup', handleKeyUp)
  window.addEventListener('click', shoot)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown)
  window.removeEventListener('keyup', handleKeyUp)
  window.removeEventListener('click', shoot)
})
</script>

<template>
  <canvas ref="gameCanvas"></canvas>
</template>

<style scoped>
canvas {
  display: block;
  cursor: crosshair; /* Curseur en forme de cible */
}
</style>
