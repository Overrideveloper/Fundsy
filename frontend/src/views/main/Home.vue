<template>
    <div class="page page-main">
      <SideBar :routes="routes" />
      <router-view />
    </div>
</template>

<script lang="ts">
    import SideBar from '@/components/SideBar.vue';
    import { SidebarRoute } from '../../types'; 

    const routes: SidebarRoute[] = [
      { to: '/main/investments', name: 'My Investments', icon: 'briefcase' },
      { to: '/main/transactions', name: 'My Transactions', icon: 'box-plot' },
      { to: '/main/invest', name: 'Invest', icon: 'view-cards' }
    ]

    export default {
      name: 'Main',
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
  .page-main {
    background-color: var(--primary-dark);
    display: flex;
    overflow: auto !important;
  }
</style>