<script setup lang="ts">
import NavBar from '@/components/NavBar.vue';

import TuxImg from '@/assets/img/tux-normal.png';

const scrollDown = () => {
  window.scrollTo({
    top: window.innerHeight,
    behavior: 'smooth'
  });
};
</script>

<template>
  <div class="home-page">
    <NavBar />

    <header class="hero-section">
      <div class="cyber-grid"></div>
      <div class="overlay-vignette"></div>

      <div class="hero-content">
        <div class="badge-container">
          <span class="badge">Nuit de l'Info 2025</span>
        </div>

        <h1 class="main-title">
          Le Village Numérique
          <span class="highlight">Résistant</span>
        </h1>

        <p class="subtitle">
          Face au Goliath des Big Tech, l'école contre-attaque.<br>
          Rejoignez la démarche <strong>NIRD</strong> : Inclusif, Responsable, Durable.
        </p>

        <div class="cta-group">
          <button class="btn-primary" @click="scrollDown">
            🔎 Décourvir la NIRD
          </button>
        </div>
      </div>

      <div class="scroll-indicator" @click="scrollDown">
        <span>▼</span>
      </div>
    </header>

    <section class="story-interlude">
      <div class="container flex-story">

        <div class="character-box">
          <div class="hologram-effect"></div>
          <img :src="TuxImg" alt="Agent Tux" class="tux-character" />
          <div class="char-name">Agent Tuxy</div>
        </div>

        <div class="dialogue-box">
          <div class="dialogue-header">
            <span class="status-dot blink"></span> Transmission Cryptée v2.025
          </div>
          <p class="typewriter-text">
            "Psst ! Recrue ! Ici l'Agent Tuxy. <br><br>
            La situation est critique. <strong>L'Empire des GAFAM</strong> tente de verrouiller notre école avec des logiciels fermés et obsolètes.
            <br><br>
            Heureusement, un groupe de résistants a mis au point un plan de défense :
            la démarche <strong>N.I.R.D</strong>. <br>
            C'est notre seule chance de garder notre liberté numérique. Voici leur stratégie..."
          </p>
          <div class="dialogue-arrow">▼</div>
        </div>

      </div>
    </section>

    <section id="nird-mission" class="mission-section">
      <div class="container">

        <div class="mission-header">
          <span class="section-tag">// Le Plan de Bataille</span>
          <h2>L'Arme Secrète : <span class="text-nird">N.I.R.D</span></h2>
          <p class="mission-desc">
            Pour transformer votre l'école en village résistant, la démarche NIRD propose une stratégie en 3 axes.
            Une initiative venue d'en bas pour changer les choses en haut.
          </p>
        </div>

        <div class="pillars-grid">

          <div class="card inclusive">
            <div class="icon-box">🤝</div>
            <h3>Inclusif</h3>
            <p>
              Le numérique ne doit laisser personne de côté. NIRD vise à redonner le
              <strong>pouvoir d'agir</strong> aux élèves, aux profs et aux familles,
              pour ne plus dépendre d'experts coûteux.
            </p>
          </div>

          <div class="card responsible">
            <div class="icon-box">🛡️</div>
            <h3>Responsable</h3>
            <p>
              Stop au pillage des données. En privilégiant des outils
              <strong>éthiques et souverains</strong>, le collectif protège la vie privée
              de la communauté éducative hors des GAFAM.
            </p>
          </div>

          <div class="card durable">
            <div class="icon-box">🌱</div>
            <h3>Durable</h3>
            <p>
              Pourquoi jeter des PC qui marchent ? Contre l'obsolescence programmée,
              la démarche encourage l'installation de <strong>Linux</strong> pour faire durer le matériel
              plus longtemps.
            </p>
          </div>

        </div>

        <div class="forge-link">
          <p>Cette démarche est portée par la <a href="https://nird.forge.apps.education.fr/" target="_blank" class="link-highlight">Forge des Communs Numériques</a>.</p>
        </div>

      </div>
    </section>
  </div>
</template>

<style scoped>
.home-page {
  min-height: 100vh;
  background-color: #111827;
  color: white;
}

/* HERO SECTION - PLEIN ÉCRAN */
.hero-section {
  position: relative;
  height: 100vh; /* Prend toute la hauteur */
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  overflow: hidden;
  padding: 0 20px;
}

