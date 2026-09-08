<script lang="ts" setup>
import {
    computed,
    onMounted,
    onUnmounted,
    ref,
    watch
} from 'vue'
import { useRoute, useRouter } from 'vue-router'

import CompDashPanel from '@/Components/Dashboard/CompDashPanel.vue'
import CompLinkToolbar from '@C/Dashboard/Links/CompLinkToolbar.vue'
import CompLinkAddForm from '@/Components/Dashboard/Links/CompLinkAddForm.vue'
import CompLinkActionsMenu from '@/Components/Dashboard/Links/CompLinkActionsMenu.vue'
import CompLinkFilterMenu from '@/Components/Dashboard/Links/CompLinkFilterMenu.vue'
import CompLinkViewer from '@/Components/Dashboard/Links/CompLinkViewer.vue'

import KDataTable from '@/Widgets/Data/KDataTable.vue'
import KBadge from '@/Widgets/Feedback/KBadge.vue'
import KButton from '@/Widgets/Actions/KButton.vue'
import KDialog from '@/Widgets/Layout/KDialog.vue'

import {
    serveAddLink,
    serveDeleteLink,
    serveEditLink,
    serveLinks,
    serveViewLink
} from '@/Services/Links.serve'

import type {
    InterfaceLink,
    InterfaceLinkInput,
    InterfaceLinkFilters
} from '@/Services/Interfaces'

import { useNotify } from '@/Composables/useNotify'
import { getShareableLink } from '@/Composables/useLink'

const { notify } = useNotify()
const route = useRoute()
const router = useRouter()

const links = ref<InterfaceLink[]>([])
const add_edit_form_open = ref(route.query.new === 'true')
const add_edit_form_mode = ref<"add" | "edit">("add")

const selectedActionLinkID = ref<number | string | null>(null)
const editingLinkID = ref<number | string | null>(null)
const viewingLink = ref<InterfaceLink | null>(null)
const actionMenuPosition = ref({
    top: 0,
    left: 0
})

const filter_open = ref(false)
const isLoading = ref(false)
const isSubmitting = ref(false)

// Initialize filters from URL query params
const currentFilters = ref<InterfaceLinkFilters>({
    q: route.query.q as string || '',
    ascen: route.query.ascen !== 'false',
    sort_by: (route.query.sort_by as InterfaceLinkFilters['sort_by']) || 'updated_at',
    status: (route.query.status as InterfaceLinkFilters['status']) || null,
    limit: route.query.limit ? Number(route.query.limit) : -1
})

const now = ref(Date.now())
let ageTimer: ReturnType<typeof setInterval> | undefined

const displayLinks = computed(() => {
    return links.value.filter(link => link.status !== 'deleted').map(link => ({
        id: link.id,
        link_name: link.link_name,
        link_target: link.destination_link,
        slug: link.slug,
        visits: link.visits,
        age_left: getAgeLeft(link.created_at, link.max_age_minutes),
        created_at: formatDate(link.created_at),
        updated_at: formatDate(link.updated_at),
        status: link.status,
    }))
})

function getAgeLeft(created_at: string, max_age_minutes?: number | null): string {
    if (max_age_minutes === null || max_age_minutes === undefined) {
        return 'Never'
    }

    const created = new Date(created_at).getTime()
    if (Number.isNaN(created)) return 'Unknown'
    const expiry = created + max_age_minutes * 60000
    const difference = expiry - now.value

    if (difference <= 0) {
        return 'Expired'
    }

    const minutes = Math.floor(difference / 60000)

    if (minutes < 60) {
        return `${minutes}m`
    }

    const hours = Math.floor(minutes / 60)

    if (hours < 24) {
        return `${hours}h ${minutes % 60}m`
    }

    const days = Math.floor(hours / 24)
    return `${days}d ${hours % 24}h`
}

function formatDate(value: string) {
    const date = new Date(value)
    return Number.isNaN(date.getTime()) ? 'Unknown' : date.toLocaleString([], { dateStyle: 'medium', timeStyle: 'short' })
}

