import { RouteConfig } from 'vue-router';

export const AUTHORIZE = 'ADMIN';

const adminRoute: RouteConfig = {
    path: '/admin',
    component: () => import('../views/admin/Home.vue'),
    meta: { authorize: [AUTHORIZE] },
    children: [
      { path: '/', redirect: '/admin/investments' },
      {
        path: 'investments',
        component: () => import('../views/admin/Investments.vue'),
        meta: { authorize: [AUTHORIZE] }
      }
    ]
}

export default adminRoute;