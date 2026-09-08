<script setup lang="ts">
import KBadge from '@/Widgets/Feedback/KBadge.vue'
import KButton from '@/Widgets/Actions/KButton.vue'
import KIcon from '@/Widgets/UX/KIcon.vue'
import type { InterfaceLink } from '@/Services/Interfaces'

const props = defineProps<{ link: InterfaceLink }>()
const emit = defineEmits<{ close: [] }>()

const fields = [
    { key: 'link_name', label: 'Name', icon: 'label' },
    { key: 'slug', label: 'Slug', icon: 'link' },
    { key: 'destination_link', label: 'Destination', icon: 'open_in_new' },
    { key: 'link_description', label: 'Description', icon: 'notes' },
    { key: 'visits', label: 'Visits', icon: 'bar_chart' },
    { key: 'max_age_minutes', label: 'Max age', icon: 'schedule' },
    { key: 'created_at', label: 'Created', icon: 'calendar_today' },
    { key: 'updated_at', label: 'Updated', icon: 'update' }
] as const

function value(key: typeof fields[number]['key']) {
    const result = props.link[key]
    if (key === 'max_age_minutes') return result == null ? 'Never' : `${result} minutes`
    if (key === 'created_at' || key === 'updated_at') {
        const date = new Date(String(result))
        return Number.isNaN(date.getTime()) ? 'Unknown' : date.toLocaleString([], { dateStyle: 'medium', timeStyle: 'short' })
    }
    return String(result ?? 'Not provided')
}
</script>

<template>
    <div class="grid gap-3">
        <div class="flex items-center justify-between rounded-lg p-3" style="background: var(--color-accent-soft)">
            <div class="flex items-center gap-3">
                <span class="grid h-10 w-10 place-items-center rounded-full" style="background: var(--color-accent); color: var(--color-on-accent)">
                    <KIcon icon="link" />
                </span>
                <div>
                    <p class="font-semibold">{{ link.link_name }}</p>
                    <p class="text-sm" style="color: var(--color-text-muted)">{{ link.destination_link }}</p>
                </div>
            </div>
            <KBadge :label="link.status" :tone="link.status === 'active' ? 'success' : 'warning'" />
        </div>
        <div class="grid gap-2 sm:grid-cols-2">
            <div v-for="field in fields" :key="field.key" class="rounded-lg border p-3" style="border-color: var(--color-border)">
                <div class="flex items-center gap-2 text-xs font-semibold uppercase tracking-wide" style="color: var(--color-text-muted)">
                    <KIcon :icon="field.icon" />
                    <span>{{ field.label }}</span>
                </div>
                <p class="mt-1 wrap-break-word text-sm" style="color: var(--color-text)">{{ value(field.key) }}</p>
            </div>
        </div>
        <div class="flex justify-end">
            <KButton label="Close" variant="secondary" @click="emit('close')" />
        </div>
    </div>
</template>
