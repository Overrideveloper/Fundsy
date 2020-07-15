<template>
    <div>
        <vue-good-table :columns="columns" :rows="rows" :totalRows="total" v-on:on-page-change="onPageChange" :fixed-header="true" :pagination-options="options">
            <template slot="table-row" slot-scope="props">
                <div v-if="props.column.field === 'buttons'">
                    <template v-for="button of buttons">
                        <router-link v-if="button.link" :to="replacePathParam(button.link, props.row)" :key="button.id">
                            <button class="button datatable__button">{{ button.displayText }}</button>
                        </router-link>
                        <button v-else class="button datatable__button" :key="button.id" @click.prevent="onButtonClick(button.id, props.row)">{{ button.displayText }}</button>
                    </template>
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
            onButtonClick(btnId: string, data: any) {
                this.$emit('buttonClick', btnId, data);
            },
            replacePathParam(link: string, data: any) {
                const linkArr = link.split('/')
                const linkParams = linkArr.filter(l => l.includes(':'));

                linkParams.map(param => {
                    const paramString = param.match(/[^:]+$/g)[0];
                    const paramValue = data[paramString];
                    linkArr.splice(linkArr.findIndex(l => l === param), 1, paramValue)
                });

                return linkArr.join('/')
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