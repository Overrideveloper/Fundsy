<template>
    <router-link class="customerinvestment__link" :to="link">
        <div class="customerinvestment">
            <div>
                <div class="customerinvestment__info">
                    <div class="img__placeholder"></div>
                    <div class="customerinvestment__info__detail">
                        <h5 class="customerinvestment__title">{{customerInvestment.title}}</h5>
                        <h5 class="customerinvestment__amount">{{customerInvestment.amount | currency}}</h5>
                    </div>
                </div>
                <div class="customerinvestment__meta">
                    <h5 class="customerinvestment__meta__text">{{customerInvestment.investment}}</h5>
                </div>

            </div>
        </div>
    </router-link>
</template>

<script lang="ts">
    import { CustomerInvestmentRes } from '../types/customer_investment';
    import { formatAmountFromAPI, getDateStringFromDateTime } from '../common/utils';

    export default {
        name: 'CustomerInvestmentComponent',
        props: ["customer_investment"],
        computed: {
            customerInvestment: function() {
                const { title, amount: _amount, created_at, id, investment, appreciation } = <CustomerInvestmentRes> this.$props.customer_investment;

                const amount = formatAmountFromAPI(_amount + appreciation)
                const date = getDateStringFromDateTime(created_at)

                return { id, title, amount, date, investment: investment.title };
            },
            link: function() {
                const { id } = <CustomerInvestmentRes> this.$props.customer_investment;
                return `/main/my-investments/${id}`;
            }
        }
    }
</script>

<style lang="scss" scoped>
    .customerinvestment__link {
        display: flex;
    }

    .customerinvestment {
        height: auto;
        width: 250px;
        border: 1px solid var(--tertiary);
        border-radius: 8px;
        padding: 1rem;
        margin: 0 16px 32px 16px;
        transition: all 500ms ease;
        cursor: pointer;

        .customerinvestment__info {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }

        &:hover {
            box-shadow: 0 0.5em 1em -0.125em rgba(0, 209, 178, 0.1), 0 0px 0 1px rgba(0, 209, 178, 0.1);
        }
    }

    .customerinvestment__info__detail {
        width: 70%;
    }

    .customerinvestment__title {
        color: var(--tertiary);
        text-align: right;
        overflow-wrap: normal;
        word-break: break-word;
        white-space: break-spaces;
        font-size: 20px;
        font-weight: 500;
    }

    .customerinvestment__amount {
        color: var(--dim-white);
        text-align: right;
        overflow-wrap: normal;
        word-break: break-word;
        white-space: break-spaces;
        font-size: 18px;
    }

    .customerinvestment__meta {
        width: max-content;
        padding: 4px 8px;
        background-color: var(--tertiary-alt);
        border-radius: 4px;

        .customerinvestment__meta__text {
            font-size: 10px;
            color: var(--dim-white);
            text-transform: capitalize;
        }
    }


    .img__placeholder {
        height: 50px;
        width: 50px;
        background-color: var(--primary);
        border-radius: 4px;
        margin-right: 16px;
    }

    @media screen and (max-width: 768px) {
        .customerinvestment__link {
            flex-grow: 1;
        }

        .customerinvestment {
            width: 100%;
            flex-grow: 1;
        }
    }
</style>