<template>
    <div class="page page-customers">
        <NavBar :title="title" :user="user" />
        <Loader v-if="isPageLoading" />
        <div class="page__main" v-else>
            <p class="customer__count">{{total}} customer{{ total === 1 ? '' : 's'}}</p>

            <DataTable :columns="columns" :rows="customers" :total="total" :per_page="per_page" :buttons="buttons"
            @pageChange="handlePageChange" />
        </div>
    </div>
</template>

<script lang="ts">
    import { Component, Vue } from 'vue-property-decorator';
    import NavBar from '@/components/NavBar.vue';
    import Loader from '@/components/Loader.vue';
    import DataTable from '@/components/DataTable.vue';
    import { currentUser } from '../../services/auth';
    import { customerCache, getCustomers } from '../../services/customer';
    import { CustomerRes as Customer } from '../../types/customer';
    import { CurrentUser } from '../../types/auth';
    import { PaginationQuery, PaginatedData, DatatableColumn, DatatableButton } from '../../types';
    import { NOTIFICATIONS } from '../../services/notification';
    import { getDateStringFromDateTime } from '../../common/utils';

    @Component({
        notifications: { ...NOTIFICATIONS },
        components: { NavBar, Loader, DataTable }
    })
    export default class Customers extends Vue {
        customers: Customer[] = null;
        isPageLoading: boolean = true;
        page: number = 1;
        per_page: number = 10;
        total: number = 0;
        columns: DatatableColumn[] = [
            { label: 'Name', field: 'name' },
            { label: 'Date Registered', field: 'created_at', formatFn: getDateStringFromDateTime },
            { label: '', field: 'buttons' }
        ];
        buttons: DatatableButton[] = [
            { id: 'view_investments', link: '/admin/customers/:id/transactions', displayText: 'View Transactions' }
        ];
        title: string = 'Customers';

        get user() {
            const user = <CurrentUser> currentUser.getValue();
            return { name: user.name, username: user.user.username };
        }

        created() {
            this.customers = customerCache.getValue();

            if (this.customers) {
                this.page = Math.floor(this.customers.length/this.per_page) + 1;
                this.isPageLoading = false;
            }

            customerCache.subscribe(val => this.customers = val);
            this.loadCustomers(this.page, this.per_page);
        }

        loadCustomers(page: number, per_page: number) {
            const query: PaginationQuery = { page, per_page };

            getCustomers<PaginatedData<Customer>>(query).then((data: PaginatedData<Customer>) => {
                this.total = data.total;
                this.isPageLoading = false;

                if (data.data.length === per_page) {
                    this.page += 1;
                }
            }).catch(err => (<any> this).error({ message: err }));
        }

        handlePageChange() {
            (<any> this).info({ message: 'Fetching customers...' });
            this.loadCustomers(this.page, this.per_page);
        }
    }
</script>

<style lang="scss" scoped>
    .page-customers {
        overflow-y: auto;
    }

    .page__main {
        padding: 3rem;
    }
    
    .customer__count {
        color: var(--dim-white);
        font-size: 13px;
        margin:  0 0 1rem;
    }
</style>