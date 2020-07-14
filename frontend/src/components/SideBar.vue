<template>
    <aside class="menu sidemenu">
        <div class="sidemenu__logo">
            <h5 class="sidemenu__logo__text">Fundsy.</h5>
            <h5 class="sidemenu__logo__text sidemenu__logo__text-sm">F.</h5>
        </div>
        <ul class="menu-list sidemenu__main">
            <li class="menu__list__item" v-for="route in routes" :key="route.to">
                <router-link :to="route.to" class="list__item">
                    <clr-icon :shape="route.icon" class="list__item__icon" :class="{'is-solid': route.icon_solid }"></clr-icon>
                    <span class="list__item__title">{{route.name}}</span>
                </router-link>
            </li>
        </ul>

        <div class="section-break"></div>

        <ul class="menu-list sidemenu__settings">
            <li>
                <button @click="logout()" class="list__item button list__item-btn" :class="{ 'is-loading': isLoggingOut }">
                    <clr-icon shape="logout" class="list__item-btn__icon is-solid"></clr-icon>
                    <span class="list__item-btn__text" >Logout</span>
                </button>
            </li>
        </ul>
    </aside>
</template>

<script lang="ts">
    import { logout } from '../services/auth'
    import { NOTIFICATIONS, prompt } from '../services/notification'
    import router from '../router'

    export default {
        name: 'SideBar',
        props: ["routes"],
        notifications: { ...NOTIFICATIONS },
        data() {
            return {
                isLoggingOut: false
            }
        },
        methods: {
            logout() {
                prompt('warning', 'Log out', 'Are you sure?', true).then(willAct => {
                    if (willAct) {
                        this.isLoggingOut = true;

                        logout().then(_ => router.replace('/login')).catch(err => {
                            this.error({ message: err });
                            this.isLoggingOut = false;
                        });
                    }
                });
            }
        }
    }
</script>

<style lang="scss" scoped>
    .sidemenu {
        width: auto;
        background-color: var(--primary-dark);
        height: 100%;
        border-right: 1px solid var(--primary-dark-alt);
        position: relative;
        padding: 0 1rem;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
    }

    .sidemenu__logo {
        margin: 1rem 0 1rem 0;
        width: 100%;

        .sidemenu__logo__text {
            text-align: center;
            font-size: 24px;
            font-weight: 500;
            color: var(--dim-white);

            &.sidemenu__logo__text-sm {
                display: none;
            }
        }
    }

    .sidemenu__main {
        margin-top: 50%;
        width: 100%;
    }

    .sidemenu__settings {
        width: 100%;
        margin-top: auto;
        margin-bottom: 1rem;
    }

    .list__item {
        height: 40px;
        width: auto;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 4px;
        border: 1px solid var(--dim-white);
        cursor: pointer;
        transition: all 500ms ease;

        .list__item__icon {
            margin-right: 8px;
            width: 26px;
            height: 26px;
            color: var(--dim-white);
        }

        .list__item__title {
            font-size: 14px;
            color: var(--dim-white);
            transition: all 5ms ease;
        }

        &.router-link-active, .router-link-exact-active, &:hover {
            background-color: #25294a8c;
            border: none;

            .list__item__title {
                font-size: 14px;
                color: var(--tertiary);
            }

            .list__item__icon {
                color: var(--tertiary);
            }
        }
    }

    .list__item-btn {
        width: 100%;
        padding: 1rem;
        background-color: #3b53ec1e;
        border: none;
        color: var(--tertiary);
        font-size: 14px;
        cursor: pointer;

        .list__item-btn__icon {
            height: 26px;
            width: 26px;
            margin-right: 4px;
        }

        &:hover {
            background: var(--tertiary);
            color: var(--dim-white);
        }
    }

    .menu__list__item {
        &:not(:last-of-type) {
            margin-bottom: 1rem;
        }
    }

    @media screen and (max-width: 767px) {
        .sidemenu__logo__text {
            display: none;

            &.sidemenu__logo__text-sm {
                display: inherit !important;
            }
        }

        .list__item__icon {
            margin: 0 !important;
        }

        .list__item__title {
            display: none;
        }

        .list__item-btn {
            width: auto;

            .list__item-btn__text {
                display: none;
            }

            .list__item-btn__icon {
                margin: 0;
            }
        }
    }
</style>