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
    import { Component, Vue } from 'vue-property-decorator';
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
    import { PaginationQuery, DatatableColumn, PaginatedData } from '../../types';
    import { CustomerRes } from '../../types/customer';

    @Component({
        components: { NavBar, Loader, DataTable },
        notifications: { ...NOTIFICATIONS }
    })
    export default class Transactions extends Vue {
        customer: CustomerRes = null;
        transactions: Transaction[] = null;
        isPageLoading: boolean = true;
        columns: DatatableColumn[] = [
            { label: "Date", field: "created_at", formatFn: getDateStringFromDateTime },
            { label: "Description", field: "description" },
            { label: "Amount", field: "amount", formatFn: this.amountFormatFn },
            { label: "Type", field: "type" }
        ];
        page: number = 1;
        per_page: number = 5;
        total: number = 0;
        id: number = null;

        get user() {
            const user = <CurrentUser> currentUser.getValue();
            return { name: user.name, username: user.user.username };
        }

        get title() {
            if (this.customer) {
                return `${this.customer.name}'s Transactions`;
            }

            return 'Transactions';
        }

        created() {
            this.id = Number(this.$route.params.id);
            this.customer = getFromCustomerCache(this.id);

            if (!this.customer) {
                this.loadCustomerInformation(this.id);
            }

            this.loadCustomerTransactions(this.id, this.page, this.per_page);
        }

        loadCustomerInformation(id: number) {
            getCustomer(id).then(data => {
                this.customer = data;
            }).catch(err => (<any>this).error({ message: err }));
        }

        loadCustomerTransactions(id: number, page: number, per_page: number) {
            const query: PaginationQuery = { page, per_page };

            getCustomerTransactions<PaginatedData<Transaction>>(id, query).then(data => {
                this.total = data.total;
                this.isPageLoading = false;

                if (data.data.length === per_page) {
                    this.page += 1;
                }

                this.addTransactionsToList(data.data);
            }).catch(err => (<any> this).error({ message: err }));
        }

        addTransactionsToList(transactions: Transaction[]) {
            let list = this.transactions || [];
            list = [...list, ...transactions];

            this.transactions = Array.from(new Set(list.map(l => l.id))).map(id => <Transaction> list.find(l => l.id === id));
        }

        amountFormatFn(value: number) {
            return formatAmountToCurrency(formatAmountFromAPI(value));
        }

        handlePageChange() {
            (<any> this).info({ message: 'Fetching investments...'})
            this.loadCustomerTransactions(this.id, this.page, this.per_page);
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