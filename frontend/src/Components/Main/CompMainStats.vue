<script setup lang="ts">
import type { InterfaceStatistics } from '@S/Interfaces'
import KCard from '@W/Layout/KCard.vue'

defineProps<{
    statistics?: InterfaceStatistics
    loading?: boolean
}>()
</script>

<template>
    <section v-if="loading || statistics" class="border-y border-[var(--color-border)] py-8" aria-live="polite">
        <div v-if="loading" class="grid gap-4 sm:grid-cols-4">
            <div v-for="index in 4" :key="index" class="h-24 animate-pulse rounded-xl bg-[var(--color-surface-muted)]" />
        </div>
        <div v-else class="grid gap-4 grid-cols-2 md:grid-cols-4">
            <KCard v-for="item in [
                { label: 'Links shortened', value: statistics?.total_links },
                { label: 'Total visits', value: statistics?.total_visits },
                { label: 'People using KutLync', value: statistics?.total_users },
                { label: 'Successful logins', value: statistics?.total_log_ins },
            ]" :key="item.label" class="!border-0 !bg-transparent !p-0">
                <p class="text-3xl font-black text-[var(--color-text)]">{{ item.value?.toLocaleString() }}</p>
                <p class="mt-1 text-sm text-[var(--color-text-muted)]">{{ item.label }}</p>
            </KCard>
        </div>
    </section>
</template>