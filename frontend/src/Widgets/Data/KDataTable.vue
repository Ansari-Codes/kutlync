<script setup lang="ts">

import { computed } from 'vue'

type Row = Record<string, unknown>

const props = withDefaults(
    defineProps<{
        rows: Row[]
        columns?: string[]
        slotColumns?: string[]
    }>(),
    {
        columns: undefined,
        slotColumns: () => []
    }
)

const displayColumns = computed(() => {

    // Explicitly supplied columns
    if (props.columns?.length) {
        return props.columns
    }

    // Otherwise automatically determine columns
    const longestRow = props.rows.reduce(
        (longest, row) =>
            Object.keys(row).length > Object.keys(longest).length
                ? row
                : longest,
        {}
    )

    return Object.keys(longestRow)
})

const formatHeader = (header: string) => {
    return header
        .replace(/[\_-]/g, ' ')
        .replace(/\b\w/g, char => char.toUpperCase())
}

const formatValue = (value: unknown) => {

    if (value === null || value === undefined) {
        return '—'
    }

    if (typeof value === 'boolean') {
        return value ? 'Yes' : 'No'
    }

    if (typeof value === 'object') {
        return JSON.stringify(value)
    }

    return String(value)
}

const hasSlot = (column: string) => {
    return props.slotColumns.includes(column)
}

</script>

<template>

    <div class="k-table-wrapper">

        <div class="k-table-scroll">

            <table class="k-table">

                <thead>
                    <tr>
                        <th
                            v-for="column in displayColumns"
                            :key="column"
                            scope="col"
                        >
                            {{ formatHeader(column) }}
                        </th>
                    </tr>
                </thead>

                <tbody>

                    <tr
                        v-for="(row, rowIndex) in rows"
                        :key="rowIndex"
                    >

                        <td
                            v-for="column in displayColumns"
                            :key="column"
                        >

                            <slot
                                v-if="hasSlot(column)"
                                :name="column"
                                :row="row"
                                :value="row[column]"
                                :index="rowIndex"
                            />

                            <template v-else>
                                {{ formatValue(row[column]) }}
                            </template>

                        </td>

                    </tr>

                    <tr v-if="rows.length === 0">

                        <td
                            :colspan="displayColumns.length || 1"
                            class="k-table__empty"
                        >
                            No data available.
                        </td>

                    </tr>

                </tbody>

            </table>

        </div>

    </div>

</template>

<style scoped>
@reference "../../style.css";

.k-table-wrapper {
    @apply w-full overflow-hidden rounded-xl border;
    background: var(--color-surface);
    border-color: var(--color-border);
}

.k-table-scroll {
    @apply w-full overflow-x-auto;
}

.k-table {
    @apply w-full border-collapse text-sm;
    color: var(--color-text);
}

.k-table thead {
    background: var(--color-surface-muted);
}

.k-table th {
    @apply px-4 py-3 text-left font-semibold whitespace-nowrap;
    color: var(--color-text);
    border-bottom: 1px solid var(--color-border);
}

.k-table td {
    @apply px-4 py-3;
    border-bottom: 1px solid var(--color-border);
}

.k-table tbody tr:last-child td {
    border-bottom: none;
}

.k-table tbody tr {
    transition:
        background-color 150ms ease,
        box-shadow 150ms ease;
}

.k-table tbody tr:hover {
    background: var(--color-surface-muted);
}

.k-table__empty {
    @apply py-10 text-center;
    color: var(--color-text-muted);
}
</style>