function updateUrlWithFilters() {
    const query: Record<string, string> = {}

    // Build query params from currentFilters
    const filters = currentFilters.value

    if (filters.q) query.q = filters.q
    if (filters.ascen !== undefined && filters.ascen !== true) query.ascen = 'false'
    if (filters.sort_by && filters.sort_by !== 'updated_at') query.sort_by = filters.sort_by
    if (filters.status) query.status = filters.status
    if (filters.limit && filters.limit > 0) query.limit = String(filters.limit)

    router.replace({ query })
}

// FIXED: applyFilters now correctly uses q from the filter menu
function applyFilters(filters: any) {
    // Convert the filter menu output to our LinkFilters format
    currentFilters.value = {
        q: filters.q || '',  // Changed from filters.query to filters.q
        ascen: filters.ascen,
        sort_by: filters.sort_by,
        status: filters.status as InterfaceLinkFilters['status'],
        limit: filters.limit || -1
    }

    filter_open.value = false
    updateUrlWithFilters()
    loadLinks()
}

function search(query: string) {
    currentFilters.value.q = query
    updateUrlWithFilters()
    loadLinks()
}

function toggleFilter() {
    filter_open.value = !filter_open.value
}

function refreshLinks() {
    loadLinks()
}

function openNewLink() {
    add_edit_form_open.value = true
    router.push({ name: 'new-link', query: { new: 'true' } })
}

function closeForm() {
    add_edit_form_open.value = false
    if (route.query.new) {
        const query = { ...route.query }
        delete query.new
        router.replace({ query })
    }
}

const selectedLink = computed(() =>
    links.value.find(link => link.id === editingLinkID.value)
)

async function handleAddEditFormSubmit(data: InterfaceLinkInput) {
    isSubmitting.value = true
    try {
        let response
        if (add_edit_form_mode.value === 'add') {
            response = await serveAddLink(data)
        } else {
            if (editingLinkID.value === null) return
            response = await serveEditLink(String(editingLinkID.value), data)
        }
        if (add_edit_form_mode.value === 'add') {
            links.value.unshift(response.data)
        } else {
            const index = links.value.findIndex(link => link.id === response.data.id)
            if (index !== -1) links.value[index] = response.data
        }

        notify(response.message, 'success')
        add_edit_form_open.value = false
        selectedActionLinkID.value = null
        editingLinkID.value = null
        if (route.query.new) {
            const query = { ...route.query }
            delete query.new
            router.replace({ query })
        }
    } catch (e) {
        notify(String(e), 'error')
    } finally {
        isSubmitting.value = false
    }
}

function openActions(id: number | string, event: MouseEvent) {
    const trigger = event.currentTarget as HTMLElement
    const triggerRect = trigger.getBoundingClientRect()

    actionMenuPosition.value = {
        top: triggerRect.bottom + 4,
        left: triggerRect.left
    }

    if (selectedActionLinkID.value === id) {
        selectedActionLinkID.value = null
        return
    }

    selectedActionLinkID.value = id
}

function closeActions() {
    selectedActionLinkID.value = null
}

function handleEdit(id: number | string) {
    add_edit_form_mode.value = 'edit'
    editingLinkID.value = id
    add_edit_form_open.value = true
    closeActions()
}

async function handleView(id: number | string) {
    closeActions()
    try {
        viewingLink.value = (await serveViewLink(String(id))).data
    } catch (error) {
        notify(String(error), 'error')
    }
}

function getRowId(row: Record<string, unknown>) {
    return Number(row.id)
}

async function handleCopyLink(id: number | string) {
    const link = links.value.find(link => link.id === id)
    if (!link) {
        notify('Link not found', 'error')
        return
    }
    try {
        await navigator.clipboard.writeText(getShareableLink(link.slug))
        notify('Link copied to clipboard', 'success')
        closeActions()
    } catch {
        notify('Failed to copy link', 'error')
    }
}
async function handleDelete(id: number | string) {
    try {
        await serveDeleteLink(String(id))
        links.value = links.value.filter(item => item.id !== id)
        notify('Link deleted successfully', 'success')
    } catch (error) {
        notify(String(error), 'error')
    }
    closeActions()
}

