<script setup lang="ts">
import NavBar from '@/components/NavBar.vue';

import TuxImg from '@/assets/img/tux-normal.png';
import TuxImg2 from '@/assets/img/tux-detective.png';
import NirdLogo from '@/assets/img/logo-nird.png';

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
            <span class="status-dot blink"></span> Alerte Écologique Prioritaire
          </div>
          <p class="typewriter-text">
            "Psst ! Recrue ! Ici l'Agent Tuxy. <br><br>
            L'heure est grave pour la planète. <strong>L'Empire Big Tech</strong> a programmé l'obsolescence de milliers d'ordinateurs dans nos écoles.
            <br><br>
            Ils veulent nous forcer à jeter du matériel qui fonctionne encore très bien, juste pour vendre du neuf. C'est un gâchis immense !
            <br><br>
            Mais la résistance a un plan pour stopper ce gaspillage : la démarche <strong>N.I.R.D</strong>. <br>
            Son but est de faire durer le matériel le plus longtemps possible. Voici leur stratégie..."
          </p>
          <div class="dialogue-arrow">▼</div>
        </div>

      </div>
    </section>

    <section id="nird-mission" class="mission-section">
      <div class="container">

        <div class="mission-branding">
          <div class="logo-wrapper">
            <div class="pulse-ring"></div>
            <img :src="NirdLogo" alt="Logo NIRD" class="nird-logo-main" />
          </div>
          <h2>L'Alternative <span class="text-nird">Écologique</span></h2>
          <p class="subtitle-compact">3 piliers pour stopper le gaspillage numérique.</p>
        </div>

        <div class="pillars-grid compact-grid">

          <div class="card inclusive">
            <div class="card-header-flex">
              <span class="icon-small">🤝</span>
              <h3>Inclusif</h3>
            </div>
            <p>
              <strong>Pas besoin de PC neuf.</strong><br>
              La démarche favorise la sobriété : on utilise le matériel existant pour ne laisser personne de côté.
            </p>
          </div>

          <div class="card responsible">
            <div class="card-header-flex">
              <span class="icon-small">⚖️</span>
              <h3>Responsable</h3>
            </div>
            <p>
              <strong>Refus du jetable.</strong><br>
              Le collectif choisit des logiciels légers qui ne ralentissent pas les ordis, évitant leur remplacement.
            </p>
          </div>

          <div class="card durable">
            <div class="card-header-flex">
              <span class="icon-small">🌱</span>
              <h3>Durable</h3>
            </div>
            <p>
              <strong>Objectif 10 ans.</strong><br>
              Contre l'obsolescence programmée, on installe Linux pour doubler la durée de vie du matériel.
            </p>
          </div>

        </div>

        <div class="action-footer">
          <a href="https://nird.forge.apps.education.fr/" target="_blank" class="btn-forge">
            Voir la Forge NIRD ➔
          </a>
        </div>

      </div>
    </section>

    <section class="eco-impact-section">
      <div class="container">

        <div class="impact-header">
          <span class="alert-badge">⚠️ Données Critiques</span>
          <h2>La Face Cachée de <span class="highlight-impact">votre PC</span></h2>
          <p class="subtitle">
            Pourquoi s'acharner à garder nos vieux ordinateurs ?<br>
            Parce que le coût réel de fabrication est terrifiant.
          </p>
        </div>

        <div class="impact-content">

          <div class="rucksack-visual">
            <div class="laptop-icon">💻</div>
            <div class="weight-line">
              <span class="visible-weight">2 kg (Poids visible)</span>
              <span class="arrow-down">⬇️</span>
            </div>
            <div class="hidden-weight-box">
              <h3>800 kg</h3>
              <p>de matières premières extraites</p>
              <div class="earth-texture"></div>
            </div>
            <p class="caption">
              C'est le <strong>"Sac à dos écologique"</strong>. <br>
              Jeter ce PC, c'est gaspiller tout ça.
            </p>
          </div>

          <div class="stats-grid">

            <div class="stat-item">
              <div class="stat-value">80%</div>
              <div class="stat-label">de la pollution</div>
              <p class="stat-desc">
                L'impact carbone d'un appareil vient de sa <strong>fabrication</strong>, pas de son utilisation électrique.
              </p>
            </div>

            <div class="stat-item">
              <div class="stat-value">240k</div>
              <div class="stat-label">Litres d'eau</div>
              <p class="stat-desc">
                Nécessaires pour fabriquer un seul ordinateur (extraction minière et produits chimiques).
              </p>
            </div>

            <div class="stat-item warning">
              <div class="stat-value">2025</div>
              <div class="stat-label">Le grand gâchis</div>
              <p class="stat-desc">
                La fin de support Windows 10 menace d'envoyer <strong>240 millions</strong> de PC fonctionnels à la casse.
              </p>
            </div>

          </div>

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
  padding: 60px 20px;
  background-color: #111827;
  position: relative;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
}

/* LOGO & BRANDING */
.mission-branding {
  text-align: center;
  margin-bottom: 40px;
}

.logo-wrapper {
  position: relative;
  width: 100px;
  height: 100px;
  margin: 0 auto 20px auto;
  display: flex;
  justify-content: center;
  align-items: center;
}

.nird-logo-main {
  width: 100%;
  height: auto;
  position: relative;
  z-index: 2;
  filter: drop-shadow(0 0 15px rgba(52, 211, 153, 0.3));
}

