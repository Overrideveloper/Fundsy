<template>
    <div class="investment">
        <div>
            <div class="investment__info">
                <div class="img__placeholder"></div>
                <h5 class="investment__title">{{_investment.title}}</h5>
            </div>
            <div>
                <h5 class="investment__meta">- Appreciates {{_investment.appreciationRate}}% in {{_investment.appreciationDuration}}</h5>
                <h5 class="investment__meta">- {{_investment.lockPeriod}}</h5>
                <h5 class="investment__meta">- {{_investment.withdrawalCost}}</h5>
                <button class="investment__btn" @click.prevent="buttonClick()">{{btnText}}</button>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
    import { Component, Vue, Prop, Emit } from 'vue-property-decorator';
    import { InvestmentReq, InvestmentRes } from '../types/investment'
    import { getDurationFromSeconds } from '../common/utils';

    @Component
    export default class InvestmentComponent extends Vue {
        @Prop({ required: true }) investment!: InvestmentRes;
        @Prop({ required: true }) btnText!: string;

        get _investment() {
            const { title, appreciation_amount, appreciation_duration, lock_period, withdrawal_cost } = this.investment;

            const { amount: appDurationAmount, type: appDurationType } = getDurationFromSeconds(appreciation_duration);
            const appreciationDuration = `${appDurationAmount} ${appDurationType}`;

            let withdrawalCost = 'No withdrawal fees', lockPeriod = 'No lock period';

            if (withdrawal_cost) {
                withdrawalCost = `${withdrawal_cost}% withdrawal fees`;
            }

            if (lock_period) {
                const duration = getDurationFromSeconds(lock_period);
                lockPeriod = `Lock period of ${duration.amount} ${duration.type}`;
            }

            return { title, withdrawalCost, lockPeriod, appreciationDuration, appreciationRate: appreciation_amount };
        }

        @Emit('actionButtonClicked')
        buttonClick() {
            return this.investment;
        }
    }
</script>

<style lang="scss" scoped>
    .investment {
        height: auto;
        width: 320px;
        border: 1px solid var(--tertiary);
        border-radius: 8px;
        padding: 1rem;
        margin: 0 16px 32px 16px;
        transition: all 500ms ease;

        .investment__info {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }

        &:hover {
            box-shadow: 0 0.5em 1em -0.125em rgba(0, 209, 178, 0.1), 0 0px 0 1px rgba(0, 209, 178, 0.1);
        }
    }

    .investment__title {
        color: var(--tertiary);
        text-align: right;
        margin-bottom: 16px;
        overflow-wrap: normal;
        word-break: break-word;
        white-space: break-spaces;
        width: 70%;
        text-transform: capitalize;
    }

    .investment__meta {
        color: var(--dim-white);
        text-align: right;
        font-size: 12px;
    }

    .investment__btn {
        background-color: var(--tertiary-alt);
        color: var(--dim-white);
        border: none;
        padding: 0.2rem 1rem;
        display: block;
        margin: 0.5rem 0 0 auto;
        transition: all 500ms ease;
        font-size: 16px;
        cursor: pointer;

        &:hover {
            color: white;
            background-color: var(--tertiary);
        }
    }

    .img__placeholder {
        height: 50px;
        width: 50px;
        background-color: var(--primary);
        border-radius: 4px;
        margin-right: 16px;
    }
</style>