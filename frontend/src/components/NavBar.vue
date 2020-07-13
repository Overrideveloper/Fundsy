<template>
    <div class="nav">
        <h3 class="nav__title">{{title}}</h3>
        
        <div class="nav__user">
            <h5 class="nav__user__name">{{user.name}}</h5>
            <h6 class="nav__user__username">@{{user.username}}</h6>
        </div>
    </div>
</template>

<script lang="ts">
    export default {
        name: 'NavBar',
        props: ["title", "user"]
    }
</script>

<style lang="scss" scoped>
    .nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid var(--primary-dark-alt);
        padding: 1rem 1.5rem;
        flex-wrap: wrap;

        .nav__title {
            color: var(--tertiary);
            font-size: 20px;
            margin: 0rem 1px 1rem 0;
        }

        .nav__user {
            margin-bottom: 1px;

            .nav__user__name, .nav__user__username {
                color: var(--dim-white);
            }

            .nav__user__name {
                font-size: 12px;
            }

            .nav__user__username {
                font-size: 11px;
            }
        }
    }
</style>