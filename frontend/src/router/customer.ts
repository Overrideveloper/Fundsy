import { RouteConfig } from 'vue-router';

export const AUTHORIZE = 'CUSTOMER';

const customerRoute: RouteConfig = {
    path: '/main',
    component: () => import('../views/main/Home.vue'),
    meta: { authorize: [AUTHORIZE] },
    children: [
      { path: '/', redirect: '/main/investments' },
      {
        path: 'investments',
        component: () => import('../views/main/MyInvestments.vue'),
        meta: { authorize: [AUTHORIZE] }
      },
      {
        path: 'invest',
        component: () => import('../views/main/Invest.vue'),
        meta: { authorize: [AUTHORIZE] }
      },
    ]
}

export default customerRoute;