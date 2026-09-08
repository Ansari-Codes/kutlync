<script setup lang="ts">
import CompDashStatCards from '@C/Dashboard/Dashboard/CompDashStatCards.vue'
import KIcon from '@/Widgets/UX/KIcon.vue'
import { useAuthStore } from '@/Stores/Auth.store'
import type { InterfaceAnalytics, InterfaceUserDashboardStats } from '@/Services/Interfaces';
import { computed, onMounted, onUnmounted, ref } from 'vue';
import { serveUserDashStats } from '@/Services/Dashboard.serve';

const auth = useAuthStore()
const err = ref("")
const analytics = ref<InterfaceAnalytics | null>(null)
const analyticsLoading = ref(true)
const currentTime = ref(new Date())
const stats = ref<InterfaceUserDashboardStats>({
    total_links: 0, total_visits: 0, expired_links: 0, deleted_links: 0,
    recent_links: [], near_expiry_links: []
});

let clockTimer: ReturnType<typeof setInterval> | undefined

const greeting = computed(() => {
    const hour = currentTime.value.getHours()
    if (hour < 12) return 'Good morning'
    if (hour < 18) return 'Good afternoon'
    return 'Good evening'
})

const formattedTime = computed(() => currentTime.value.toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit'
}))

const formattedDate = computed(() => currentTime.value.toLocaleDateString([], {
    weekday: 'long',
    month: 'short',
    day: 'numeric'
}))

onMounted(async () => {
    clockTimer = setInterval(() => { currentTime.value = new Date() }, 1000)
    try {
        stats.value = (await serveUserDashStats()).data
        const { serveAnalytics } = await import('@/Services/Analytics.serve')
        analytics.value = (await serveAnalytics(30)).data
    } catch (error) {
        err.value = String(error)
    } finally {
        analyticsLoading.value = false
    }
})

const statusTotals = computed(() => analytics.value?.status_breakdown ?? [])
const statusTotal = computed(() => statusTotals.value.reduce((sum, item) => sum + item.links, 0) || 1)
const statusPie = computed(() => {
    let cursor = 0
    return statusTotals.value.map(item => {
        const start = cursor
        cursor += (item.links / statusTotal.value) * 100
        return `${item.status === 'active' ? 'var(--color-success)' : item.status === 'expired' ? 'var(--color-warning)' : 'var(--color-danger)'} ${start}% ${cursor}%`
    }).join(', ')
})

function statusClass(status: string) {
    return status === 'active' ? 'status-active' : status === 'expired' ? 'status-expired' : 'status-deleted'
}

function remainingLabel(link: InterfaceAnalytics['near_expiry'][number]) {
    const minutes = link.expiry_minutes ?? 0
    return minutes < 60 ? `${Math.ceil(minutes)}m left` : `${Math.ceil(minutes / 60)}h left`
}

onUnmounted(() => {
    if (clockTimer) clearInterval(clockTimer)
})

</script>

