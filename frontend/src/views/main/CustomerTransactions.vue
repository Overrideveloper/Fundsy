<template>
  <div class="page page-mytransactions">
    <NavBar :user="user" :title="title" />
    <Loader v-if="isPageLoading" />

    <div class="page__main" v-else>
        <Empty v-if="isEmpty" :text="emptyText" />

        <template v-else>
            <p class="page__intro">You have made {{total}} transaction{{ total === 1 ? '' : 's'}}</p>

            <div class="transactions">
                <CustomerTransaction v-for="transaction of transactions" :key="transaction.id" :transaction="transaction" />
            </div>

            <button @click.prevent="loadTransactions(page, per_page, true)" v-if="showLoadMore" class="load__more__btn button" :class="{ 'is-loading': isMoreLoading }">Load More</button>
        </template>
    </div>
  </div>
</template>

<script lang="ts">
    import { Component, Vue } from 'vue-property-decorator';
    import NavBar from '../../components/NavBar.vue';
    import Loader from '../../components/Loader.vue';
    import Empty from '../../components/Empty.vue';
    import CustomerTransaction from '../../components/CustomerTransaction.vue';
    import { CurrentUser } from '../../types/auth';
    import { currentUser } from '../../services/auth';
    import { NOTIFICATIONS } from '../../services/notification';
    import { getCustomerTransactions } from '../../services/transaction';
    import { PaginationQuery, PaginatedData } from '../../types';
    import { Transaction } from '../../types/transaction';

    @Component({
        components: { NavBar, Loader, Empty, CustomerTransaction },
        notifications: { ...NOTIFICATIONS }
    })
    export default class CustomerTransactions extends Vue {
        title: string = 'My Transactions';
        isPageLoading: boolean = true;
        isMoreLoading: boolean = false;
        emptyText: string = 'You have not made any transactions yet';
        transactions: Transaction[] = null;
        page: number = 1;
        per_page: number = 4;
        total: number = 0;

        get user() {
            const user = <CurrentUser> currentUser.getValue();
            return { id: user.id, name: user.name, username: user.user.username };
        }

        get isEmpty() {
            return this.transactions && !this.transactions.length;
        }

        get showLoadMore() {
            return this.transactions && this.transactions.length !== this.total;
        }

        created() {
            if (this.transactions) {
                this.isPageLoading = false;
            }
            this.loadTransactions(this.page, this.per_page);
        }

        loadTransactions(page: number, per_page: number, isMore?: boolean) {
            const query: PaginationQuery = { page, per_page };

            if (isMore) {
                this.isMoreLoading = true;
            }

            getCustomerTransactions<PaginatedData<Transaction>>(this.user.id, query).then((data: PaginatedData<Transaction>) => {
                this.isPageLoading = false;
                this.isMoreLoading = false;
                this.total = data.total;
                this.transactions = [...(this.transactions || []), ...data.data];

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
    .page-mytransactions {
        overflow-y: auto;
    }

    .page__main {
        padding: 2rem;
        width: 100%;
    }

    .page__intro {
        color: var(--dim-white);
        font-size: 20px;
    }

    .transactions {
        margin: 1.5rem auto 0;
        width: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        background-color: var(--primary);
        border-radius: 4px;
        padding: 1rem 1rem 1.5rem;
    }

    .load__more__btn {
        margin: 2rem auto;
    }

    @media screen and (max-width: 768px) {
        .transactions {      
            width: 100%;
        }
    }
</style>