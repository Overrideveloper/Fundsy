<template>
  <div class="page page-myinvestments">
    <NavBar :user="user" :title="title" />
    <Loader v-if="isPageLoading" />

    <div class="page__main" v-else>
      <Empty v-if="isEmpty" :text="emptyText" :actionLink="emptyLink" :actionText="emptyLinkText" :hasAction="true" />

      <template v-else>
          <p class="page__intro">You currently have {{total}} investment{{ total === 1 ? '' : 's'}}</p>

          <div class="page__customerinvestments">
            <router-link to="/main/invest" class="new__investment__link">
              <button class="new__investment">
                <svg class="new__investment__icon" width="50" height="50"  viewBox="0 0 36 36" preserveAspectRatio="xMidYMid meet">
                  <path d="M26.17,17H19V9.83a1,1,0,0,0-2,0V17H9.83a1,1,0,0,0,0,2H17v7.17a1,1,0,0,0,2,0V19h7.17a1,1,0,0,0,0-2Z" class="clr-i-outline clr-i-outline-path-1"></path>
                  <path d="M18,2A16,16,0,1,0,34,18,16,16,0,0,0,18,2Zm0,30A14,14,0,1,1,32,18,14,14,0,0,1,18,32Z" class="clr-i-outline clr-i-outline-path-2"></path>
                  <rect x="0" y="0" width="36" height="36" fill-opacity="0"/>
                </svg>
                <span class="new__investment__text">New Investment</span>
              </button>
            </router-link>

            <CustomerInvestment v-for="customerInvestment of customerInvestments" :key="customerInvestment.id" :customerInvestment="customerInvestment" />
          </div>
          
          <button @click.prevent="loadCustomerInvestments(page, per_page, true)" v-if="showLoadMore" class="load__more__btn button" :class="{ 'is-loading': isMoreLoading }">Load More</button>
      </template>
    </div>
  </div>
</template>

<script lang="ts">
  import { Component, Vue } from 'vue-property-decorator';
  import NavBar from '@/components/NavBar.vue';
  import SideBar from '@/components/SideBar.vue';
  import Loader from '@/components/Loader.vue';
  import Empty from '@/components/Empty.vue';
  import CustomerInvestment from '@/components/CustomerInvestment.vue';
  import { CurrentUser } from '../../types/auth';
  import { currentUser } from '../../services/auth';
  import { customerInvestmentCache, getCustomerInvestments, customerInvestmentTotal } from '../../services/customer_investment';
  import { PaginationQuery, PaginatedData } from '../../types';
  import { CustomerInvestmentRes } from '../../types/customer_investment';
  import { NOTIFICATIONS } from '../../services/notification';

  @Component({
    components: { NavBar, SideBar, Empty, Loader, CustomerInvestment },
    notifications: { ...NOTIFICATIONS }
  })
  export default class CustomerInvestments extends Vue {
    title: string = 'My Investments';
    emptyText: string = 'You have no investments yet.';
    emptyLink: string = '/main/invest';
    emptyLinkText: string ='Make your first investment';
    customerInvestments: CustomerInvestmentRes[] = null;
    isPageLoading: boolean = true;
    isMoreLoading: boolean = false;
    page: number = 1;
    per_page: number = 10;
    total: number = 0;

    get user() {
      const user = <CurrentUser> currentUser.getValue();
      return { id: user.id, name: user.name, username: user.user.username };
    }

    get isEmpty() {
      return this.customerInvestments && !this.customerInvestments.length;
    }

    get showLoadMore() {
      return this.customerInvestments && this.customerInvestments.length !== this.total;
    }

    created() {
      this.customerInvestments = customerInvestmentCache.getValue();

      if (this.customerInvestments) {
        this.page = Math.floor(this.customerInvestments.length/this.per_page) + 1;
        this.isPageLoading = false;
      }

      customerInvestmentCache.subscribe(val => this.customerInvestments = val);
      customerInvestmentTotal.subscribe(val => this.total = val);
      this.loadCustomerInvestments(this.page, this.per_page)
    }

    loadCustomerInvestments(page: number, per_page: number, isMore?: boolean) {
      const query: PaginationQuery = { page, per_page };

      if (isMore) {
        this.isMoreLoading = true;
      }

      getCustomerInvestments<PaginatedData<CustomerInvestmentRes>>(this.user.id, query).then((data: PaginatedData<CustomerInvestmentRes>) => {
        this.isPageLoading = false;
        this.isMoreLoading = false;

        if (data.data.length === per_page) {
          this.page += 1;
        }
      }).catch(err => {
        this.isMoreLoading = false;
        (<any> this).error({ message: err });
      });
    }
  }
</script>

<style lang="scss" scoped>
  .page-myinvestments {
    overflow-y: auto;
  }

  .page__main {
    padding: 2rem;
  }

  .page__intro {
    color: var(--dim-white);
    font-size: 20px;
  }

  .page__customerinvestments {
    margin-top: 2rem;
    display: flex;
    flex-wrap: wrap;
  }

  .new__investment__link {
    height: auto;
    display: flex;
  }

  .new__investment {
    height: auto;
    width: 240px;
    border: 1px solid var(--tertiary);
    border-radius: 8px;
    align-items: center;
    justify-content: center;
    background-color: transparent;
    margin-right: 40px;
    margin: 0 16px 32px 16px;
    display: flex;
    flex-direction: column;
    cursor: pointer;
    transition: all 500ms ease;
    padding: 1rem 0;

    .new__investment__text {
      font-size: 16px;
      color: var(--tertiary);
    }

    .new__investment__icon {
      fill: var(--tertiary);
      margin-bottom: 1rem;
    }

    &:hover {
      box-shadow: 0 0.5em 1em -0.125em rgba(0, 209, 178, 0.1), 0 0px 0 1px rgba(0, 209, 178, 0.1);
      background-color: var(--tertiary);

      .new__investment__text {
        color: var(--dim-white);
      }

      .new__investment__icon {
        fill: var(--dim-white);
      }
    }
  }

  @media screen and (max-width: 768px) {
    .new__investment__link, .new__investment {
      width: 100%
    }
  }
</style>