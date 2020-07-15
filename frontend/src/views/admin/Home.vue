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
        { to: '/admin/investments', name: 'Investments', icon: 'briefcase' },
        { to: '/admin/customers', name: 'Customers', icon: 'users', icon_solid: true },
    ]

    export default {
        name: 'Admin',
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
</style>