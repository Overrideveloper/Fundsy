<template>
    <div class="page page-register">
        <h4 class="page-register__title">Fundsy.</h4>
        <div class="register__card">
            <h5 class="register__card__title">Create An Account</h5>

            <form class="register__form" @submit.prevent="submit">
                <div class="register__form__group">
                    <label for="name" class="form__group__label">Name</label>
                    <input name="name" type="text" class="form__group__input" placeholder="Charles Darwin" :class="{ 'form__group__input-invalid': $v.name.$error }"
                        v-model="$v.name.$model">
                </div>
                <div class="register__form__group">
                    <label for="username" class="form__group__label">Username</label>
                    <input name="username" type="text" class="form__group__input" placeholder="charlesdarwin" :class="{ 'form__group__input-invalid': $v.username.$error }"
                        v-model.trim="$v.username.$model">
                    <small v-if="!$data._isUsernameUnique" class="form__group__info form__group__info-error">Username already in use</small>
                </div>
                <div class="register__form__group">
                    <label for="password" class="form__group__label">Password</label>
                    <input name="password" type="password" class="form__group__input" placeholder="*******" :class="{ 'form__group__input-invalid': $v.password.$error }"
                        v-model.trim="$v.password.$model">
                    <small class="form__group__info">Password should not be less than 7 characters</small>
                </div>

                <div class="register__form__actions">
                    <router-link to="/login" class="register__form__link">Already have an account?</router-link>
                    <button class="register__form__submit button" type="submit" :class="{ 'is-loading': isSubmitting }" :disabled="!isFormValid">Register</button>
                </div>
            </form>
        </div>
    </div>
</template>

<script lang="ts">
    import { required, minLength } from 'vuelidate/lib/validators';
    import { doesUserExist, signup, login } from '../../services/auth';
    import { NOTIFICATIONS } from '../../services/notification';
    import { Subject } from 'rxjs';
    import { debounceTime, distinctUntilChanged, switchMap } from 'rxjs/operators';
import { SignupReq, LoginReq } from '../../types/auth';
import router from '../../router';

    export default {
        name: 'Register',
        data() {
            return {
                name: '',
                username: '',
                password: '',
                $username: new Subject<string>(),
                _isUsernameUnique: true,
                isSubmitting: false
            }
        },
        validations: {
            name: { required },
            username: { required },
            password: { required, minLength: minLength(7) }
        },
        notifications: { ...NOTIFICATIONS },
        created() {
            this.isUsernameUnique(this.$data.$username).subscribe(flag => this.$data._isUsernameUnique = !flag);
        },
        computed: {
            isFormValid: function() {
                return !(this.$v.$invalid || !this.$data._isUsernameUnique)
            }
        },
        methods: {
            isUsernameUnique($username: Subject<string>) {
                return $username.pipe(
                    debounceTime(1000),
                    distinctUntilChanged(),
                    switchMap(async username => {
                        try {
                            return await doesUserExist(username);
                        } catch (err) {
                            return true;
                        }
                    })
                );
            },
            submit() {
                if (this.isFormValid) {
                    const signupCredentials: SignupReq = { name: this.name, username: this.username, password: this.password };
                    const loginCredentials: LoginReq = { username: this.username, password: this.password };

                    this.isSubmitting = true;

                    signup(signupCredentials).then(_ => {
                        login(loginCredentials).then(_ => {
                            router.replace('/main');
                            this.success({ message: 'Welcome to Fundsy' });
                        }).catch(err => {
                            this.error({ message: err });
                            this.isSubmitting = false;
                        });
                    }).catch(err => {
                        this.error({ message: err });
                        this.isSubmitting = false;
                    });
                }
            }
        },
        watch: {
            "username": {
                handler: function(val) {
                    this.$data.$username.next(val);
                }
            }
        }
    }
</script>

<style lang="scss" scoped>
    .page-register {
        background-color: var(--primary-dark);
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }

    .page-register__title {
        font-size: 24px;
        font-weight: 600;
        color: #FFFFFF;
        margin-bottom: 1rem;
    }

    .register__card {
        height: auto;
        width: 360px;
        background-color: white;
        border-radius: 6px;
        padding: 1.5rem 2rem 2rem;
    }

    .register__card__title {
        font-size: 16px;
        font-weight: 400;
        color: #000000;
        text-align: center;
        margin-bottom: 1rem;
    }

    .register__form__group:nth-child(even) {
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

        &.form__group__info-error {
            color: crimson;
        }
    }

    .register__form__submit {
        height: 32px;
        width: 50%;
        color: var(--primary-dark);
        border: none;
        border-radius: 4px;
        cursor: pointer;
        margin-bottom: 8px;
        flex-grow: 1;
        background-color: whitesmoke;
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

    .register__form__actions {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-top: 1rem;
        flex-wrap: wrap;
    }

    .register__form__link {
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
        .register__card {
            width: 80%;
        }
    }
</style>
