import { RouteConfig } from 'vue-router';

export const AUTHORIZE = 'CUSTOMER';

const customerRoutes: RouteConfig[] = [
    {
        path: '/myinvestments',
        name: 'MyInvestments',
        component: () => import('../views/main/Home.vue'),
        meta: { authorize: [AUTHORIZE] }
    }
]

export default customerRoutes;