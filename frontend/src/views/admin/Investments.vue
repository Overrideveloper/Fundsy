<template>
    <div class="page page-investments">
        <NavBar :title="title" :user="user" />
        <Loader v-if="isPageLoading" />
        <div class="page__main" v-else>
            <p class="investment__count">{{total}} investment{{ total === 1 ? '' : 's'}}</p>

            <div class="investments">
                <button @click="openAddModal" class="new__investment">
                    <svg class="new__investment__icon" width="50" height="50"  viewBox="0 0 36 36" preserveAspectRatio="xMidYMid meet">
                        <path d="M26.17,17H19V9.83a1,1,0,0,0-2,0V17H9.83a1,1,0,0,0,0,2H17v7.17a1,1,0,0,0,2,0V19h7.17a1,1,0,0,0,0-2Z" class="clr-i-outline clr-i-outline-path-1"></path>
                        <path d="M18,2A16,16,0,1,0,34,18,16,16,0,0,0,18,2Zm0,30A14,14,0,1,1,32,18,14,14,0,0,1,18,32Z" class="clr-i-outline clr-i-outline-path-2"></path>
                        <rect x="0" y="0" width="36" height="36" fill-opacity="0"/>
                    </svg>
                    <span class="new__investment__text">New Investment</span>
                </button>

                <template v-if="investments">
                    <Investment v-for="investment of investments" :key="investment.id" :investment="investment" btn_text="Edit"
                        v-on:investmentActionButtonClicked="openEditModal" />
                </template>
            </div>

            <button @click="loadInvestments(page, per_page, true)" v-if="investments" class="load__more__btn button" :class="{ 'is-loading': isMoreLoading }">Load More</button>

            <template v-if="isAddModalOpen">
                <AddInvestment v-on:close="closeAddModal" />
            </template>
            
            <template v-if="isEditModalOpen">
                <EditInvestment v-on:close="closeEditModal" :investment="investmentToEdit" />
            </template>
        </div>
    </div>
</template>

<script lang="ts">
    import NavBar from '@/components/NavBar.vue';
    import Loader from '@/components/Loader.vue';
    import Investment from '@/components/Investment.vue';
    import AddInvestment from '@/components/admin/AddInvestment.vue';
    import EditInvestment from '@/components/admin/EditInvestment.vue';
    import { currentUser } from '../../services/auth';
    import { CurrentUser } from '../../types/auth';
    import { PaginationQuery, PaginatedData } from '../../types';
    import { investmentCache, getInvestments } from '../../services/investment';
    import { NOTIFICATIONS } from '../../services/notification';
    import { InvestmentRes } from '../../types/investment';

    export default {
        name: 'Investments',
        components: { NavBar, Loader, Investment, AddInvestment, EditInvestment },
        notifications: { ...NOTIFICATIONS },
        data() {
            return {
                title: 'Investments',
                investments: null,
                isPageLoading: true,
                isMoreLoading: false,
                isAddModalOpen: false,
                isEditModalOpen: false,
                investmentToEdit: null,
                page: 1,
                per_page: 10,
                total: 0
            }
        },
        created() {
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
            loadInvestments(page: number, per_page: number, isMore?: boolean) {
                const query: PaginationQuery = { page, per_page };

                if (isMore) {
                    this.isMoreLoading = true;
                }

                getInvestments<PaginatedData<InvestmentRes>>(query).then((data: PaginatedData<InvestmentRes>) => {
                    this.total = data.total;
                    this.isPageLoading = false;
                    this.isMoreLoading = false;

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

        }
    }
</script>

<style lang="scss" scoped>
    .page-investments {
        overflow-y: auto;
    }

    .page__main {
        padding: 2rem;
    }

    .investment__count {
        color: var(--dim-white);
        font-size: 13px;
    }

    .investments {
        margin-top: 1.5rem;
        display: flex;
        flex-wrap: wrap;
    }

    .new__investment {
        height: 180px;
        width: 240px;
        border: 1px solid var(--tertiary);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: transparent;
        margin-right: 40px;
        margin: 0 16px 32px 16px;
        display: flex;
        flex-direction: column;
        cursor: pointer;
        transition: all 500ms ease;

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

    .load__more__btn {
        display: block;
        margin: 1rem auto;
        padding: 1rem 2rem;
        border-radius: 4px;
        border: none;
        background-color: #3b53ec1e;
        color: var(--tertiary);
        line-height: inherit;
        height: inherit;
        cursor: pointer;
        font-size: 14px;

        &:hover {
            color: var(--dim-white);
            background-color: var(--tertiary);   
        }
    }
</style>