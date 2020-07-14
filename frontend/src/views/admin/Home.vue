<template>
    <div class="page page-admin">
        <SideBar :routes="routes" />
        <router-view />
    </div>
</template>

<script lang="ts">
    import SideBar from '@/components/SideBar.vue';
    import { SidebarRoute } from '../../types'; 

    const routes: SidebarRoute[] = [
        { to: '/admin/investments', name: 'Investments' },
        { to: '/admin/customers', name: 'Customers' },
    ]

    export default {
        name: 'AdminHome',
        components: {
            SideBar
        },
        data() {
            return {
                routes
            }
        }
    }
</script>

<style lang="scss" scoped>
    .page-admin {
        background-color: var(--primary-dark);
        display: flex;
        overflow: auto !important;
    }

    .page-admin__main {
        width: 100%;
    }
</style>