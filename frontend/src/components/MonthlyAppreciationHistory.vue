<template>
    <div class="appreciation__history">
        <Loader v-if="isLoading" />
        <template v-else>
            <Empty v-if="isEmpty" text="No appreciation history yet." />

            <div v-else>
                <div class="container">
                    <div v-for="log in logs" :key="log.month + log.year" class="appreciation">
                        <div class="appreciation__info">
                            <h6 class="appreciation__date">{{formatMonth(log.month)}}, {{log.year}}</h6>

                            <div>
                                <span class="appreciation__amount appreciation__amount-old">{{formatAmount(log.old_amount) | currency}}</span>
                                <span class="appreciation__arrow">&rAarr;</span>
                                <span class="appreciation__amount">{{formatAmount(log.new_amount) | currency}}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <button @click.prevent="loadAppreciationHistory(page, per_page, true)" v-if="showLoadMore" class="load__more__btn button" :class="{ 'is-loading': isMoreLoading }">Load More</button>
        </template>
    </div>
</template>

<script lang="ts">
    import { Component, Vue, Prop } from 'vue-property-decorator';
    import Loader from './Loader.vue';
    import Empty from './Empty.vue';
    import { NOTIFICATIONS } from '../services/notification';
    import { getAppreciationLogs } from '../services/customer_investment';
    import { CustomerInvestmentRes } from '../types/customer_investment';
    import { AppreciationLogResMonthly, AppreciationLogType } from '../types/appreciation_log';
    import { formatAmountFromAPI, MONTHS } from '../common/utils';
    import { PaginationQuery, PaginatedData } from '../types';

    @Component({
        components: { Loader, Empty },
        notifications: { ...NOTIFICATIONS },
    })
    export default class MonthlyAppreciationHistory extends Vue {
        @Prop({ required: true }) customerInvestment!: CustomerInvestmentRes;

        isLoading: boolean = false;
        isMoreLoading: boolean = false;
        logs: AppreciationLogResMonthly[] = null;
        page: number = 1;
        per_page: number = 10;
        total: number = 0;

        created() {
            this.loadAppreciationHistory(this.page, this.per_page)
        }

        get isEmpty() {
            return this.logs && !this.logs.length;
        }

        get showLoadMore() {
            return this.logs && this.logs.length !== this.total;
        }

        addLogsToList(logs: AppreciationLogResMonthly[]) {
            let list: AppreciationLogResMonthly[] = this.logs || [];
            list = [ ...list, ...logs ];

            this.logs = Array.from(new Set(list.map(l => l.month))).map(month => <AppreciationLogResMonthly> list.find(c => c.month === month));
        }

        loadAppreciationHistory(page: number, per_page: number, isMore?: boolean) {
            const { id } = this.customerInvestment;

            const query: PaginationQuery = { page: this.page, per_page: this.per_page }

            if (isMore) {
                this.isMoreLoading = true;
            }

            getAppreciationLogs<PaginatedData<AppreciationLogResMonthly>>(id, AppreciationLogType.MONTHLY, query).then((data: PaginatedData<AppreciationLogResMonthly>) => {this.total = data.total;
                this.addLogsToList(data.data)

                this.isMoreLoading = false;
                this.isLoading = false;

                if (data.data.length === per_page) {
                    this.page += 1;
                }
            }).catch(err => (<any> this).error({ message: err }));
        }

        formatMonth(month: number) {
            return MONTHS[month - 1];
        }

        formatAmount(amount: number) {
            return formatAmountFromAPI(amount);
        }
    }
</script>

<style lang="scss" scoped></style>