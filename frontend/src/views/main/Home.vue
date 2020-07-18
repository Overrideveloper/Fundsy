<template>
    <div class="page page-main">
      <SideBar :routes="routes" />
      <router-view />
    </div>
</template>

<script lang="ts">
  import { Component, Vue } from 'vue-property-decorator';
  import SideBar from '@/components/SideBar.vue';
  import { SidebarRoute } from '../../types'; 

  @Component({
    components: { SideBar }
  })
  export default class Main extends Vue {
    routes: SidebarRoute[] = [
      { to: '/main/my-investments', name: 'My Investments', icon: 'briefcase' },
      { to: '/main/my-transactions', name: 'My Transactions', icon: 'box-plot' },
      { to: '/main/invest', name: 'Invest', icon: 'view-cards' }
    ];
  }
</script>

<style lang="scss" scoped>
  .page-main {
    background-color: var(--primary-dark);
    display: flex;
    overflow: auto !important;
  }
</style>