import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import AdminRoute, { AUTHORIZE as ADMIN_AUTHORIZE } from './admin'
import AuthRoutes from './auth'
import MainRoute, { AUTHORIZE as MAIN_AUTHORIZE } from './main'
import config from '@/common/config'
import { homeRedirect } from './utils'
import { currentUser } from '@/services/auth'
import { CurrentUser as User } from '@/types/auth'

Vue.use(VueRouter)

const routes: RouteConfig[] = [
  {
    path: '/',
    name: 'Home',
    redirect: homeRedirect(),
    meta: { authorize: [] }
  },
  AdminRoute,
  MainRoute,
  ...AuthRoutes,
  { path: '*', redirect: '/'}
];

const router = new VueRouter({
  mode: 'history',
  base: config.BASE_URL,
  routes
});

let user: User | null = null;

currentUser.subscribe(val => user = val);

router.beforeEach((to, from, next) => {
  const { authorize }: { [key: string]: string[]} = to.meta;

  if (authorize) {
    if (!user) {
      return next({ path: '/login' });
    }

    if (authorize.length) {
      if ((authorize.includes(ADMIN_AUTHORIZE) && !user.user.is_admin) || (authorize.includes(MAIN_AUTHORIZE) && !!user.user.is_admin)) {
        return next({ path: from.path });
      }
    }
  }

  next();
});

export default router;
