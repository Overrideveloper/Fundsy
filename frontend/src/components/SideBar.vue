<template>
    <aside class="menu sidemenu">
        <ul class="menu-list sidemenu__main">
            <li class="menu__list__item" v-for="route in routes" :key="route.to">
                <router-link :to="route.to" class="list__item">
                    <span class="list__item__title">{{route.name}}</span>
                </router-link>
            </li>
        </ul>

        <div class="section-break"></div>

        <ul class="menu-list sidemenu__settings">
            <li>
                <button @click="logout()" class="list__item button list__item-btn" :class="{ 'is-loading': isLoggingOut }">
                    Logout
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
        width: 18%;
        background-color: var(--primary-dark);
        height: 100%;
        border-right: 1px solid var(--primary-dark-alt);
        position: relative;
        padding: 0 1rem;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
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
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        padding: 1rem;
        border-radius: 4px;
        border: 1px solid var(--dim-white);
        cursor: pointer;
        transition: all 500ms ease;
        
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
        }
    }

    .list__item-btn {
        background-color: #3b53ec1e;
        border: none;
        color: var(--tertiary);
        font-size: 14px;
        cursor: pointer;

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
</style>