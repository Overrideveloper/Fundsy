<template>
    <div class="page page-admin">
        <SideBar :routes="routes" />
        <router-view />
    </div>
</template>

<script lang="ts">
    import { Component, Vue } from 'vue-property-decorator';
    import SideBar from '@/components/SideBar.vue';
    import { SidebarRoute } from '../../types'; 

    @Component({
        name: 'Admin',
        components: { SideBar }
    })
    export default class Home extends Vue {
        routes: SidebarRoute[] = [
            { to: '/admin/investments', name: 'Investments', icon: 'briefcase' },
            { to: '/admin/customers', name: 'Customers', icon: 'users', icon_solid: true },
        ];
    }
</script>

<style lang="scss" scoped>
    .page-admin {
        background-color: var(--primary-dark);
        display: flex;
        overflow: auto !important;
    }
</style>