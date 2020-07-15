import { RouteConfig } from 'vue-router';

export const AUTHORIZE = 'MAIN';

const mainRoute: RouteConfig = {
    path: '/main',
    component: () => import('../views/main/Home.vue'),
    meta: { authorize: [AUTHORIZE] },
    children: [
      { path: '/', redirect: '/main/my-investments' },
      {
        path: 'my-investments',
        component: () => import('../views/main/CustomerInvestments.vue'),
        meta: { authorize: [AUTHORIZE] }
      },
      {
        path: 'invest',
        component: () => import('../views/main/Invest.vue'),
        meta: { authorize: [AUTHORIZE] }
      },
    ]
}

export default mainRoute;