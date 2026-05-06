import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import MovieView from '../views/MovieView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    {
      path: '/:mediaType(movie|tv)/:id',
      name: 'movie',
      component: MovieView,
      props: true,
    },
  ],
  scrollBehavior(to, from, saved) {
    if (saved) return saved
    if (to.name === 'movie') return null
    return { top: 0 }
  },
})

export default router
