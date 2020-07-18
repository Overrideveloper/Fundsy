<template>
    <div class="page page-investments">
        <NavBar :title="title" :user="user" />
        <Loader v-if="isPageLoading" />
        <div class="page__main" v-else>
            <Empty v-if="isEmpty" text="There are currently no investment options available. Please check again later." />

            <template v-else>
                <p class="page__intro">
                    We have {{total}} investment option{{ total === 1 ? '' : 's'}} for you to choose from</p>

                <div class="investments">
                    <Investment v-for="investment of investments" :key="investment.id" :investment="investment" btnText="Invest now"
                        @actionButtonClicked="onInvestmentActionButtonClick" />
                </div>
                
                <button @click.prevent="loadInvestments(page, per_page, true)" v-if="showLoadMore" class="load__more__btn button" :class="{ 'is-loading': isMoreLoading }">Load More</button>
        
                <InvestModal v-if="isInvestModalOpen" :investment="investmentToInvestIn" :customerId="user.id" @close="onInvestModalCloseEmit" />
            </template>
        </div>
    </div>
</template>

<script lang="ts">
    import { Component, Vue } from 'vue-property-decorator';
    import NavBar from '@/components/NavBar.vue';
    import Loader from '@/components/Loader.vue';
    import Empty from '@/components/Empty.vue';
    import Investment from '@/components/Investment.vue';
    import InvestModal from '@/components/InvestModal.vue';
    import { currentUser } from '../../services/auth';
    import { CurrentUser } from '../../types/auth';
    import { PaginationQuery, PaginatedData } from '../../types';
    import { investmentCache, getInvestments } from '../../services/investment';
    import { NOTIFICATIONS } from '../../services/notification';
    import { InvestmentRes } from '../../types/investment';

    @Component({
        components: { NavBar, Loader, Investment, Empty, InvestModal },
        notifications: { ...NOTIFICATIONS }
    })
    export default class Invest extends Vue {
        title: string = 'Invest';
        investments: InvestmentRes[] = null;
        isPageLoading: boolean = true;
        isMoreLoading: boolean = false;
        isInvestModalOpen: boolean = false;
        investmentToInvestIn: InvestmentRes = null;
        page: number = 1;
        per_page: number = 10;
        total: number = 0;

        get user() {
            const user = <CurrentUser> currentUser.getValue();
            return { id: user.id, name: user.name, username: user.user.username };
        }

        get isEmpty() {
            return !this.investments || (this.investments && !this.investments.length)
        }

        get showLoadMore() {
            return this.investments && this.investments.length !== this.total;
        }

        created() {
            this.investments = investmentCache.getValue();

            if (this.investments) {
                this.page = Math.floor(this.investments.length/this.per_page) + 1;
                this.isPageLoading = false;
            }

            investmentCache.subscribe(val => this.investments = val);
            this.loadInvestments(this.page, this.per_page);
        }

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
            }).catch(err => (<any> this).error({ message: err }));
        }

        onInvestmentActionButtonClick(investment: InvestmentRes) {
            this.investmentToInvestIn = investment;
            this.isInvestModalOpen = true;
        }

        onInvestModalCloseEmit() {
            this.investmentToInvestIn = null;
            this.isInvestModalOpen = false;
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

    .page__intro {
        color: var(--dim-white);
        font-size: 20px;
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
</style>