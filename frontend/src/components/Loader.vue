<template>
    <div class="loader__container">
        <div class="loader"></div>
    </div>
</template>

<script lang="ts">
    import { Component, Vue } from 'vue-property-decorator';

    @Component
    export default class Loader extends Vue { }
</script>

<style lang="scss" scoped>
    .loader__container {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        margin-top: 10%;

        .loader {
            height: 80px;
            width: 80px;
        }
    }

    @media screen and (max-width: 768px) {
        .loader__container {
            margin-top: 20%;

            .loader {
                height: 50px;
                width: 50px;
            }
        }
    }
</style>