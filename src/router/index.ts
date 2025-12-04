import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import FrustratingForm from '@/components/FrustratingForm.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      // L'URL dans la barre d'adresse
      path: '/windows-nightmare',

      // Le nom technique de la route
      name: 'frustrating-form',

      // Le composant à charger
      component: FrustratingForm,

      // Optionnel : Changer le titre de l'onglet
      meta: { title: 'Mise à jour critique...' }
    },
  ],
})

export default router