/* CONTENU DU HERO */
.hero-content {
  z-index: 10;
  max-width: 900px;
  animation: fadeUp 1s ease-out;
}

/* BADGE */
.badge {
  background: rgba(16, 185, 129, 0.1);
  color: #34d399; /* Vert NIRD */
  border: 1px solid #34d399;
  padding: 6px 16px;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  margin-bottom: 24px;
  display: inline-block;
}

/* TITRE PRINCIPAL */
.main-title {
  font-size: 4rem;
  font-weight: 900;
  line-height: 1.1;
  margin-bottom: 1.5rem;
  color: #f8fafc;
}

.highlight {
  background: linear-gradient(135deg, #34d399 0%, #3b82f6 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  display: block; /* Force le retour à la ligne pour l'impact */
}

/* SOUS-TITRE */
.subtitle {
  font-size: 1.25rem;
  color: #94a3b8; /* Gris bleuté */
  margin-bottom: 3rem;
  line-height: 1.6;
}

.subtitle strong {
  color: #e2e8f0;
}

/* BOUTONS */
.cta-group {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-primary {
  background-color: #10b981; /* Vert action */
  color: #022c22;
  font-weight: 700;
  padding: 16px 32px;
  border-radius: 12px;
  border: none;
  font-size: 1.1rem;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 0 20px rgba(16, 185, 129, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 30px rgba(16, 185, 129, 0.5);
}

.btn-secondary {
  background-color: transparent;
  color: #e2e8f0;
  border: 2px solid #334155;
  font-weight: 600;
  padding: 16px 32px;
  border-radius: 12px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  border-color: #94a3b8;
  background-color: rgba(255, 255, 255, 0.05);
}

/* BACKGROUND ANIMÉ (GRILLE CYBERPUNK) */
.cyber-grid {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  background-image:
    linear-gradient(rgba(16, 185, 129, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(16, 185, 129, 0.1) 1px, transparent 1px);
  background-size: 60px 60px;
  transform-origin: top center;
  transform: perspective(500px) rotateX(60deg) translateY(0);
  animation: gridMove 10s linear infinite;
  z-index: 1;
  opacity: 0.4;
}

.overlay-vignette {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  background: radial-gradient(circle at center, transparent 0%, #0f172a 90%);
  z-index: 2; /* Par dessus la grille pour fondre les bords */
}

/* ANIMATIONS */
@keyframes gridMove {
  0% { background-position: 0 0; }
  100% { background-position: 0 60px; } /* Doit correspondre à la taille de la grille */
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* INDICATEUR DE SCROLL */
.scroll-indicator {
  position: absolute;
  bottom: 30px;
  z-index: 10;
  color: #94a3b8;
  font-size: 1.5rem;
  animation: bounce 2s infinite;
  cursor: pointer;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
  60% { transform: translateY(-5px); }
}

/* RESPONSIVE MOBILE */
@media (max-width: 768px) {
  .main-title { font-size: 2.5rem; }
  .cta-group { flex-direction: column; width: 100%; }
  .btn-primary, .btn-secondary { width: 100%; }
}

/* SECTION STORYTELLING */
.story-interlude {
  background-color: #111827;
  padding: 60px 20px;
  display: flex;
  justify-content: center;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.flex-story {
  display: flex;
  align-items: center;
  gap: 40px;
  max-width: 900px;
  width: 100%;
}

/* PERSONNAGE (TUX) */
.character-box {
  position: relative;
  width: 150px;
  flex-shrink: 0;
  text-align: center;
}

.tux-character {
  width: 100%;
  height: auto;
  filter: drop-shadow(0 0 10px rgba(52, 211, 153, 0.5)); /* Lueur verte */
  animation: float 4s ease-in-out infinite;
}

/* Petit effet hologramme (scanline) */
.hologram-effect {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  background: linear-gradient(rgba(16, 185, 129, 0) 50%, rgba(16, 185, 129, 0.1) 50%);
  background-size: 100% 4px;
  pointer-events: none;
  z-index: 2;
  opacity: 0.5;
}

.char-name {
  margin-top: 10px;
  font-weight: bold;
  color: #34d399;
  font-family: 'Courier New', monospace;
  background: rgba(0, 0, 0, 0.5);
  padding: 2px 8px;
  border-radius: 4px;
}

/* BOITE DE DIALOGUE */
.dialogue-box {
  background: rgba(31, 41, 55, 0.8); /* Fond sombre semi-transparent */
  border: 2px solid #374151;
  border-left: 5px solid #34d399; /* Bordure verte à gauche */
  padding: 25px;
  border-radius: 12px;
  position: relative;
  flex-grow: 1;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
}

/* Flèche de la bulle (version Desktop) */
.dialogue-box::before {
  content: '';
  position: absolute;
  left: -12px;
  top: 30px;
  border-top: 10px solid transparent;
  border-bottom: 10px solid transparent;
  border-right: 12px solid #34d399;
}

.dialogue-header {
  font-size: 0.8rem;
  color: #6b7280;
  margin-bottom: 10px;
  text-transform: uppercase;
  letter-spacing: 1px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-dot {
  width: 8px; height: 8px;
  background-color: #ef4444; /* Rouge enregistrement */
  border-radius: 50%;
  display: inline-block;
}

.blink { animation: blinker 1.5s linear infinite; }

.typewriter-text {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #e5e7eb;
}

.dialogue-arrow {
  position: absolute;
  bottom: 10px; right: 20px;
  color: #34d399;
  animation: bounce 1s infinite;
}

/* RESPONSIVE */
@media (max-width: 768px) {
  .flex-story {
    flex-direction: column;
    text-align: center;
  }

  .dialogue-box::before {
    /* Flèche vers le haut sur mobile */
    left: 50%; top: -12px;
    transform: translateX(-50%) rotate(90deg);
  }

  .character-box { width: 100px; }
}



/** NIRD SECTION **/
.mission-section {
  padding: 80px 20px;
  background-color: #111827; /* Un poil plus clair que le hero pour le contraste */
  position: relative;
}

.container {
  max-width: 1100px;
  margin: 0 auto;
}

/* EN-TÊTE DE SECTION */
.mission-header {
  text-align: center;
  margin-bottom: 60px;
}

.section-tag {
  color: #64748b;
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
  display: block;
  margin-bottom: 10px;
}

.mission-header h2 {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 20px;
}

.text-nird {
  background: linear-gradient(90deg, #f472b6, #a78bfa, #34d399); /* Dégradé 3 couleurs */
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.mission-desc {
  max-width: 700px;
  margin: 0 auto;
  color: #9ca3af;
  font-size: 1.1rem;
  line-height: 1.6;
}

/* GRILLE DES CARTES */
.pillars-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

/* CARTE INDIVIDUELLE */
.card {
  background: #1f2937;
  padding: 30px;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: transform 0.3s, border-color 0.3s;
  position: relative;
  overflow: hidden;
}

.card:hover {
  transform: translateY(-10px);
}

.card h3 {
  font-size: 1.5rem;
  margin-bottom: 15px;
  font-weight: 700;
}

.card p {
  color: #d1d5db;
  font-size: 1rem;
  line-height: 1.5;
}

.icon-box {
  font-size: 3rem;
  margin-bottom: 20px;
}

/* COULEURS SPÉCIFIQUES PAR PILIER */
/* Inclusif (Rose/Violet) */
.card.inclusive:hover { border-color: #f472b6; }
.card.inclusive h3 { color: #f472b6; }

/* Responsable (Bleu/Violet) */
.card.responsible:hover { border-color: #a78bfa; }
.card.responsible h3 { color: #a78bfa; }

/* Durable (Vert) */
.card.durable:hover { border-color: #34d399; }
.card.durable h3 { color: #34d399; }

/* LIEN FORGE */
.forge-link {
  text-align: center;
  margin-top: 50px;
  padding-top: 30px;
  border-top: 1px solid #374151;
}

.forge-link p {
  color: #6b7280;
}

.link-highlight {
  color: #34d399;
  text-decoration: none;
  font-weight: bold;
  border-bottom: 1px dashed #34d399;
  transition: color 0.2s;
}

.link-highlight:hover {
  color: #10b981;
  border-bottom-style: solid;
}





</style>
