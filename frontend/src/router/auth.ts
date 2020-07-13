import { RouteConfig } from 'vue-router';

const authRoutes: RouteConfig[] = [
    {
      path: '/login',
      name: 'Login',
      component: () => import('../views/auth/Login.vue')
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('../views/auth/Register.vue')
    },
];

export default authRoutes;