async function loadLinks() {
    try {
        isLoading.value = true
        const filters: InterfaceLinkFilters = {
            ...currentFilters.value,
            status: currentFilters.value.status === 'deleted' ? null : currentFilters.value.status
        }
        const response = await serveLinks(filters)
        links.value = response.data
    } catch (e) {
        notify(String(e), 'error')
    } finally {
        isLoading.value = false
    }
}

watch(() => route.query, () => {
    const newFilters: InterfaceLinkFilters = {
        q: route.query.q as string || '',
        ascen: route.query.ascen !== 'false',
        sort_by: (route.query.sort_by as InterfaceLinkFilters['sort_by']) || 'updated_at',
        status: (route.query.status as InterfaceLinkFilters['status']) || null,
        limit: route.query.limit ? Number(route.query.limit) : -1
    }

    if (JSON.stringify(newFilters) !== JSON.stringify(currentFilters.value)) {
        currentFilters.value = newFilters
        loadLinks()
    }
}, { deep: true })

onMounted(async () => {
    if (route.query.new === 'true') add_edit_form_open.value = true

    ageTimer = setInterval(() => {
        now.value = Date.now()
    }, 60000)

    await loadLinks()
})

onUnmounted(() => {
    if (ageTimer) {
        clearInterval(ageTimer)
    }
})
</script>

<template>
    <CompDashPanel title="Links" tagline="Manage your links">
        <template #header>
            <div class="relative">
                <CompLinkToolbar class="mb-2" @open-new="openNewLink" @refresh="refreshLinks" @search="search"
                    @filter="toggleFilter" />
                <CompLinkFilterMenu v-if="filter_open" mode="links" :initial-filters="{
                    q: currentFilters.q || '',
                    ascen: currentFilters.ascen,
                    sort_by: currentFilters.sort_by,
                    status: currentFilters.status || '',
                    limit: String(currentFilters.limit || -1)
                }" @apply="applyFilters" @close="filter_open = false" @reset="() => {
                        currentFilters = {
                            q: '',
                            ascen: true,
                            sort_by: 'updated_at',
                            status: null,
                            limit: -1
                        }
                        updateUrlWithFilters()
                        loadLinks()
                    }" />
            </div>
        </template>

        <KDialog v-model="add_edit_form_open" mode="elevated"
            :title="add_edit_form_mode === 'edit' ? 'Edit link' : 'Create link'" @close="closeForm">
            <CompLinkAddForm :mode="add_edit_form_mode" :link="selectedLink" :loading="isSubmitting" @handle-new="handleAddEditFormSubmit"
                @close-form="closeForm" />
        </KDialog>

        <KDialog :model-value="Boolean(viewingLink)" mode="elevated" title="Link details"
            @update:model-value="viewingLink = null" @close="viewingLink = null">
            <CompLinkViewer v-if="viewingLink" :link="viewingLink" @close="viewingLink = null" />
        </KDialog>

        <KDataTable :rows="displayLinks" :columns="[
            'actions',
            'link_name',
            'link_target',
            'slug',
            'visits',
            'age_left',
            'created_at',
            'updated_at',
            'status'
        ]" :slot-columns="[
                'actions',
                'status'
            ]" :loading="isLoading">
            <template #actions="{ row }">
                <div class="relative flex items-center">
                    <KButton icon="more_vert" variant="quiet" @click="openActions(getRowId(row), $event)" />

                    <div v-if="selectedActionLinkID === row.id" class="fixed z-50" :style="{
                        top: `${actionMenuPosition.top}px`,
                        left: `${actionMenuPosition.left}px`
                    }">
                        <CompLinkActionsMenu @close="selectedActionLinkID = null" @view="handleView(getRowId(row))"
                            @edit="handleEdit(getRowId(row))" @copy_link="handleCopyLink(getRowId(row))"
                            @delete="handleDelete(getRowId(row))" />
                    </div>
                </div>
            </template>

            <template #status="{ value }">
                <KBadge :label="String(value)" :tone="value === 'active'
                    ? 'success'
                    : value === 'expired'
                        ? 'neutral'
                        : 'warning'
                    " />
            </template>
        </KDataTable>
    </CompDashPanel>
</template>