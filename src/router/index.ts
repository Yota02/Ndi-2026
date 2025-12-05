import { createRouter, createWebHashHistory } from 'vue-router'
import TrailerPage from '../views/TrailerPage.vue'
import HomePage from '../views/HomeView.vue'
import Sobriete from '@/views/SobrieteView.vue'
import LasergameMenuView from '../views/LasergameMenuView.vue'
import LasergameSurvival from '../views/LasergameSurvivalView.vue'
import LasergameQuiz from '../views/LasergameQuizView.vue'
import PortfolioView from '../views/PortfolioView.vue'
import ChapterPage from '../views/ChapterPage.vue'

import ContactView from '@/views/ContactView.vue'
import PhoneGameView from '@/views/PhoneGameView.vue'

const SESSION_KEY = 'trailer_seen'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'trailer',
      component: TrailerPage
    },
    {
      path: '/home',
      name: 'home',
      component: HomePage
    },
    {
      path: '/sobriete-numerique',
      name: 'sobriete-numerique',
      component: Sobriete,
    },
    {
      path: '/laser-game',
      name: 'laser-game',
      component: LasergameMenuView
    },
    {
      path: '/laser-game/survival',
      name: 'survival',
      component: LasergameSurvival
    },
    {
      path: '/laser-game/quiz',
      name: 'quiz',
      component: LasergameQuiz
    },
    { path: '/portfolio',
      name: 'portfolio',
      component: PortfolioView
    },
    { path: '/chapter/:id',
      name: 'chapter',
      component: ChapterPage
    },  {
      path: '/contact',
      name: 'contact',
      component: ContactView
     },
    {
      path: '/phone-game',
      name: 'phone-game',
      component: PhoneGameView
    }
  ]
})

router.beforeEach((to) => {
  // Si on va sur le trailer et qu'il a déjà été vu, rediriger vers /home
  if (to.name === 'trailer') {
    const trailerSeen = sessionStorage.getItem(SESSION_KEY)
    if (trailerSeen) {
      return { name: 'home' }
    }
  }
  // Pas de return = navigation continue normalement
})

export default router
