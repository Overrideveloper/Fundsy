<template>
    <div class="page page-customers">
        <NavBar :title="title" :user="user" />
        <Loader v-if="isPageLoading" />
        <div class="page__main" v-else>
            <DataTable :columns="columns" :rows="customers" :total="total" :per_page="per_page" :buttons="buttons"
            @pageChange="handlePageChange" @buttonClick="handleButtonClick" />
        </div>
    </div>
</template>

<script lang="ts">
    import NavBar from '@/components/NavBar.vue';
    import Loader from '@/components/Loader.vue';
    import DataTable from '@/components/DataTable.vue';
    import { currentUser } from '../../services/auth';
    import { customerCache, getCustomers } from '../../services/customer';
    import { CustomerRes as Customer } from '../../types/customer';
    import { CurrentUser } from '../../types/auth';
    import { PaginationQuery, PaginatedData } from '../../types';
    import { NOTIFICATIONS } from '../../services/notification';
import { getDateStringFromDateTime } from '../../common/utils';

"2020-07-12T01:33:17.093689+00:00"
"yyyy-mm-ddThh:mm:ss"
    export default {
        name: 'Investments',
        components: { NavBar, Loader, DataTable },
        notifications: { ...NOTIFICATIONS },
        data() {
            return {
                title: 'Customers',
                customers: null,
                isPageLoading: true,
                page: 1,
                per_page: 10,
                total: 0,
                columns: [
                    { label: 'Name', field: 'name' },
                    { label: 'Date Registered', field: 'created_at', formatFn: getDateStringFromDateTime },
                    { label: '', field: 'buttons' }
                ],
                buttons: [
                    { id: 'view_investments', displayText: 'View Investments' }
                ]
            }
        },
        created() {
            if (this.customers) {
                this.isPageLoading = false;
            }

            customerCache.subscribe(val => this.customers = val);
            this.loadCustomers(this.page, this.per_page);
        },
        computed: {
            user: function() {
                const user = <CurrentUser> currentUser.getValue();
                return { name: user.name, username: user.user.username };
            }
        },
        methods: {
            loadCustomers(page: number, per_page: number) {
                const query: PaginationQuery = { page, per_page };

                getCustomers<PaginatedData<Customer>>(query).then((data: PaginatedData<Customer>) => {
                    this.total = data.total;
                    this.isPageLoading = false;

                    if (data.data.length === per_page) {
                        this.page += 1;
                    }
                }).catch(err => this.error({ message: err }));
            },
            handlePageChange() {
                this.info('Fetching customers...')
                this.loadCustomers(this.page, this.per_page);
            },
            handleButtonClick(buttonId: string) { }
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
</style>