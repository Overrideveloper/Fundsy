<template>
    <div class="page page-register">
        <h4 class="page-register__title">Fundsy</h4>
        <div class="register__card">
            <h5 class="register__card__title">Create An Account</h5>

            <form class="register__form">
                <div class="register__form__group">
                    <label for="name" class="form__group__label">Name</label>
                    <input name="name" type="text" class="form__group__input" placeholder="Korede Bello">
                </div>
                <div class="register__form__group">
                    <label for="username" class="form__group__label">Username</label>
                    <input name="username" type="text" class="form__group__input" placeholder="koredebello">
                </div>
                <div class="register__form__group">
                    <label for="password" class="form__group__label">Password</label>
                    <input name="password" type="password" class="form__group__input" placeholder="*******">
                    <small class="form__group__info">Password should not be less than 7 characters</small>
                </div>

                <div class="register__form__actions">
                    <router-link to="/login" class="register__form__link">Already have an account?</router-link>
                    <button class="register__form__submit" type="submit">Register</button>
                </div>
            </form>
        </div>
    </div>
</template>

<script lang="ts">
    export default {
        name: 'Register',
        components: { }
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

        &:hover, &:active {
            color: white;
            background-color: var(--primary-dark);
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
