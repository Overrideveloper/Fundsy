<template>
    <div class="page page-login">
        <h4 class="page-login__title">Fundsy.</h4>
        <div class="login__card">
            <h5 class="login__card__title">Sign In</h5>

            <form class="login__form" @submit.prevent="submit">
                <div class="login__form__group">
                    <label for="username" class="form__group__label">Username</label>
                    <input name="username" type="text" class="form__group__input" :class="{ 'form__group__input-invalid': $v.username.$error }"
                        placeholder="charlesdarwin" v-model.trim="$v.username.$model">
                </div>
                <div class="login__form__group">
                    <label for="password" class="form__group__label">Password</label>
                    <input name="password" type="password" class="form__group__input" :class="{ 'form__group__input-invalid': $v.password.$error }"
                        placeholder="*******" v-model.trim="$v.password.$model">
                    <small class="form__group__info">Password should not be less than 7 characters</small>
                </div>

                <div class="login__form__actions">
                    <router-link to="/register" class="login__form__link">Create an account</router-link>
                    <button class="login__form__submit button" type="submit" :class="{ 'is-loading': isSubmitting }" :disabled="$v.$invalid">Sign me in</button>
                </div>
            </form>
        </div>
    </div>
</template>

<script lang="ts">
    import router from '../../router';
    import { required, minLength } from 'vuelidate/lib/validators';
    import { LoginReq, CurrentUser } from '../../types/auth';
    import { login } from '../../services/auth';
    import { NOTIFICATIONS } from '../../services/notification';

    export default {
        name: 'Login',
        data() {
            return {
                username: '',
                password: '',
                isSubmitting: false
            }
        },
        validations: {
            username: { required },
            password: { required, minLength: minLength(7) }
        },
        notifications: { ...NOTIFICATIONS },
        methods: {
            submit() {
                this.$v.$touch();

                if(!this.$v.$invalid) {
                    const credentials: LoginReq = { username: this.username, password: this.password };
                    this.isSubmitting = true;

                    login(credentials).then((user: CurrentUser) => {
                        if (user.user.is_admin) {
                            router.replace('/admin');
                        } else {
                            router.replace('/main');
                        }

                        this.success({ message: 'Welcome back' })
                    }).catch(err => {
                        this.error({ message: err });
                        this.isSubmitting = false;
                    });
                }
            }
        }
    }
</script>

<style lang="scss" scoped>
    .page-login {
        background-color: var(--primary-dark);
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }

    .page-login__title {
        font-size: 24px;
        font-weight: 600;
        color: #FFFFFF;
        margin-bottom: 1rem;
    }

    .login__card {
        height: auto;
        width: 360px;
        background-color: white;
        border-radius: 6px;
        padding: 1.5rem 2rem 2rem;
    }

    .login__card__title {
        font-size: 16px;
        font-weight: 400;
        color: #000000;
        text-align: center;
        margin-bottom: 1rem;
    }

    .login__form__group:nth-child(even) {
        margin: 0.8rem 0;
    } 

    .form__group__label, .form__group__input {
        display: block;
    }

    .form__group__label {
        font-size: 13px;
        text-transform: capitalize;
        color: grey;
        margin-bottom: 0.2rem;
        font-weight: 400;
    }

    .form__group__input {
        width: 100%;
        font-size: 13px;
        height: 32px;
        border-radius: 4px;
        border: 1px solid gainsboro;
        padding: 0 0.5rem;
        box-sizing: border-box;
        color: var(--primary-dark);

        &.form__group__input-invalid {
            border-color: crimson;
        }

        &:focus {
            border-color: var(--primary-dark);
        }
    }

    .form__group__info {
        font-size: 12px;
        color: grey;
        font-weight: 300;
    }

    .login__form__submit {
        height: 32px;
        width: 50%;
        color: var(--primary-dark);
        border: none;
        border-radius: 4px;
        cursor: pointer;
        background-color: whitesmoke;
        margin-bottom: 8px;
        flex-grow: 1;
        font-size: 13px;

        &:hover, &:active {
            color: white;
            background-color: var(--primary-dark);
        }

        &:disabled {
            opacity: 0.7;
            pointer-events: none;
        }
    }

    .login__form__actions {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-top: 1rem;
        flex-wrap: wrap;
    }

    .login__form__link {
        font-size: 12px;
        color: var(--primary-dark);
        font-weight: 400;
        cursor: pointer;
        margin: 0 24px 8px 0;

        &:hover, &:active {
            text-decoration: underline;
        }

        &:active {
            color: grey;
        }
    }

    @media screen and (max-width: 767px) {
        .login__card {
            width: 80%;
        }
    }
</style>
