<template>
    <div class="transaction">
        <div class="transaction__info">
            <h6 class="transaction__desc">{{ _transaction.description }} | {{ _transaction.title}} </h6>
            <h5 class="transaction__amount">{{ _transaction.amount | currency }}</h5>
        </div>
        <div class="transaction__info">
            <span class="transaction__type" :class="{ 'transaction__type-debit': isDebit }">{{ _transaction.type }}</span>
            <span class="transaction__date">{{ _transaction.date }}</span>
        </div>
    </div>
</template>

<script lang="ts">
    import { formatAmountFromAPI, getDateStringFromDateTime } from '../common/utils';
    import { Transaction, TransactionType } from '../types/transaction';

    export default {
        name: 'CustomerTransactionComponent',
        props: ['transaction'],
        computed: {
            _transaction: function() {
                const { description, type, amount: _amount, created_at, customer_investment } = <Transaction> this.$props.transaction;

                const title = customer_investment.title;
                const amount = formatAmountFromAPI(_amount);
                const date = getDateStringFromDateTime(created_at);

                return { description, title, amount, date, type }
            },
            isDebit: function() {
                const { type } = <Transaction> this.$props.transaction;
                return type === TransactionType.WITHDRAWAL;
            }
        }
    }
</script>

<style lang="scss" scoped>
    .transaction {
        width: 100%;
        padding-top: 8px;

        .transaction__type {
            font-size: 10px;
            background-color: var(--tertiary-alt);
            color: var(--tertiary);
            padding: 2px 8px;
            border-radius: 6px;
            margin-top: 4px;
            font-weight: 500;

            &.transaction__type-debit {
                background-color: rgba(220, 20, 60, 0.2);
                color: crimson;
            }
        }

        .transaction__info {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
        }

        .transaction__desc {
            color: var(--dim-white);
            font-size: 16px;
        }

        .transaction__amount {
            color: var(--tertiary);
            font-size: 20px;
        }

        .transaction__date {
            font-size: 13px;  
            color: var(--dim-white);
        }

        &:not(:last-child) {
            border-bottom: 0.5px solid var(--dim-white);
            margin-bottom: 4px;
            padding-bottom: 16px;
        }
    }
</style>