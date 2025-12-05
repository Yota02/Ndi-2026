import { createRouter, createWebHistory } from 'vue-router'
import TrailerPage from '../views/TrailerPage.vue'
import HomePage from '../views/HomeView.vue'

const SESSION_KEY = 'trailer_seen'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
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
