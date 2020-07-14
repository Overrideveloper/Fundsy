<template>
    <div>
        <vue-good-table :columns="columns" :rows="rows" :totalRows="total" v-on:on-page-change="onPageChange" :fixed-header="true" :pagination-options="options">
            <template slot="table-row" slot-scope="props">
                <div v-if="props.column.field === 'buttons'">
                    <button class="button datatable__button" v-for="button of buttons" :key="button.id" @click.prevent="onButtonClick(button.id)">{{ button.displayText }}</button>
                </div>
            </template>
        </vue-good-table>
    </div>
</template>

<script lang="ts">
    import 'vue-good-table/dist/vue-good-table.css'

    export default {
        name: 'DataTable',
        props: ["columns", "rows", "total", "per_page", "buttons"],
        data() {
            return {
                options: {
                    enabled: true,
                    mode: 'remote',
                    position: 'bottom',
                    perPage: this.$props.per_page
                }
            }
        },
        methods: {
            onPageChange() {
                this.$emit('pageChange');
            },
            onButtonClick(btnId: string) {
                this.$emit('buttonClick', btnId);
            }
        }
    }
</script>

<style lang="scss" scoped>
    .datatable__button {
        background-color: #25294a8c;
        color: var(--tertiary);
        margin-right: 16px;
        font-size: 14px;
        border: none;
        cursor: pointer;

        &:hover {
            color: white;
            background-color: var(--tertiary);
        }
    }
</style>