<template>
    <main class="dashboard-home">
        <section class="dashboard-hero">
            <div>
                <p class="dashboard-kicker"><KIcon icon="auto_awesome" /> Link workspace</p>
                <h1>{{ greeting }}, {{ auth.user?.username || 'there' }}</h1>
                <p class="dashboard-subtitle">A clear view of everything your links are doing today.</p>
            </div>
            <div class="dashboard-clock">
                <KIcon icon="schedule" />
                <div><strong>{{ formattedTime }}</strong><span>{{ formattedDate }}</span></div>
            </div>
        </section>

        <CompDashStatCards :stats="stats" />

        <section class="dashboard-actions">
            <div><p class="dashboard-kicker">Quick action</p><h2>Keep your link library moving.</h2></div>
            <div class="dashboard-action-buttons">
                <RouterLink to="/dashboard/link?new=true" class="dashboard-primary"><KIcon icon="add_link" /> Create new link</RouterLink>
                <RouterLink to="/dashboard/links" class="dashboard-secondary"><KIcon icon="arrow_forward" /> Browse links</RouterLink>
            </div>
        </section>

        <section class="dashboard-columns">
            <article class="dashboard-list-panel">
                <div class="panel-heading"><div><p class="dashboard-kicker">Latest activity</p><h2>Recently updated</h2></div><KIcon icon="history" /></div>
                <RouterLink v-for="link in stats.recent_links" :key="link.id" :to="'/dashboard/links?q=' + encodeURIComponent(link.slug)" class="activity-row">
                    <span class="activity-icon"><KIcon icon="link" /></span><span class="activity-copy"><strong>{{ link.link_name }}</strong><small>{{ link.slug }}</small></span><KIcon icon="chevron_right" />
                </RouterLink>
                <p v-if="!stats.recent_links.length" class="empty-state">Your latest links will appear here.</p>
            </article>
            <article class="dashboard-list-panel expiry-panel">
                <div class="panel-heading"><div><p class="dashboard-kicker">Needs attention</p><h2>Near expiry</h2></div><KIcon icon="timer" /></div>
                <RouterLink v-for="link in stats.near_expiry_links" :key="link.id" :to="'/dashboard/links?q=' + encodeURIComponent(link.slug)" class="activity-row">
                    <span class="activity-icon warning-icon"><KIcon icon="hourglass_top" /></span><span class="activity-copy"><strong>{{ link.link_name }}</strong><small>{{ link.max_age_minutes }} minute limit</small></span><KIcon icon="chevron_right" />
                </RouterLink>
                <p v-if="!stats.near_expiry_links.length" class="empty-state">Nothing is expiring in the next five minutes.</p>
            </article>
        </section>

        <section v-if="analytics" class="dashboard-analytics">
            <article class="dashboard-list-panel status-panel">
                <div class="panel-heading"><div><p class="dashboard-kicker">Status health</p><h2>Link distribution</h2></div><KIcon icon="pie_chart" /></div>
                <div class="status-summary">
                    <div class="status-pie" :style="{ background: `conic-gradient(${statusPie})` }"><strong>{{ analytics.totals.total_links }}</strong><small>links</small></div>
                    <div class="status-legend">
                        <div v-for="item in statusTotals" :key="item.status" class="status-legend-row">
                            <span class="status-dot" :class="statusClass(item.status)" />
                            <span>{{ item.status }}</span><strong>{{ item.links }}</strong><small>{{ item.visits }} visits</small>
                        </div>
                    </div>
                </div>
            </article>

            <article class="dashboard-list-panel">
                <div class="panel-heading"><div><p class="dashboard-kicker">Leaders</p><h2>Top links by visits</h2></div><KIcon icon="trending_up" /></div>
                <div v-if="analytics.top_links.length" class="insight-list">
                    <div v-for="(link, index) in analytics.top_links" :key="link.id" class="insight-row">
                        <span class="rank-badge">{{ index + 1 }}</span><div><strong>{{ link.link_name || link.slug }}</strong><small>{{ link.slug }}</small></div><b>{{ link.visits }}</b>
                    </div>
                </div>
                <p v-else class="empty-state">Visits will appear as your links are shared.</p>
            </article>

            <article class="dashboard-list-panel">
                <div class="panel-heading"><div><p class="dashboard-kicker">Security</p><h2>Protected traffic</h2></div><KIcon icon="lock" /></div>
                <div class="security-total"><strong>{{ analytics.totals.secured_links }}</strong><span>secured active or expired links</span><b>{{ analytics.totals.secured_visits }} visits</b></div>
                <p class="status-note">Secured links keep access codes in place while still contributing to total traffic.</p>
            </article>

            <article class="dashboard-list-panel attention-panel">
                <div class="panel-heading"><div><p class="dashboard-kicker">Needs attention</p><h2>Status changes soon</h2></div><KIcon icon="notifications_active" /></div>
                <div v-if="analytics.near_expiry.length || analytics.near_deleted.length || analytics.expired_near_deleted.length" class="insight-list">
                    <div v-for="link in analytics.near_expiry" :key="`expiry-${link.id}`" class="insight-row"><span class="attention-icon status-expired"><KIcon icon="timer" /></span><div><strong>{{ link.link_name || link.slug }}</strong><small>Expires {{ remainingLabel(link) }}</small></div><KIcon icon="chevron_right" /></div>
                    <div v-for="link in [...analytics.near_deleted, ...analytics.expired_near_deleted]" :key="`delete-${link.id}`" class="insight-row"><span class="attention-icon status-deleted"><KIcon icon="delete_sweep" /></span><div><strong>{{ link.link_name || link.slug }}</strong><small>{{ Math.ceil(link.deletion_hours ?? 0) }}h until deletion</small></div><KIcon icon="chevron_right" /></div>
                </div>
                <p v-else class="empty-state">No links are close to changing status.</p>
            </article>
        </section>
        <section v-else-if="analyticsLoading" class="dashboard-loading"><KIcon icon="progress_activity" /> Loading deeper insights...</section>
        <p v-if="err" class="dashboard-error">{{ err }}</p>
    </main>
</template>

