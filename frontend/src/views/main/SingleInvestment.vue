<template>
    <div class="page page-singletransaction">
        <NavBar :user="user" :title="title" />
        <Loader v-if="isPageLoading" />

        <div class="page__main" v-else>
            <div class="columns is-mobile is-multiline">
                <div class="column is-one-third-desktop is-one-third-tablet is-full-mobile">
                    <div class="column__card">
                        <div class="img__placeholder"></div>

                        <div class="investment">
                            <h5 class="investment__name">{{customerInvestment.title}}</h5>
                            <h6 class="investment__amount">{{customerInvestmentTotal | currency}}</h6>
                            <span class="investment__date">Started on {{customerInvestmentStartDate}}</span>
                        </div>

                        <div class="withdrawal">
                            <template v-if="withdrawalEligiblity">
                                <template v-if="maxWithdrawableAmountRaw">
                                    <span class="withdrawal__notice">You can withdraw a maximum of {{maxWithdrawableAmount | currency}}</span>
                                    <button class="button withdrawal__button" @click.prevent="isWithdrawModalOpen = true">Withdraw</button>
                                </template>
                                <span class="withdrawal__notice" v-else>The investment amount is too low to be be withdrawn from.</span>
                            </template>
                            <span class="withdrawal__notice" v-else>You cannot withdraw at this time as the lock period for this investment is still active</span>
                        </div>
                    </div>
                </div>
                <div class="column is-two-thirds-desktop is-two-thirds-tablet is-full-mobile">
                    <div class="appreciation__history__controls">
                        <h5 class="appreciation__history__title">Appreciation History ({{appreciationHistoryType}})</h5>
                        <select class="appreciation__history__typeselect" v-model="appreciationHistoryType">
                            <option v-for="type of appreciationHistoryTypes" :key="type">{{type}}</option>
                        </select>
                    </div>

                    <div class="appreciation__history__container">
                        <DailyAppreciationHistory v-if="appreciationHistoryType === 'daily'" :customerInvestment="customerInvestment" />
                        <WeeklyAppreciationHistory v-if="appreciationHistoryType === 'weekly'" :customerInvestment="customerInvestment" />
                        <MonthlyAppreciationHistory v-if="appreciationHistoryType === 'monthly'" :customerInvestment="customerInvestment" />
                        <QuarterlyAppreciationHistory v-if="appreciationHistoryType === 'quarterly'" :customerInvestment="customerInvestment" />
                    </div>
                </div>
            </div>
            <WithdrawModal v-if="isWithdrawModalOpen" :maxWithdrawableAmount="maxWithdrawableAmount" :customerInvestment="customerInvestment" @close="withdrawModalCloseHandler" />
        </div>
    </div>
</template>