/* Animation de pulsation derrière le logo */
.pulse-ring {
  position: absolute;
  width: 100%; height: 100%;
  border-radius: 50%;
  border: 2px solid #34d399;
  animation: pulse-ring 2s cubic-bezier(0.215, 0.61, 0.355, 1) infinite;
  z-index: 1;
}

@keyframes pulse-ring {
  0% { transform: scale(0.8); opacity: 0.8; }
  100% { transform: scale(1.5); opacity: 0; }
}

.mission-branding h2 {
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 5px;
}

.subtitle-compact {
  color: #9ca3af;
  font-size: 1.1rem;
}

.text-nird {
  color: #34d399; /* Vert NIRD simple et efficace */
}

/* GRILLE COMPACTE */
.pillars-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

/* CARTE ALLÉGÉE */
.card {
  background: #1f2937;
  padding: 20px; /* Moins de padding */
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: transform 0.2s, border-color 0.2s;
}

.card:hover {
  transform: translateY(-5px);
  border-color: #34d399;
  background: #252f3f;
}

.card-header-flex {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.icon-small {
  font-size: 1.5rem;
}

.card h3 {
  font-size: 1.2rem; /* Titre plus petit */
  margin: 0;
  color: white;
}

.card p {
  color: #d1d5db;
  font-size: 0.95rem; /* Texte plus petit */
  line-height: 1.5;
  margin: 0;
}

.card strong {
  color: #34d399;
  display: block;
  margin-bottom: 4px;
}

/* BOUTON FORGE (Discret) */
.action-footer {
  text-align: center;
  margin-top: 40px;
}

.btn-forge {
  display: inline-block;
  color: #9ca3af;
  border: 1px solid #4b5563;
  padding: 10px 20px;
  border-radius: 50px;
  text-decoration: none;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.btn-forge:hover {
  border-color: #34d399;
  color: #34d399;
  background: rgba(16, 185, 129, 0.05);
}

/* SECTION ECO IMPACT */
.eco-impact-section {
  padding: 80px 20px;
  background-color: #111827;
  color: white;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.impact-header {
  text-align: center;
  margin-bottom: 60px;
}

.alert-badge {
  background: rgba(239, 68, 68, 0.2);
  color: #fca5a5;
  border: 1px solid #f87171;
  padding: 5px 12px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
  text-transform: uppercase;
  margin-bottom: 15px;
  display: inline-block;
  animation: pulse-red 2s infinite;
}

.highlight-impact {
  color: #f87171; /* Rouge pâle */
  text-decoration: underline;
  text-decoration-color: rgba(248, 113, 113, 0.5);
}

.subtitle {
  color: #9ca3af;
  font-size: 1.1rem;
}

/* CONTENU PRINCIPAL (FLEX) */
.impact-content {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 60px;
  max-width: 1100px;
  margin: 0 auto;
}

/* VISUEL SAC A DOS (GAUCHE) */
.rucksack-visual {
  flex: 1;
  min-width: 300px;
  text-align: center;
  background: #1f2937;
  padding: 30px;
  border-radius: 20px;
  border: 1px dashed #4b5563;
}

.laptop-icon { font-size: 4rem; margin-bottom: 10px; }

.visible-weight {
  background: #374151;
  padding: 5px 15px;
  border-radius: 50px;
  font-size: 0.9rem;
  color: #e5e7eb;
}

.hidden-weight-box {
  background: linear-gradient(135deg, #4b5563 0%, #1f2937 100%);
  margin-top: 10px;
  padding: 20px;
  border-radius: 12px;
  color: white;
  border: 2px solid #6b7280;
  position: relative;
  overflow: hidden;
}

/* Texture "Terre" abstraite */
.earth-texture {
  position: absolute;
  bottom: -20px; right: -20px;
  width: 100px; height: 100px;
  background: repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(0,0,0,0.1) 10px, rgba(0,0,0,0.1) 20px);
  opacity: 0.5;
}

.hidden-weight-box h3 { font-size: 2.5rem; margin: 0; color: #fca5a5; font-weight: 900; }
.caption { margin-top: 20px; font-size: 0.9rem; color: #9ca3af; }

/* GRILLE STATS (DROITE) */
.stats-grid {
  flex: 1;
  min-width: 300px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.stat-item {
  background: rgba(255, 255, 255, 0.03);
  padding: 20px;
  border-left: 4px solid #34d399; /* Vert par défaut */
  border-radius: 0 10px 10px 0;
  transition: transform 0.2s;
}

.stat-item:hover { transform: translateX(10px); background: rgba(255, 255, 255, 0.06); }

.stat-item.warning { border-left-color: #ef4444; /* Rouge pour le danger Windows 10 */ }

.stat-value { font-size: 2rem; font-weight: 800; color: white; line-height: 1; }
.stat-label { font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; color: #6b7280; margin-bottom: 5px; font-weight: bold; }
.stat-desc { color: #d1d5db; font-size: 0.95rem; margin: 0; }

@keyframes pulse-red {
  0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
  70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
  100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
}

@media (max-width: 768px) {
  .impact-content { flex-direction: column; gap: 30px; }
  .stat-item:hover { transform: translateX(0) translateY(-5px); }
}



</style>
