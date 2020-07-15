<template>
    <div class="page page-transactions">
        <NavBar :title="title" :user="user" />
        <Loader v-if="isPageLoading" />

        <div class="page__main" v-else>
            <p class="transaction__count">{{total}} transaction{{ total === 1 ? '' : 's'}}</p>

            <DataTable :columns="columns" :rows="transactions" :total="total" :per_page="per_page" @pageChange="handlePageChange"/>
        </div>
    </div>
</template>

<script lang="ts">
    import NavBar from '@/components/NavBar.vue';
    import Loader from '@/components/Loader.vue';
    import DataTable from '@/components/DataTable.vue';
    import { CurrentUser } from '../../types/auth';
    import { currentUser } from '../../services/auth';
    import { getFromCustomerCache, getCustomer } from '../../services/customer';
    import { getCustomerTransactions } from '../../services/transaction';
    import { Transaction } from '../../types/transaction';
    import { NOTIFICATIONS } from '../../services/notification';
    import { getDateStringFromDateTime, formatAmountFromAPI, formatAmountToCurrency } from '../../common/utils';
    import { PaginationQuery } from '../../types';

    export default {
        name: 'Transactions',
        components: { NavBar, Loader, DataTable },
        data() {
            return {
                customer: null,
                transactions: null,
                isPageLoading: true,
                columns: [
                    { label: "Date", field: "created_at", formatFn: getDateStringFromDateTime },
                    { label: "Amount", field: "amount", formatFn: this.amountFormatFn },
                    { label: "Type", field: "type" }
                ],
                page: 1,
                per_page: 10,
                total: 0,
            }
        },
        notifications: { ...NOTIFICATIONS },
        created() {
            const customerId = Number(this.$route.params.id);
            this.customer = getFromCustomerCache(customerId);

            if (!this.customer) {
                this.loadCustomerInformation(customerId);
            }

            this.loadCustomerTransactions(customerId, this.page, this.per_page);
        },
        computed: {
            user: function() {
                const user = <CurrentUser> currentUser.getValue();
                return { name: user.name, username: user.user.username };
            },
            title: function() {
                if (this.customer) {
                    return `${this.customer.name}'s Transactions`;
                }

                return 'Transactions';
            }
        },
        methods: {
            loadCustomerInformation(id: number) {
                getCustomer(id).then(data => {
                    this.customer = data;
                }).catch(err => this.error({ message: err }));
            },
            loadCustomerTransactions(id: number, page: number, per_page: number) {
                const query: PaginationQuery = { page, per_page };

                getCustomerTransactions(id, false, query).then(data => {
                    this.total = data.total;
                    this.isPageLoading = false;

                    if (data.data.length === per_page) {
                        this.page += 1;
                    }

                    this.addTransactionsToList(data.data);
                }).catch(err => this.error({ message: err }));
            },
            addTransactionsToList(transactions: Transaction[]) {
                let list = this.transactions || [];
                list = [...list, ...transactions];

                this.transactions = Array.from(new Set(list.map(l => l.id))).map(id => <Transaction> list.find(l => l.id === id));
            },
            amountFormatFn(value: number) {
                return formatAmountToCurrency(formatAmountFromAPI(value));
            },
            handlePageChange() {
                this.info('Fetching investments...')
                this.loadCustomerTransactions(this.$route.params.id, this.page, this.per_page);
            }
        }

    }
</script>

<style lang="scss" scoped>
    .page-transactions {
        overflow-y: auto;
    }

    .page__main {
        padding: 3rem;
    }

    .transaction__count {
        color: var(--dim-white);
        font-size: 13px;
        margin: 0 0 1rem;
    }
</style>