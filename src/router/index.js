
import {
  createRouter,
  createWebHistory
} from 'vue-router';
import HomeView from '../views/HomeView.vue';
import AdminView from '../views/AdminView.vue';
import MovieView from '../views/MovieView.vue';
import store from '../store/index';
const router = createRouter({
  createWebHistory,
  // jshint ignore:start
  
  history: createWebHistory(
    import.meta.env.BASE_URL),
  // jshint ignore:end
  routes: [{
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/admin',
    name: 'admin',
    component: AdminView
  },
  {
    path: "/movie/:id",
    name: "movie",
    component: MovieView,
    beforeEnter: async (to, from, next) => {
      const routeId = to.params.id;
      await store.dispatch("setMovie", routeId);
      next();
    }
  },

  ]
});

export default router;