<style scoped>
@reference "../../style.css";
.dashboard-home { @apply min-h-full p-4 sm:p-6; background: var(--color-page); color: var(--color-text); }
.dashboard-hero { @apply mb-6 flex flex-col justify-between gap-5 rounded-2xl p-6 sm:flex-row sm:items-center; background: linear-gradient(120deg, var(--color-accent-strong), var(--color-accent)); color: var(--color-on-accent); }
.dashboard-hero h1 { @apply mt-2 text-3xl font-bold tracking-tight sm:text-4xl; }
.dashboard-subtitle { @apply mt-2 max-w-lg text-sm opacity-80; }
.dashboard-kicker { @apply flex items-center gap-2 text-xs font-bold uppercase tracking-widest; opacity: .72; }
.dashboard-clock { @apply flex items-center gap-3 rounded-xl px-4 py-3; background: rgb(255 255 255 / 14%); }
.dashboard-clock > span { @apply text-2xl; }.dashboard-clock strong { @apply block text-2xl; }.dashboard-clock div span { @apply block text-xs opacity-75; }
.dashboard-actions { @apply my-6 flex flex-col justify-between gap-4 rounded-xl border p-5 sm:flex-row sm:items-center; background: var(--color-surface); border-color: var(--color-border); }
.dashboard-actions h2, .dashboard-list-panel h2 { @apply mt-1 text-lg font-bold; }
.dashboard-action-buttons { @apply flex flex-wrap gap-2; }.dashboard-primary, .dashboard-secondary { @apply inline-flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-semibold; }
.dashboard-primary { background: var(--color-accent); color: var(--color-on-accent); }.dashboard-secondary { background: var(--color-surface-muted); color: var(--color-text); }
.dashboard-columns { @apply grid gap-4 lg:grid-cols-2; }.dashboard-list-panel { @apply rounded-xl border p-5; background: var(--color-surface); border-color: var(--color-border); }
.dashboard-analytics { @apply mt-6 grid gap-4 xl:grid-cols-2; }.status-summary { @apply flex flex-col items-center gap-6 sm:flex-row sm:justify-center; }.status-pie { @apply grid h-36 w-36 shrink-0 place-content-center rounded-full; }.status-pie::after { content: ''; @apply col-start-1 row-start-1 h-24 w-24 rounded-full; background: var(--color-surface); }.status-pie strong, .status-pie small { @apply z-10 col-start-1 row-start-1 text-center; }.status-pie strong { @apply mt-5 text-2xl; }.status-pie small { @apply mt-14 text-xs; color: var(--color-text-muted); }.status-legend { @apply grid w-full gap-3; }.status-legend-row { @apply grid grid-cols-[auto_1fr_auto_auto] items-center gap-2 text-sm; }.status-legend-row small { color: var(--color-text-muted); }.status-dot { @apply h-2.5 w-2.5 rounded-full; }.status-active { background: var(--color-success); color: var(--color-success); }.status-expired { background: var(--color-warning); color: var(--color-warning); }.status-deleted { background: var(--color-danger); color: var(--color-danger); }.insight-list { @apply grid gap-2; }.insight-row { @apply flex items-center gap-3 rounded-lg border p-3; border-color: var(--color-border); }.insight-row > div { @apply min-w-0 flex-1; }.insight-row strong, .insight-row small { @apply block truncate; }.insight-row small { @apply mt-0.5 text-xs; color: var(--color-text-muted); }.rank-badge, .attention-icon { @apply grid h-8 w-8 shrink-0 place-items-center rounded-lg text-sm font-bold; background: var(--color-accent-soft); color: var(--color-accent); }.security-total { @apply grid gap-1 rounded-xl p-5; background: var(--color-accent-soft); }.security-total strong { @apply text-4xl; }.security-total span, .security-total b, .status-note { @apply text-sm; color: var(--color-text-muted); }.status-note { @apply mt-4; }.attention-icon { color: inherit; background: color-mix(in srgb, currentColor 14%, transparent); }.dashboard-loading { @apply mt-6 flex items-center justify-center gap-2 rounded-xl border p-8 text-sm; border-color: var(--color-border); color: var(--color-text-muted); }
.panel-heading { @apply mb-4 flex items-start justify-between; }.panel-heading > span { @apply text-2xl; color: var(--color-accent); }
.activity-row { @apply flex items-center gap-3 border-t py-3; border-color: var(--color-border); }.activity-icon { @apply grid h-9 w-9 shrink-0 place-items-center rounded-lg; background: var(--color-accent-soft); color: var(--color-accent); }.warning-icon { background: var(--color-warning-soft); color: var(--color-warning); }
.activity-copy { @apply min-w-0 flex-1; }.activity-copy strong, .activity-copy small { @apply block truncate; }.activity-copy small { @apply mt-0.5 text-xs; color: var(--color-text-muted); }.activity-row > span:last-child { color: var(--color-text-muted); }.empty-state { @apply py-5 text-sm; color: var(--color-text-muted); }.dashboard-error { @apply mt-4 text-sm; color: var(--color-danger); }
</style>