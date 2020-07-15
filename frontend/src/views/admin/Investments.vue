<template>
    <div class="page page-investments">
        <NavBar :title="title" :user="user" />
        <Loader v-if="isPageLoading" />
        <div class="page__main" v-else>
            <div class="page__main__controls">
                <p class="investment__count">{{total}} investment{{ total === 1 ? '' : 's'}}</p>

                <button  class="button new__button" @click="openAddModal">
                    <clr-icon class="new__button__icon" shape="plus-circle"></clr-icon>
                    New investment
                </button>
            </div>
            
            <DataTable :columns="columns" :rows="investments" :total="total" :per_page="per_page" :buttons="buttons"
            @pageChange="handlePageChange" @buttonClick="handleButtonClick" />

            <AddInvestment v-if="isAddModalOpen" v-on:close="closeAddModal" />
            <EditInvestment v-if="isEditModalOpen" v-on:close="closeEditModal" :investment="investmentToEdit" />
        </div>
    </div>
</template>

<script lang="ts">
    import NavBar from '@/components/NavBar.vue';
    import Loader from '@/components/Loader.vue';
    import DataTable from '@/components/DataTable.vue';
    import Investment from '@/components/Investment.vue';
    import AddInvestment from '@/components/admin/AddInvestment.vue';
    import EditInvestment from '@/components/admin/EditInvestment.vue';
    import { currentUser } from '../../services/auth';
    import { CurrentUser } from '../../types/auth';
    import { PaginationQuery, PaginatedData } from '../../types';
    import { investmentCache, getInvestments } from '../../services/investment';
    import { NOTIFICATIONS } from '../../services/notification';
    import { InvestmentRes } from '../../types/investment';
    import { getDurationFromSeconds } from '../../common/utils';

    export default {
        name: 'Investments',
        components: { NavBar, Loader, Investment, AddInvestment, EditInvestment, DataTable },
        notifications: { ...NOTIFICATIONS },
        data() {
            return {
                title: 'Investments',
                investments: null,
                isPageLoading: true,
                isAddModalOpen: false,
                isEditModalOpen: false,
                investmentToEdit: null,
                page: 1,
                per_page: 10,
                total: 0,
                columns: [
                    { label: 'Title', field: 'title' },
                    { label: 'Appreciation Rate', field: 'appreciation_amount', formatFn: this.appreciationRateFormatFn },
                    { label: 'Appreciation Duration', field: 'appreciation_duration', formatFn: this.appreciationDurationFormatFn },
                    { label: 'Lock Period', field: 'lock_period', formatFn: this.lockPeriodFormatFn },
                    { label: 'Withdrawal Cost', field: 'withdrawal_cost', formatFn: this.withdrawalCostFormatFn },
                    { label: '', field: 'buttons' }
                ],
                buttons: [
                    { id: 'edit_investment', displayText: 'Edit' }
                ]
            }
        },
        created() {
            if (this.investments) {
                this.isPageLoading = false;
            }

            investmentCache.subscribe(val => this.investments = val);
            this.loadInvestments(this.page, this.per_page);
        },
        computed: {
            user: function() {
                const user = <CurrentUser> currentUser.getValue();
                return { name: user.name, username: user.user.username };
            }
        },
        methods: {
            loadInvestments(page: number, per_page: number) {
                const query: PaginationQuery = { page, per_page };

                getInvestments<PaginatedData<InvestmentRes>>(query).then((data: PaginatedData<InvestmentRes>) => {
                    this.total = data.total;
                    this.isPageLoading = false;

                    if (data.data.length === per_page) {
                        this.page += 1;
                    }
                }).catch(err => this.error({ message: err }));
            },
            openAddModal() {
                this.isAddModalOpen = true;
            },
            openEditModal(investment: InvestmentRes) {
                this.investmentToEdit = investment;
                this.isEditModalOpen = true;
            },
            closeAddModal(addSuccess?: boolean) {
                this.isAddModalOpen = false;

                if (addSuccess) {
                    this.total += 1;
                }
            },
            closeEditModal(deleteSuccess?: boolean) {
                this.isEditModalOpen = false;
                this.investmentToEdit = null;

                if (deleteSuccess) {
                    this.total -= 1;
                }
            },
            withdrawalCostFormatFn(value: number) {
                return value ? 'None' : `${value}%`;
            },
            lockPeriodFormatFn(value: number) {
                if (value) {
                    const { amount, type } = getDurationFromSeconds(value);
                    return `${amount} ${type}`;
                }

                return 'None';
            },
            appreciationRateFormatFn(value: number) {
                return `${value}%`;
            },
            appreciationDurationFormatFn(value: number) {
                const { amount, type } = getDurationFromSeconds(value);
                
                return `${amount} ${type}`;
            },
            handlePageChange() {
                this.info('Fetching investments...')
                this.loadInvestments(this.page, this.per_page);
            },
            handleButtonClick(buttonId: string, data: any) {
                if (buttonId === 'edit_investment') {
                    this.openEditModal(data as InvestmentRes);
                }
            }
        }
    }
</script>

<style lang="scss" scoped>
    .page-investments {
        overflow-y: auto;
    }

    .page__main {
        padding: 3rem;
    }

    .investment__count {
        color: var(--dim-white);
        font-size: 13px;
    }

    .page__main__controls {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        margin:  0 0 1rem;
    }

    .new__button {
        font-size: 14px;
        background-color: var(--tertiary-alt);
        color: var(--tertiary);
        cursor: pointer;
        border: none;
        transition: all 500ms ease;


        .new__button__icon {
            margin-right: 4px;
        }

        &:hover {
            background-color: var(--tertiary);
            color: white;
        }
    }
</style>