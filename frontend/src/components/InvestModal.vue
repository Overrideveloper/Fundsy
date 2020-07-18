<template>
    <div class="modal">
        <div class="modal-background"></div>
        <div class="modal-content">
            <div class="modal__card">
                <div class="modal__card__title">Invest in <span class="investment__title">"{{investment.title}}"</span></div>
                <form class="modal__form" @submit.prevent="submit">
                    <div class="modal__form__group">
                        <label for="title" class="form__group__label">Investment Title <span class="label__required">*</span></label>
                        <input name="title" type="text" class="form__group__input" placeholder="Graduate School Fund"
                            v-model="$v.title.$model" :class="{ 'form__group__input-invalid': $v.title.$error }">
                    </div>

                    <div class="modal__form__group">
                        <label for="title" class="form__group__label">Amount (&#8358;)<span class="label__required">*</span></label>
                        <input name="title" type="number" class="form__group__input form__group__input-currency" placeholder="1000"
                            v-model="$v.amount.$model" :class="{ 'form__group__input-invalid': $v.amount.$error }">
                        <small class="form__group__info">The least amount you can invest is &#8358;1000.</small>
                    </div>

                    <div class="modal__form__controls">
                        <button class="modal__form__cancel button" :disabled="isSubmitting" @click.prevent="close()">Cancel</button>

                        <div class="modal__form__controls m-0">
                            <button type="submit" class="modal__form__submit button" :class="{ 'is-loading': isSubmitting }" :disabled="$v.$invalid">Submit</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
    import { Component, Vue, Prop, Emit } from 'vue-property-decorator';
    import { required, minValue } from 'vuelidate/lib/validators';
    import { NOTIFICATIONS } from '../services/notification';
    import { CustomerInvestmentCreateReq } from '../types/customer_investment';
    import { createCustomerInvestment } from '../services/customer_investment';
    import { InvestmentRes } from '../types/investment';

    @Component({
        validations: {
            title: { required },
            amount: { required, minValue: minValue(1000) }
        },
        notifications: { ...NOTIFICATIONS }
    })
    export default class InvestModal extends Vue {
        @Prop({ required: true }) investment!: InvestmentRes;
        @Prop({ required: true }) customerId!: number;

        title: string = '';
        amount: number = null;
        isSubmitting: boolean = false;

        @Emit('close')
        close() { }

        submit() {
            const req: CustomerInvestmentCreateReq = {
                customer_id: this.customerId,
                title: this.title,
                amount: this.amount,
                investment_id: this.investment.id
            };

            this.isSubmitting = true;

            createCustomerInvestment(req).then(_ => {
                (<any> this).success({ message: `You have invested in ${this.investment.title}`});
                this.close();
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