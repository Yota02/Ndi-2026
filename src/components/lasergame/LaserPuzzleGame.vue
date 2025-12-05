<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'

const emit = defineEmits(['close', 'win'])


// CONFIGURATION
const WIDTH = 800
const HEIGHT = 750
const FINAL_LEVEL_INDEX = 9;

// TYPES
type EntityType = 'source' | 'target' | 'mirror' | 'wall'

interface Entity {
  id: number
  type: EntityType
  x: number // Centre X
  y: number // Centre Y
  angle: number // En degrés
  width: number
  height: number
}

interface Point { x: number; y: number }

//  DONNÉES DES NIVEAUX
const levels = [
  // NIVEAU 1 : "Hello World" - Comprendre le rebond simple
  [
    { id: 1, type: 'source', x: 100, y: 300, angle: 0, width: 60, height: 60 },
    { id: 2, type: 'target', x: 700, y: 300, angle: 0, width: 60, height: 60 },
    // CORRECTION : Miroir à 90° (vertical) au début pour bloquer le laser.
    // Le joueur doit cliquer pour le mettre à plat.
    { id: 3, type: 'mirror', x: 400, y: 300, angle: 90, width: 60, height: 10 },
    { id: 4, type: 'wall',   x: 400, y: 100, angle: 90, width: 200, height: 20 },
    { id: 5, type: 'wall',   x: 400, y: 500, angle: 90, width: 200, height: 20 },
  ],

  // NIVEAU 2 : "Le U" - Contournement basique
  [
    { id: 1, type: 'source', x: 100, y: 100, angle: 90, width: 60, height: 60 },
    { id: 2, type: 'target', x: 700, y: 100, angle: 0, width: 60, height: 60 },
    { id: 3, type: 'wall',   x: 400, y: 200, angle: 0, width: 400, height: 20 },

    // Miroirs mal orientés au départ
    { id: 4, type: 'mirror', x: 100, y: 500, angle: 45, width: 60, height: 10 },
    { id: 5, type: 'mirror', x: 700, y: 500, angle: 0, width: 60, height: 10 },
  ],

  // NIVEAU 3 : "Le Zig-Zag"
  [
    // Source décalée pour éviter le mur
    { id: 1, type: 'source', x: 100, y: 500, angle: -60, width: 60, height: 60 },
    { id: 2, type: 'target', x: 700, y: 100, angle: 0, width: 60, height: 60 },

    // Murs espacés pour laisser passer le rayon de 45°
    // Le rayon part de (100, 500) -> doit passer entre les murs
    { id: 10, type: 'wall', x: 300, y: 400, angle: 90, width: 300, height: 20 },
    { id: 11, type: 'wall', x: 500, y: 200, angle: 90, width: 300, height: 20 },

    // Miroirs positionnés sur la trajectoire théorique
    { id: 3, type: 'mirror', x: 300, y: 150, angle: 0, width: 60, height: 10 }, // Premier rebond
    { id: 4, type: 'mirror', x: 500, y: 500, angle: 90, width: 60, height: 10 }, // Deuxième rebond
    { id: 5, type: 'mirror', x: 750, y: 70, angle: 45, width: 60, height: 10 }, // Vers la cible
  ],

  // NIVEAU 4 : "Le Bunker" - Tirer dans un espace clos
  [
    // Source à gauche, tire tout droit vers la droite (Angle 0°)
    { id: 1, type: 'source', x: 100, y: 350, angle: 0, width: 60, height: 60 },
    // Cible enfermée
    { id: 2, type: 'target', x: 500, y: 350, angle: 0, width: 60, height: 60 },

    // Le grand mur vertical qui bloque le tir direct
    { id: 10, type: 'wall', x: 300, y: 350, angle: 90, width: 300, height: 20 },

    // Le "U" qui enferme la maison
    { id: 11, type: 'wall', x: 450, y: 350, angle: 90, width: 100, height: 20 }, // Mur gauche du U
    { id: 12, type: 'wall', x: 550, y: 350, angle: 90, width: 100, height: 20 }, // Mur droit du U
    { id: 13, type: 'wall', x: 500, y: 400, angle: 0, width: 120, height: 20 },  // Mur bas du U


    { id: 3, type: 'mirror', x: 280, y: 350, angle: 90, width: 60, height: 10 },
    { id: 4, type: 'mirror', x: 500, y: 100, angle: 0, width: 60, height: 10 },
    { id: 5, type: 'mirror', x: 280, y: 520, angle: 90, width: 60, height: 10 },
    { id: 6, type: 'mirror', x: 160, y: 520, angle: 0, width: 60, height: 10 },
    { id: 7, type: 'mirror', x: 160, y: 120, angle: 0, width: 60, height: 10 },
    { id: 8, type: 'mirror', x: 580, y: 520, angle: 90, width: 60, height: 10 },
    { id: 9, type: 'mirror', x: 580, y: 150, angle: 45, width: 60, height: 10 },
  ],

  // NIVEAU 5 : "La Fibre Croisée" - Le rebond en X
  [
    { id: 1, type: 'source', x: 190, y: 190, angle: 45, width: 60, height: 60 }, // Tire diagonale bas-droite
    { id: 2, type: 'target', x: 100, y: 500, angle: 0, width: 60, height: 60 }, // Cible en bas à gauche

    { id: 3, type: 'mirror', x: 700, y: 300, angle: 90, width: 60, height: 10 }, // Miroir fond
    { id: 4, type: 'mirror', x: 400, y: 150, angle: 0, width: 60, height: 10 },
    { id: 5, type: 'mirror', x: 500, y: 500, angle: 0, width: 60, height: 10 },
    { id: 6, type: 'mirror', x: 150, y: 150, angle: 25, width: 60, height: 10 },
    { id: 7, type: 'mirror', x: 550, y: 150, angle: 25, width: 60, height: 10 }, // Miroir fond
    { id: 8, type: 'mirror', x: 380, y: 50, angle: 0, width: 60, height: 10 },// Miroir fond
    { id: 9, type: 'mirror', x: 30, y: 100, angle: 0, width: 60, height: 10 },

    { id: 10, type: 'wall', x: 400, y: 300, angle: 90, width: 150, height: 20 }, // Obstacle central
  ],

  // NIVEAU 6 : "Précision Chirurgicale" - Le trou de souris
  [
    { id: 1, type: 'source', x: 50, y: 300, angle: 0, width: 60, height: 60 },
    { id: 2, type: 'target', x: 750, y: 300, angle: 0, width: 60, height: 60 },

    // Un grand mur avec un tout petit trou au milieu (y=300)
    { id: 10, type: 'wall', x: 400, y: 100, angle: 90, width: 380, height: 20 }, // Mur haut
    { id: 11, type: 'wall', x: 400, y: 500, angle: 90, width: 380, height: 20 }, // Mur bas

    // Le joueur doit aligner les miroirs pour passer pile dans le trou
    // Obstacle devant la source
    { id: 12, type: 'wall', x: 200, y: 300, angle: 90, width: 200, height: 20 },

    { id: 3, type: 'mirror', x: 150, y: 500, angle: 0, width: 60, height: 10 },
    { id: 4, type: 'mirror', x: 600, y: 500, angle: 0, width: 60, height: 10 },
    { id: 5, type: 'mirror', x: 600, y: 300, angle: 45, width: 60, height: 10 },
    { id: 6, type: 'mirror', x: 250, y: 280, angle: 45, width: 60, height: 10 },
    { id: 6, type: 'mirror', x: 150, y: 300, angle: 45, width: 60, height: 10 },
    { id: 7, type: 'mirror', x: 360, y: 500, angle: 0, width: 60, height: 10 },
    { id: 8, type: 'mirror', x: 360, y: 400, angle: 90, width: 60, height: 10 },
    { id: 9, type: 'mirror', x: 230, y: 400, angle: 90, width: 60, height: 10 },
    { id: 10, type: 'mirror', x: 450, y: 500, angle: 0, width: 60, height: 10 },
    { id: 11, type: 'mirror', x: 450, y: 200, angle: 0, width: 60, height: 10 },
    { id: 12, type: 'mirror', x: 750, y: 200, angle: 0, width: 60, height: 10 },
  ],

  // NIVEAU 7 : "Les Leurres" - Beaucoup de miroirs inutiles
  [
    { id: 1, type: 'source', x: 400, y: 50, angle: 90, width: 60, height: 60 }, // Tire vers le bas
    { id: 2, type: 'target', x: 400, y: 480, angle: 0, width: 60, height: 60 },

    // Obstacle central direct
    { id: 10, type: 'wall', x: 400, y: 300, angle: 0, width: 100, height: 20 },

    // Cercle de miroirs (6 miroirs autour)
    { id: 3, type: 'mirror', x: 300, y: 200, angle: 135, width: 60, height: 10 },
    { id: 4, type: 'mirror', x: 600, y: 200, angle: 135, width: 60, height: 10 },
    { id: 5, type: 'mirror', x: 220, y: 400, angle: -45, width: 60, height: 10 },
    { id: 6, type: 'mirror', x: 600, y: 400, angle: 45, width: 60, height: 10 },
    { id: 7, type: 'mirror', x: 400, y: 100, angle: 45, width: 60, height: 10 },
    { id: 8, type: 'mirror', x: 600, y: 100, angle: 75, width: 60, height: 10 },
    { id: 9, type: 'mirror', x: 400, y: 0, angle: 0, width: 60, height: 10 },
    { id: 10, type: 'mirror', x: 400, y: 310, angle: 30, width: 60, height: 10 },

    // Miroirs inutiles (pièges)
    { id: 11, type: 'mirror', x: 100, y: 300, angle: 90, width: 60, height: 10 },
    { id: 12, type: 'mirror', x: 700, y: 300, angle: 90, width: 60, height: 10 },
  ],

  // NIVEAU 8 : "Le Carré Magique" - Rebond infini ?
  [
    { id: 1, type: 'source', x: 50, y: 50, angle: 10, width: 60, height: 60 },
    { id: 2, type: 'target', x: 50, y: 150, angle: 0, width: 60, height: 60 }, // Juste à côté de la source !

    // Mur qui sépare source et cible
    { id: 10, type: 'wall', x: 100, y: 100, angle: 0, width: 200, height: 20 },

    // Il faut faire tout le tour de l'écran
    { id: 3, type: 'mirror', x: 750, y: 180, angle: 90, width: 60, height: 10 },   // Coin haut droit
    { id: 4, type: 'mirror', x: 750, y: 10, angle: 0, width: 60, height: 10 },   // Coin bas droit
    { id: 5, type: 'mirror', x: 620, y: 50, angle: 30, width: 60, height: 10 },
    { id: 6, type: 'mirror', x: 680, y: 300, angle: 45, width: 60, height: 10 },
    { id: 7, type: 'mirror', x: 280, y: 200, angle: 45, width: 60, height: 10 },
    { id: 8, type: 'mirror', x: 750, y: 350, angle: 90, width: 60, height: 10 },
    { id: 9, type: 'mirror', x: 380, y: 500, angle: 70, width: 60, height: 10 },
    { id: 10, type: 'mirror', x: 250, y: 120, angle: 70, width: 60, height: 10 },
    { id: 11, type: 'mirror', x: 180, y: 380, angle: 0, width: 60, height: 10 },
  ],

  // NIVEAU 9 : "Ping Pong"
  [
    { id: 1, type: 'source', x: 100, y: 300, angle: -45, width: 60, height: 60 },
    { id: 2, type: 'target', x: 700, y: 300, angle: 0, width: 60, height: 60 },

    // Couloir haut et bas
    { id: 10, type: 'wall', x: 400, y: 50, angle: 0, width: 800, height: 20 },
    { id: 11, type: 'wall', x: 400, y: 550, angle: 0, width: 800, height: 20 },

    // 4 Murs verticaux au milieu pour forcer le zigzag
    { id: 12, type: 'wall', x: 250, y: 200, angle: 90, width: 200, height: 20 },
    { id: 13, type: 'wall', x: 400, y: 400, angle: 90, width: 200, height: 20 },
    { id: 14, type: 'wall', x: 550, y: 200, angle: 90, width: 200, height: 20 },

    // Miroirs à placer
    { id: 3, type: 'mirror', x: 350, y: 450, angle: 0, width: 60, height: 10 },
    { id: 4, type: 'mirror', x: 400, y: 70, angle: 90, width: 60, height: 10 },
    { id: 5, type: 'mirror', x: 550, y: 500, angle: 0, width: 60, height: 10 },
    { id: 6, type: 'mirror', x: 190, y: 200, angle: 0, width: 60, height: 10 },
    { id: 7, type: 'mirror', x: 100, y: 120, angle: 63, width: 60, height: 10 },
    { id: 8, type: 'mirror', x: 750, y: 100, angle: 153, width: 60, height: 10 },
    { id: 9, type: 'mirror', x: 30, y: 400, angle: 30, width: 60, height: 10 },
    { id: 10, type: 'mirror', x: 270, y: 200, angle: 90, width: 60, height: 10 },
    { id: 11, type: 'mirror', x: 500, y: 250, angle: 45, width: 60, height: 10 },
  ],

// NIVEAU 10 : "La Matrice de Confusion"
  [

    { id: 1, type: 'source', x: 100, y: 100, angle: 45, width: 60, height: 60 },
    { id: 2, type: 'target', x: 700, y: 550, angle: 0, width: 60, height: 60 },


    { id: 10, type: 'wall', x: 400, y: 300, angle: 0, width: 600, height: 20 },
    { id: 11, type: 'wall', x: 600, y: 450, angle: 90, width: 250, height: 20 },



    { id: 3, type: 'mirror', x: 250, y: 250, angle: 17, width: 60, height: 10 },
    { id: 4, type: 'mirror', x: 450, y: 100, angle: 33, width: 60, height: 10 },
    { id: 5, type: 'mirror', x: 650, y: 200, angle: 52, width: 60, height: 10 },
    { id: 6, type: 'mirror', x: 450, y: 450, angle: 78, width: 60, height: 10 },
    { id: 7, type: 'mirror', x: 700, y: 400, angle: 113, width: 60, height: 10 },


    { id: 75, type: 'mirror', x: 350, y: 175, angle: 145, width: 60, height: 10 },
    { id: 76, type: 'mirror', x: 550, y: 150, angle: 178, width: 60, height: 10 },


    { id: 20, type: 'mirror', x: 700, y: 200, angle: 201, width: 60, height: 10 },
    { id: 21, type: 'mirror', x: 150, y: 400, angle: 233, width: 60, height: 10 },
    { id: 22, type: 'mirror', x: 500, y: 50, angle: 269, width: 60, height: 10 },
    { id: 23, type: 'mirror', x: 500, y: 500, angle: 292, width: 60, height: 10 },
    { id: 24, type: 'mirror', x: 200, y: 200, angle: 311, width: 60, height: 10 },
    { id: 25, type: 'mirror', x: 300, y: 150, angle: 338, width: 60, height: 10 },
    { id: 26, type: 'mirror', x: 650, y: 30, angle: 17, width: 60, height: 10 },
    { id: 27, type: 'mirror', x: 400, y: 400, angle: 33, width: 60, height: 10 },
    { id: 28, type: 'mirror', x: 100, y: 550, angle: 52, width: 60, height: 10 },
    { id: 29, type: 'mirror', x: 350, y: 350, angle: 78, width: 60, height: 10 },
    { id: 30, type: 'mirror', x: 550, y: 250, angle: 113, width: 60, height: 10 },
    { id: 31, type: 'mirror', x: 50, y: 300, angle: 145, width: 60, height: 10 },
    { id: 32, type: 'mirror', x: 750, y: 480, angle: 178, width: 60, height: 10 },
    { id: 33, type: 'mirror', x: 500, y: 300, angle: 201, width: 60, height: 10 },
    { id: 34, type: 'mirror', x: 250, y: 50, angle: 233, width: 60, height: 10 },

    { id: 35, type: 'mirror', x: 50, y: 50, angle: 269, width: 60, height: 10 },
    { id: 36, type: 'mirror', x: 50, y: 550, angle: 292, width: 60, height: 10 },
    { id: 37, type: 'mirror', x: 750, y: 50, angle: 311, width: 60, height: 10 },
    { id: 38, type: 'mirror', x: 350, y: 200, angle: 338, width: 60, height: 10 },
    { id: 39, type: 'mirror', x: 200, y: 450, angle: 17, width: 60, height: 10 },
    { id: 40, type: 'mirror', x: 550, y: 350, angle: 33, width: 60, height: 10 },
    { id: 41, type: 'mirror', x: 700, y: 300, angle: 52, width: 60, height: 10 },
    { id: 42, type: 'mirror', x: 400, y: 550, angle: 78, width: 60, height: 10 },
    { id: 43, type: 'mirror', x: 150, y: 250, angle: 113, width: 60, height: 10 },
    { id: 44, type: 'mirror', x: 500, y: 200, angle: 145, width: 60, height: 10 },
    { id: 60, type: 'mirror', x: 50, y: 200, angle: 178, width: 60, height: 10 },
    { id: 61, type: 'mirror', x: 150, y: 50, angle: 201, width: 60, height: 10 },
    { id: 62, type: 'mirror', x: 250, y: 550, angle: 233, width: 60, height: 10 },
    { id: 63, type: 'mirror', x: 450, y: 570, angle: 269, width: 60, height: 10 },
    { id: 64, type: 'mirror', x: 650, y: 570, angle: 292, width: 60, height: 10 },
    { id: 65, type: 'mirror', x: 700, y: 250, angle: 311, width: 60, height: 10 },
    { id: 66, type: 'mirror', x: 500, y: 400, angle: 338, width: 60, height: 10 },
    { id: 67, type: 'mirror', x: 300, y: 250, angle: 17, width: 60, height: 10 },
    { id: 68, type: 'mirror', x: 100, y: 300, angle: 33, width: 60, height: 10 },
    { id: 69, type: 'mirror', x: 400, y: 450, angle: 52, width: 60, height: 10 },
    { id: 70, type: 'mirror', x: 750, y: 350, angle: 78, width: 60, height: 10 },
    { id: 71, type: 'mirror', x: 200, y: 100, angle: 113, width: 60, height: 10 },
    { id: 72, type: 'mirror', x: 350, y: 500, angle: 145, width: 60, height: 10 },
    { id: 73, type: 'mirror', x: 550, y: 550, angle: 178, width: 60, height: 10 },
    { id: 74, type: 'mirror', x: 600, y: 300, angle: 201, width: 60, height: 10 },

    // --- NOUVEAUX LEURRES (Vague 5 : Bourrage extrême) ---
    { id: 80, type: 'mirror', x: 10, y: 400, angle: 233, width: 60, height: 10 },
    { id: 81, type: 'mirror', x: 790, y: 400, angle: 269, width: 60, height: 10 },
    { id: 82, type: 'mirror', x: 400, y: 10, angle: 292, width: 60, height: 10 },
    { id: 83, type: 'mirror', x: 400, y: 590, angle: 311, width: 60, height: 10 },
    { id: 84, type: 'mirror', x: 100, y: 450, angle: 338, width: 60, height: 10 },
    { id: 85, type: 'mirror', x: 700, y: 150, angle: 17, width: 60, height: 10 },
    { id: 86, type: 'mirror', x: 200, y: 500, angle: 33, width: 60, height: 10 },
    { id: 87, type: 'mirror', x: 600, y: 500, angle: 52, width: 60, height: 10 },
    { id: 88, type: 'mirror', x: 350, y: 400, angle: 78, width: 60, height: 10 },
    { id: 89, type: 'mirror', x: 450, y: 200, angle: 113, width: 60, height: 10 },
    { id: 90, type: 'mirror', x: 550, y: 300, angle: 145, width: 60, height: 10 },
    { id: 91, type: 'mirror', x: 250, y: 400, angle: 178, width: 60, height: 10 },
    { id: 92, type: 'mirror', x: 300, y: 550, angle: 201, width: 60, height: 10 },
    { id: 93, type: 'mirror', x: 500, y: 150, angle: 233, width: 60, height: 10 },
    { id: 94, type: 'mirror', x: 750, y: 590, angle: 269, width: 60, height: 10 },
  ]
] as Entity[][]