<script lang="ts">
    import NavBar from '../../components/NavBar.vue';
    import Loader from '../../components/Loader.vue';
    import DailyAppreciationHistory from '../../components/DailyAppreciationHistory.vue';
    import WeeklyAppreciationHistory from '../../components/WeeklyAppreciationHistory.vue';
    import MonthlyAppreciationHistory from '../../components/MonthlyAppreciationHistory.vue';
    import QuarterlyAppreciationHistory from '../../components/QuarterlyAppreciationHistory.vue';
    import WithdrawModal from '../../components/WithdrawModal.vue';
    import { CurrentUser } from '../../types/auth';
    import { currentUser } from '../../services/auth';
    import { NOTIFICATIONS } from '../../services/notification';
    import { getFromCustomerInvestmentCache, getWithdrawalEligibility, getMaxAmountWithdrawable, getCustomerInvestment } from '../../services/customer_investment';
    import { formatAmountFromAPI, getDateStringFromDateTime } from '../../common/utils';
    import { CustomerInvestmentRes } from '../../types/customer_investment';

    export default {
        name: 'SingleInvestment',
        components: { NavBar, Loader, WithdrawModal, DailyAppreciationHistory, WeeklyAppreciationHistory, MonthlyAppreciationHistory, QuarterlyAppreciationHistory },
        data() {
            return {
                title: 'My Investment',
                isPageLoading: true,
                customerInvestment: null,
                withdrawalEligiblity: null,
                maxWithdrawableAmountRaw: null,
                isWithdrawModalOpen: false,
                appreciationHistoryType: 'daily',
                appreciationHistoryTypes: ['daily', 'weekly', 'monthly', 'quarterly']
            }
        },
        notifications: { ...NOTIFICATIONS },
        created() {
            const id = Number(this.$route.params.id)

            this.customerInvestment = getFromCustomerInvestmentCache(id);

            if (this.customerInvestment) {
                Promise.all([getWithdrawalEligibility(id), getMaxAmountWithdrawable(id)]).then(results => {
                    this.withdrawalEligiblity = results[0];
                    this.maxWithdrawableAmountRaw = results[1];
                    this.isPageLoading = false;
                }).catch(err => this.error({ message: err }));
            } else {
                Promise.all([getCustomerInvestment(id), getWithdrawalEligibility(id), getMaxAmountWithdrawable(id)]).then(results => {
                    this.customerInvestment = results[0];
                    this.withdrawalEligiblity = results[1];
                    this.maxWithdrawableAmountRaw = results[2];
                    this.isPageLoading = false;
                }).catch(err => this.error({ message: err }));
            }
        },
        computed: {
            user: function() {
                const user = <CurrentUser> currentUser.getValue();
                return { id: user.id, name: user.name, username: user.user.username };
            },
            customerInvestmentTotal: function() {
                const { amount, appreciation } = this.customerInvestment;

                return formatAmountFromAPI((amount + appreciation));
            },
            maxWithdrawableAmount: function() {
                return formatAmountFromAPI(this.maxWithdrawableAmountRaw);
            },
            customerInvestmentStartDate: function() {
                return getDateStringFromDateTime(this.customerInvestment.created_at);
            }
        },
        methods: {
            withdrawModalCloseHandler(data?: CustomerInvestmentRes) {
                this.isWithdrawModalOpen = false;

                if (data) {
                    this.customerInvestment = data;

                    Promise.all([getWithdrawalEligibility(data.id), getMaxAmountWithdrawable(data.id)]).then(results => {
                        this.withdrawalEligiblity = results[0];
                        this.maxWithdrawableAmountRaw = results[1];
                    }).catch(err => this.error({ message: err }));
                }
            }
        }
    }
</script>

<style lang="scss" scoped>
    .page-singletransaction {
        overflow-y: auto;
    }

    .page__main {
        padding: 2rem;
        width: 100%;
    }

    .column__card {
        height: 100%;
        width: 100%;
        background-color: transparent;
        border: 1px solid var(--tertiary);
        border-radius: 6px;
        padding: 2rem 1.2rem;
    }

    .img__placeholder {
        height: 50px;
        width: 50px;
        background-color: var(--primary);
        border-radius: 4px;
    }

    .investment {
        margin-top: 8px;
    }

    .investment__name {
        font-size: 20px;
        color: var(--dim-white);
        text-transform: capitalize;
    }

    .investment__amount {
        font-size: 24px;
        color: var(--tertiary);
    }

    .investment__date {
        font-size: 14px;
        color: var(--dim-white);
    }

    .withdrawal {
        margin-top: 1.5rem;
        padding-top: 1rem;
        border-top: 1px solid var(--tertiary);
    }

    .withdrawal__notice {
        font-size: 13px;
        color: var(--dim-white);
        display: block;
    }

    .withdrawal__button {
        background-color: var(--tertiary-alt);
        color: var(--tertiary);
        border: none;
        font-size: 14px;
        margin-top: 1rem;

        &:hover {
            color: var(--dim-white);
            background-color: var(--tertiary);
        }
    }

    .appreciation__history__title {
        font-size: 18px;
        color: var(--dim-white);
        text-transform: capitalize;
    }

    .appreciation__history__container {
        height: 300px;
        max-height: 500px;
        overflow-y: auto;
        overflow-y: auto;
    }

    .appreciation__history__controls {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
    }

    .appreciation__history__typeselect {
        font-size: 14px;
        background-color: var(--tertiary-alt);
        color: var(--tertiary);
        border-color: var(--tertiary-alt);
        padding: 4px;
        cursor: pointer;
        text-transform: capitalize;
    }
</style>