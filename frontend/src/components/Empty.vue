<template>
    <div class="empty">
        <clr-icon shape="block" class="empty__icon is-solid"></clr-icon>
        <span class="empty__text">{{text}}</span>

        <template v-if="hasAction">
            <router-link v-if="actionLink" :to="actionLink">
                <button class="empty__button button">{{actionText}}</button>
            </router-link>
            <button v-else @click.prevent="triggerAction()" class="empty__button button">{{actionText}}</button>
        </template>
    </div>
</template>

<script lang="ts">
    import { Component, Vue, Prop, Emit } from 'vue-property-decorator';

    @Component
    export default class Empty extends Vue {
        @Prop({ required: true }) text!: string;
        @Prop() actionLink: string;
        @Prop() actionText: string;
        @Prop() hasAction: boolean;
        
        @Emit('actionTriggered')
        triggerAction() { }
    }
</script>

<style lang="scss" scoped>
    .empty {
        margin: 5rem 0;
        display: flex;
        width: 100%;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 0 1rem;
    }

    .empty__icon {
        height: 48px;
        width: 48px;
        fill: var(--tertiary);
    }

    .empty__text {
        color: var(--dim-white);
        font-size: 22px;
        margin: 1rem 0;
        text-align: center;
    }

    .empty__button {
        font-size: 14px;
        background-color: var(--tertiary-alt);
        color: var(--tertiary);
        border: none;
        cursor: pointer;
        transition: all 500ms ease;

        &:hover, &:active {
            color: var(--dim-white);
            background-color: var(--tertiary);
        }
    }
</style>