// CHRONOMÈTRE & ÉTAT
const startTime = ref(0)
const totalTime = ref(0)
const timerInterval = ref<number | null>(null)
const finalTimeDisplay = ref('')

const currentLevelIndex = ref(0)
const entities = ref<Entity[]>([])
const laserPath = ref<Point[]>([])
const isLevelComplete = ref(false)
const isGameRunning = ref(false)
const isGameFinished = ref(false); // <--- AJOUTÉ
const canvasRef = ref<HTMLCanvasElement | null>(null)


// LOGIQUE CHRONOMÈTRE

const startTimer = () => {
  if (timerInterval.value) clearInterval(timerInterval.value);
  startTime.value = performance.now() - totalTime.value;
  isGameRunning.value = true;

  timerInterval.value = window.setInterval(() => {
    totalTime.value = performance.now() - startTime.value;
  }, 50);
}

const stopTimer = () => {
  if (timerInterval.value !== null) {
    clearInterval(timerInterval.value);
    timerInterval.value = null;
    isGameRunning.value = false;
  }
}

const formatTime = (ms: number): string => {
  const totalSeconds = Math.floor(ms / 1000);
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  const centiseconds = Math.floor((ms % 1000) / 10);
  return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}:${centiseconds.toString().padStart(2, '0')}`;
}

const formattedTime = computed(() => formatTime(totalTime.value))

// LOGIQUE MATHÉMATIQUE

const rad = (deg: number) => deg * (Math.PI / 180)

const getIntersection = (p1: Point, p2: Point, p3: Point, p4: Point): Point | null => {
  const x1 = p1.x, y1 = p1.y, x2 = p2.x, y2 = p2.y
  const x3 = p3.x, y3 = p3.y, x4 = p4.x, y4 = p4.y

  const denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
  if (denom === 0) return null

  const ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denom
  const ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denom

  if (ua >= 0 && ua <= 1 && ub >= 0 && ub <= 1) {
    return { x: x1 + ua * (x2 - x1), y: y1 + ua * (y2 - y1) }
  }
  return null
}

const computeLaser = () => {
  if (isLevelComplete.value) return

  const source = entities.value.find(e => e.type === 'source')
  if (!source) return

  const path: Point[] = []
  let x = source.x
  let y = source.y
  let angle = source.angle

  path.push({ x, y })

  for (let i = 0; i < 50; i++) {
    const maxDist = 2000
    const endX = x + Math.cos(rad(angle)) * maxDist
    const endY = y + Math.sin(rad(angle)) * maxDist

    let closestPoint: Point | null = null
    let minDistance = Infinity
    let hitObject: Entity | null = null

    for (const ent of entities.value) {
      if (ent.type === 'source') continue

      const hw = ent.width / 2
      let effectiveAngle = ent.angle
      if (ent.type === 'target') {
        effectiveAngle = angle + 90
      }

      const p3 = {
        x: ent.x + Math.cos(rad(effectiveAngle)) * -hw,
        y: ent.y + Math.sin(rad(effectiveAngle)) * -hw
      }
      const p4 = {
        x: ent.x + Math.cos(rad(effectiveAngle)) * hw,
        y: ent.y + Math.sin(rad(effectiveAngle)) * hw
      }

      const hit = getIntersection({x, y}, {x: endX, y: endY}, p3, p4)

      if (hit) {
        const dist = Math.hypot(hit.x - x, hit.y - y)
        if (dist < minDistance && dist > 1) {
          minDistance = dist
          closestPoint = hit
          hitObject = ent
        }
      }
    }

    if (closestPoint && hitObject) {
      path.push(closestPoint)
      x = closestPoint.x
      y = closestPoint.y

      if (hitObject.type === 'target') {
        isLevelComplete.value = true
        stopTimer();


        if (currentLevelIndex.value === levels.length - 1) {
          finalTimeDisplay.value = formatTime(totalTime.value);
          isGameFinished.value = true; // Passe à l'état final
        }
        break
      } else if (hitObject.type === 'wall') {
        break
      } else if (hitObject.type === 'mirror') {
        angle = 2 * hitObject.angle - angle
      }
    } else {
      path.push({ x: endX, y: endY })
      break
    }
  }

  laserPath.value = path
  drawLaser()
}

const drawLaser = () => {
  const ctx = canvasRef.value?.getContext('2d')
  if (!ctx || !canvasRef.value) return

  ctx.clearRect(0, 0, canvasRef.value.width, canvasRef.value.height)

  if (laserPath.value.length < 2) return

  ctx.lineCap = 'round'
  ctx.lineJoin = 'round'
  ctx.lineWidth = 6
  ctx.strokeStyle = 'rgba(66, 184, 131, 0.5)'
  ctx.beginPath()
  ctx.moveTo(laserPath.value[0].x, laserPath.value[0].y)
  for (let i = 1; i < laserPath.value.length; i++) {
    ctx.lineTo(laserPath.value[i].x, laserPath.value[i].y)
  }
  ctx.stroke()

  ctx.lineWidth = 2
  ctx.strokeStyle = '#fff'
  ctx.stroke()
}

// INTERACTIONS
const rotateObject = (ent: Entity) => {
  if (isLevelComplete.value || !isGameRunning.value || ent.type !== 'mirror') return;

  if(isLevelComplete.value) {
    isLevelComplete.value = false;
  }

  ent.angle = (ent.angle + 45) % 360
  computeLaser()
}

const loadLevel = (index: number) => {
  // FIN DU JEU
  if (index >= levels.length) {

    emit('win');
    return;
  }

  if (index === 0) {
    totalTime.value = 0;
    isGameFinished.value = false; // Réinitialisation de l'état final
  }

  entities.value = JSON.parse(JSON.stringify(levels[index]))
  currentLevelIndex.value = index
  isLevelComplete.value = false

  startTimer();

  setTimeout(computeLaser, 50)
}

const nextLevel = () => {
  stopTimer();

  // SI l'état est FINI (dernière victoire), le bouton renvoie au menu.
  if (isGameFinished.value) {
    emit('win');
    return;
  }

  // SINON, on charge le niveau suivant
  loadLevel(currentLevelIndex.value + 1)
}

// LIFECYCLE
onMounted(() => {
  // Initialisation à 0 pour le jeu complet
  loadLevel(0)
})

</script>

<template>
  <div class="puzzle-container">

    <div class="timer-display">{{ formattedTime }}</div>

    <div class="header-ui">
      <h2>Niveau {{ currentLevelIndex + 1 }} / {{ levels.length }}</h2>
      <p>Cliquez sur les miroirs pour orienter la Fibre Optique ! 📡</p>
    </div>

    <div class="game-board" :style="{ width: WIDTH + 'px', height: HEIGHT + 'px' }">

      <canvas ref="canvasRef" :width="WIDTH" :height="HEIGHT" class="laser-layer"></canvas>

      <div
        v-for="ent in entities"
        :key="ent.id"
        class="game-entity"
        :class="ent.type"
        :style="{
          left: ent.x + 'px',
          top: ent.y + 'px',
          width: ent.width + 'px',
          height: ent.height + 'px',
          transform: `translate(-50%, -50%) rotate(${ent.angle}deg)`
        }"
        @click="rotateObject(ent)"
      >
        <div v-if="ent.type === 'source'" class="icon">🐧</div>
        <div v-if="ent.type === 'target'" class="icon">🏠</div>
        <div v-if="ent.type === 'mirror'" class="mirror-shape"></div>
        <div v-if="ent.type === 'wall'" class="wall-shape"></div>
      </div>

    </div>

    <div v-if="isLevelComplete" class="level-complete-overlay">

      <div class="final-score-display">

        <h3 v-if="!isGameFinished">CONNEXION ÉTABLIE ! 📶</h3>
        <h3 v-else>✨ FIBRE OPTIQUE MAÎTRISÉE ! ✨</h3>

        <p v-if="isGameFinished">
          Temps total : <strong>{{ finalTimeDisplay }}</strong>
        </p>

        <button
          @click="nextLevel"
          class="next-btn"
        >
          {{ isGameFinished ? 'Retour Menu' : 'Niveau Suivant ➡' }}
        </button>
      </div>

    </div>

    <button class="quit-btn" @click="emit('close')">Quitter</button>

  </div>
</template>

<style scoped>
/* GENERAL */
.puzzle-container {
  position: absolute; top: 0; left: 0; width: 100%; height: auto;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  background-color: #1e1e24; color: white; user-select: none;
}

/* HUD */
.timer-display {
  position: absolute;
  top: 20px;
  left: 20px;
  font-size: 1.8rem;
  font-family: monospace;
  padding: 10px 15px;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 8px;
  color: #ffd700;
  z-index: 50;
}

.header-ui { text-align: center; margin-bottom: 20px; }
.header-ui h2 { color: #42b883; margin: 0; }
.header-ui p { color: #aaa; margin: 5px 0 0 0; }

/* ZONE DE JEU */
.game-board {
  position: relative;
  background: #252530;
  border: 4px solid #333;
  box-shadow: 0 0 20px rgba(0,0,0,0.5);
  background-image: radial-gradient(#333 1px, transparent 1px);
  background-size: 50px 50px;
}
.laser-layer { position: absolute; top: 0; left: 0; pointer-events: none; z-index: 10; }

/* ENTITÉS */
.game-entity { position: absolute; display: flex; justify-content: center; align-items: center; z-index: 20; transition: transform 0.2s; }
.game-entity.mirror { cursor: pointer; }
.game-entity.mirror:hover .mirror-shape { background: #64ffda; box-shadow: 0 0 10px #64ffda; }
.icon { font-size: 2rem; }
.mirror-shape { width: 100%; height: 100%; background: #00bcd4; border-radius: 4px; box-shadow: 0 0 5px #00bcd4; }
.wall-shape { width: 100%; height: 100%; background: #555; border: 1px solid #777; border-radius: 2px; }

/* VICTOIRE & SCORE FINAL */
.level-complete-overlay {
  position: absolute; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex; justify-content: center; align-items: center;
  flex-direction: column;
  z-index: 100;
}
.level-complete-overlay h3 { margin: 0 0 15px 0; font-size: 2rem; color: #42b883; }
.final-score-display {
  text-align: center;
  padding: 30px;
  border: 3px solid #64ffda;
  border-radius: 10px;
  background: #0d1217;
}
.final-score-display p { font-size: 1.5rem; margin: 15px 0; }
.final-score-display strong { color: #ffd700; font-size: 1.8rem; }

.next-btn { background: #42b883; color: white; border: none; padding: 10px 20px; font-size: 1.2rem; border-radius: 5px; cursor: pointer; margin-top: 15px; }
.next-btn:hover { background: #3aa876; }

.quit-btn { position: absolute; top: 20px; right: 20px; background: transparent; border: 1px solid #666; color: #aaa; padding: 5px 10px; cursor: pointer; z-index: 50; }
.quit-btn:hover { border-color: white; color: white; }
</style>
