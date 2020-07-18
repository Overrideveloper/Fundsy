<template>
    <div class="modal">
        <div class="modal-background"></div>
        <div class="modal-content">
            <div class="modal__card">
                <div class="modal__card__title">Withdraw from <span class="investment__title">"{{customerInvestment.title}}"</span></div>
                <form class="modal__form" @submit.prevent="submit">
                    <div class="modal__form__group">
                        <label for="title" class="form__group__label">Amount (&#8358;)<span class="label__required">*</span></label>
                        <input name="title" type="number" class="form__group__input form__group__input-currency" placeholder="1000"
                            v-model="$v.amount.$model" :class="{ 'form__group__input-invalid': $v.amount.$error || (amount > maxWithdrawableAmount) }">
                        <small class="form__group__info">You can withdraw between {{minWithdrawable | currency}} and {{maxWithdrawableAmount | currency}}</small>
                    </div>
                    
                    <div class="modal__form__group">
                        <small class="form__group__info">A {{withdrawalCost}}% withdrawal cost will be charged on this withdrawal</small>
                    </div>

                    <div class="modal__form__controls">
                        <button class="modal__form__cancel button" :disabled="isSubmitting" @click.prevent="close()">Cancel</button>

                        <div class="modal__form__controls m-0">
                            <button type="submit" class="modal__form__submit button" :class="{ 'is-loading': isSubmitting }" :disabled="!isFormValid">Submit</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
    import { Component, Vue, Prop, Emit } from 'vue-property-decorator';
    import { required, minValue, maxValue } from 'vuelidate/lib/validators';
    import { NOTIFICATIONS } from '../services/notification';
    import { CustomerInvestmentRes, CustomerInvestmentWithdrawReq } from '../types/customer_investment';
    import { withdrawFromCustomerInvestment } from '../services/customer_investment';
    import config from '../common/config';
    
    @Component({
        validations: {
            amount: { required, minValue: minValue(Number(config.MIN_WITHDRAWAL)) }
        },
        notifications: { ...NOTIFICATIONS }
    })
    export default class WithdrawModal extends Vue {
        @Prop({ required: true }) maxWithdrawableAmount!: number;
        @Prop({ required: true }) customerInvestment!: CustomerInvestmentRes;

        amount: number = null;
        minWithdrawable: number = Number(config.MIN_WITHDRAWAL);
        isSubmitting: boolean = false;

        get withdrawalCost() {
            const { withdrawal_cost } = this.customerInvestment.investment;
            return withdrawal_cost;
        }

        get isFormValid() {
            return !this.$v.$invalid && !(this.amount > this.maxWithdrawableAmount)
        }

        @Emit('close')
        close(data?: CustomerInvestmentRes) {
            return data;
        }

        submit() {
            const req: CustomerInvestmentWithdrawReq = { id: this.customerInvestment.id, amount: this.amount };

            this.isSubmitting = true;

            withdrawFromCustomerInvestment(req).then(data => {
                (<any> this).success({ message: 'Withdrawal successful '});
                this.close(data);
            }).catch(err => {
                this.isSubmitting = false;
                (<any> this).error({ message: err });
            });
        }
    }
</script>

<style lang="scss" scoped>
    .investment__title {
        text-transform: capitalize;
        font-weight: 500;
    }
</style>