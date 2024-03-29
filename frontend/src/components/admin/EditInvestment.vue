<template>
    <div class="modal">
        <div class="modal-background"></div>
        <div class="modal-content">
            <div class="modal__card">
                <div class="modal__card__title">Edit Investment</div>
                <form class="modal__form" @submit.prevent="submitEdit">
                    <div class="modal__form__group">
                        <label for="title" class="form__group__label">Title <span class="label__required">*</span></label>
                        <input style="width: 70%" name="title" type="text" class="form__group__input" placeholder="Investment Beta" v-model="$v.title.$model" :class="{ 'form__group__input-invalid': $v.title.$error }">
                    </div>

                    <div class="modal__form__divider">Appreciation</div>

                    <div class="modal__form__flex">
                        <div class="modal__form__group" style="margin-right: 16px">
                            <label for="app-rate" class="form__group__label">Rate (%) <span class="label__required">*</span></label>
                            <input name="app-rate" type="number" class="form__group__input" placeholder="20" v-model="$v.appRate.$model" :class="{ 'form__group__input-invalid': $v.appRate.$error }">
                            <small class="form__group__info">Appreciation rate should be at least 1%.</small>
                        </div>
                        <div class="modal__form__group">
                            <label for="app-duration" class="form__group__label">Duration <span class="label__required">*</span></label>
                            <div class="modal__form__flex modal__form__flex-inputonly">
                                <input name="app-duration" type="number" class="form__group__input" placeholder="0" v-model="$v.appDurationAmount.$model" :class="{ 'form__group__input-invalid': $v.appDurationAmount.$error }">
                                <select class="form__group__input form__group__input-select" v-model="$v.appDurationType.$model" :class="{ 'form__group__input-invalid': $v.appDurationType.$error }">
                                    <option :value="null">--Select One--</option>
                                    <option v-for="type in durationTypes" :key="type" :value="type">{{type}}</option>
                                </select>
                            </div>
                            <small class="form__group__info">Appreciation duration should be at least 1 day.</small>
                        </div>
                    </div>

                    <div class="modal__form__group">
                        <label for="lock-period" class="form__group__label">Lock period</label>
                        <div class="modal__form__flex modal__form__flex-inputonly">
                            <input name="lock-period" type="number" class="form__group__input" placeholder="0" :class="{ 'form__group__input-invalid': $v.lockPeriodAmount.$error }" v-model="$v.lockPeriodAmount.$model">
                            <select class="form__group__input form__group__input-select" v-model="lockPeriodType">
                                <option :value="null">--Select One--</option>
                                <option v-for="type in durationTypes" :key="type" :value="type">{{type}}</option>
                            </select>
                        </div>
                    </div>

                    <div class="modal__form__group">
                        <label for="withdrawal-cost" class="form__group__label">Withdrawal cost (%)</label>
                        <input style="width: 58%" name="withdrawal-cost" type="number" class="form__group__input" placeholder="0" :class="{ 'form__group__input-invalid': $v.withdrawalCost.$error }" v-model="$v.withdrawalCost.$model">
                    </div>

                    <div class="modal__form__controls">
                        <button class="modal__form__cancel button" @click.prevent="close()">Cancel</button>

                        <div class="modal__form__controls m-0">
                            <button class="modal__form__danger button" :class="{ 'is-loading': isDeleteSubmitting }" @click.prevent="submitDelete()">Delete</button>
                            <button type="submit" class="modal__form__submit button" :class="{ 'is-loading': isEditSubmitting }" :disabled="$v.$invalid">Submit</button>
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
    import { durationTypes, getSecondsFromDuration, getDurationFromSeconds, DurationType } from '../../common/utils';
    import { InvestmentReq, InvestmentRes } from '../../types/investment';
    import { editInvestment, deleteInvestment } from '../../services/investment';
    import { NOTIFICATIONS, prompt } from '../../services/notification';

    @Component({
        validations: {
            title: { required },
            appRate: { required, minValue: minValue(1) },
            appDurationAmount: { required, minValue: minValue(1) },
            appDurationType: { required },
            lockPeriodAmount: { minValue: minValue(0) },
            withdrawalCost: { minValue: minValue(0) }
        },
        notifications: { ...NOTIFICATIONS }
    })
    export default class EditInvestmentModal extends Vue {
        @Prop({ required: true }) investment!: InvestmentRes;
        
        durationTypes: DurationType[] = durationTypes;
        id: number = null;
        title: string = '';
        appRate: number = null;
        appDurationAmount: number = null;
        appDurationType: DurationType = null;
        lockPeriodType: DurationType = null;
        lockPeriodAmount: number = null;
        withdrawalCost: number = null;
        isEditSubmitting: boolean = false;
        isDeleteSubmitting: boolean = false;

        created() {
            this.parseInvestmentPropToForm();
        }

        parseInvestmentPropToForm() {
            const { title, appreciation_amount, appreciation_duration, lock_period, withdrawal_cost } = this.investment;
            const { amount: appDurationAmount, type: appDurationType } = getDurationFromSeconds(appreciation_duration);

            this.id = this.investment.id;
            this.title = title;
            this.appRate = appreciation_amount;
            this.appDurationAmount = appDurationAmount;
            this.appDurationType = appDurationType;
            this.withdrawalCost = withdrawal_cost ? withdrawal_cost : null;

            if (lock_period) {
                const duration = getDurationFromSeconds(lock_period);
                this.lockPeriodType = duration.type;
                this.lockPeriodAmount = duration.amount;
            }
        }

        @Emit('close')
        close(deleteSuccess?: boolean) {
            return deleteSuccess;
        }

        submitEdit() {
            this.$v.$touch();

            if(!this.$v.$invalid) {
                prompt('info', 'Edit investment', 'Are you sure?').then(willAct => {
                    if (willAct) {
                        const lock_period = (this.lockPeriodAmount && this.lockPeriodType) ? getSecondsFromDuration(this.lockPeriodType, this.lockPeriodAmount) : 0;
                        const req: InvestmentReq = {
                            title: this.title,
                            appreciation_amount: this.appRate,
                            appreciation_duration: getSecondsFromDuration(this.appDurationType, this.appDurationAmount),
                            withdrawal_cost: this.withdrawalCost || 0,
                            lock_period
                        }

                        this.isEditSubmitting = true;

                        editInvestment(this.id, req).then(_ => {
                            this.close();
                            (<any> this).success({ message: 'Investment edited'})
                        }).catch(err => {
                            this.isEditSubmitting = false;
                            (<any> this).error({ message: err });
                        });
                    }
                });
            }
        }

        submitDelete() {
            prompt('warning', 'Delete investment', 'Are you sure?', true).then(willAct => {
                if (willAct) {
                    this.isDeleteSubmitting = true;

                    deleteInvestment(this.id).then(_ => {
                        this.close(true);
                        (<any> this).success({ message: 'Investment deleted'})
                    }).catch(err => {
                        this.isDeleteSubmitting = false;
                        (<any> this).error({ message: err });
                    });
                }
            });
        }
    }
</script>

<style lang="scss" scoped>
</style>