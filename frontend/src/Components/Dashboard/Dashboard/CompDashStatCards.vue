<script setup lang="ts">
import { computed } from 'vue'
import type { InterfaceUserDashboardStats } from '@/Services/Interfaces';
import KIcon from '@/Widgets/UX/KIcon.vue'

const props = defineProps<{
    stats: InterfaceUserDashboardStats
}>()

// Make cards a computed property so it updates when props.stats changes
const cards = computed(() => [
    {
        label: 'Total Active Links',
        value: props.stats.total_links,
        caption: 'Ready to send',
        icon: 'link',
        tone: 'accent'
    },
    {
        label: 'Total Active Visits',
        value: props.stats.total_visits,
        caption: 'Across active links',
        icon: 'trending_up',
        tone: 'success'
    },
    {
        label: 'Expired Links',
        value: props.stats.expired_links,
        caption: 'Need a refresh',
        icon: 'timer_off',
        tone: 'warning'
    },
    {
        label: 'Deleted Links',
        value: props.stats.deleted_links,
        caption: 'Kept out of circulation',
        icon: 'delete_sweep',
        tone: 'danger'
    },
])
</script>

<template>
    <section
        class="grid w-full grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4"
    >
        <article
            v-for="card in cards"
            :key="card.label"
            class="stat-card rounded-xl border p-5"
            style="
                background: var(--color-surface);
                border-color: var(--color-border);
            "
        >
            <div class="flex items-start justify-between"><p class="text-sm" style="color: var(--color-text-muted)">{{ card.label }}</p><span class="stat-icon" :class="`stat-icon--${card.tone}`"><KIcon :icon="card.icon" /></span></div>
            <p
                class="mt-2 text-2xl font-bold"
                style="color: var(--color-text)"
            >
                {{ card.value }}
            </p>
            <p class="mt-2 text-xs" style="color: var(--color-text-muted)">{{ card.caption }}</p>
        </article>
    </section>
</template>

<style scoped>
@reference "../../../style.css";
.stat-card { transition: transform 180ms ease, box-shadow 180ms ease; }
.stat-card:hover { transform: translateY(-3px); box-shadow: 0 12px 24px rgb(23 33 31 / 9%); }
.stat-icon { @apply grid h-10 w-10 place-items-center rounded-xl; }.stat-icon--accent { background: var(--color-accent-soft); color: var(--color-accent); }.stat-icon--success { background: var(--color-success-soft); color: var(--color-success); }.stat-icon--warning { background: var(--color-warning-soft); color: var(--color-warning); }.stat-icon--danger { background: rgb(179 72 72 / 12%); color: var(--color-danger); }
</style>