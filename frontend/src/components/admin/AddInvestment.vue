<template>
    <div class="modal">
        <div class="modal-background"></div>
        <div class="modal-content">
            <div class="modal__card">
                <div class="modal__card__title">New Investment</div>
                <form class="modal__form" @submit.prevent="submit">
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
                            <input name="lock-period" type="number" class="form__group__input" placeholder="0" v-model="lockPeriodAmount">
                            <select class="form__group__input form__group__input-select" v-model="lockPeriodType">
                                <option :value="null">--Select One--</option>
                                <option v-for="type in durationTypes" :key="type" :value="type">{{type}}</option>
                            </select>
                        </div>
                    </div>

                    <div class="modal__form__group">
                        <label for="withdrawal-cost" class="form__group__label">Withdrawal cost (%)</label>
                        <input style="width:" name="withdrawal-cost" type="number" class="form__group__input" placeholder="0" v-model="withdrawalCost">
                    </div>

                    <div class="modal__form__controls">
                        <button class="modal__form__cancel button" @click.prevent="close()">Cancel</button>

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
    import { required, minValue } from 'vuelidate/lib/validators';
    import { durationTypes, getSecondsFromDuration } from '../../common/utils';
    import { InvestmentReq } from '../../types/investment';
    import { createInvestment } from '../../services/investment';
    import { NOTIFICATIONS, prompt } from '../../services/notification';

    export default {
        name: 'AddInvestment',
        data() {
            return {
                durationTypes: durationTypes,
                title: '',
                appRate: null,
                appDurationAmount: null,
                appDurationType: null,
                lockPeriodType: null,
                lockPeriodAmount: null,
                withdrawalCost: null,
                isSubmitting: false
            }
        },
        validations: {
            title: { required },
            appRate: { required, minValue: minValue(1) },
            appDurationAmount: { required, minValue: minValue(1) },
            appDurationType: { required }
        },
        notifications: { ...NOTIFICATIONS },
        methods: {
            close(addSuccess?: boolean) {
                this.$emit('close', addSuccess);
            },
            submit() {
                this.$v.$touch();

                if(!this.$v.$invalid) {
                    prompt('info', 'Create investment', 'Are you sure?').then(willAct => {
                        if (willAct) {
                            const lock_period = (this.lockPeriodAmount && this.lockPeriodType) ? getSecondsFromDuration(this.lockPeriodType, this.lockPeriodAmount) : 0;
                            const req: InvestmentReq = {
                                title: this.title,
                                appreciation_amount: this.appRate,
                                appreciation_duration: getSecondsFromDuration(this.appDurationType, this.appDurationAmount),
                                withdrawal_cost: this.withdrawalCost || 0,
                                lock_period
                            }

                            this.isSubmitting = true;

                            createInvestment(req).then(_ => {
                                this.close(true);
                                this.success({ message: 'New investment created'})
                            }).catch(err => {
                                this.isSubmitting = false;
                                this.error({ message: err });
                            });
                        }
                    })
                }
            }
        }
    }
</script>

<style lang="scss" scoped>
</style>