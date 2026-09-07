<script lang="ts" setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import CompDashPanel from '@/Components/Dashboard/CompDashPanel.vue'
import CompLinkToolbar from '@/Components/Dashboard/Links/CompLinkToolbar.vue'
import CompLinkFilterMenu from '@/Components/Dashboard/Links/CompLinkFilterMenu.vue'
import CompLinkViewer from '@/Components/Dashboard/Links/CompLinkViewer.vue'
import CompTrashActionsMenu from '@/Components/Dashboard/Links/CompTrashActionsMenu.vue'
import KDataTable from '@/Widgets/Data/KDataTable.vue'
import KButton from '@/Widgets/Actions/KButton.vue'
import KDialog from '@/Widgets/Layout/KDialog.vue'
import KPanel from '@/Widgets/Layout/KPanel.vue'
import KIcon from '@/Widgets/UX/KIcon.vue'
import { serveLinks, servePermanentDeleteLink, serveRestoreLink, serveViewLink } from '@/Services/Links.serve'
import type { InterfaceLink, InterfaceLinkFilters } from '@/Services/Interfaces'
import { useNotify } from '@/Composables/useNotify'

const route = useRoute()
const router = useRouter()
const { notify } = useNotify()
const links = ref<InterfaceLink[]>([])
const now = ref(Date.now())
const filter_open = ref(false)
const isLoading = ref(false)
const selectedActionLinkID = ref<number | string | null>(null)
const actionMenuPosition = ref({ top: 0, left: 0 })
const viewingLink = ref<InterfaceLink | null>(null)
const pendingDelete = ref<InterfaceLink | null>(null)
let timer: ReturnType<typeof setInterval> | undefined

const currentFilters = ref<InterfaceLinkFilters>({
	q: String(route.query.q ?? ''), ascen: route.query.ascen !== 'false',
	sort_by: (route.query.sort_by as InterfaceLinkFilters['sort_by']) || 'updated_at',
	status: 'deleted', limit: route.query.limit ? Number(route.query.limit) : -1
})

function timeLeft(updatedAt: string) {
	const remaining = new Date(updatedAt).getTime() + 5 * 86400000 - now.value
	if (remaining <= 0) return null
	return `${Math.floor(remaining / 86400000)}d ${Math.floor((remaining % 86400000) / 3600000)}h`
}

const displayLinks = computed(() => links.value
	.filter(link => link.status === 'deleted' && timeLeft(link.updated_at))
	.map(link => ({ id: link.id, link_name: link.link_name, target: link.destination_link,
		slug: link.slug, time_left: timeLeft(link.updated_at), deleted_at: link.updated_at })))

function updateUrl() {
	const query: Record<string, string> = {}
	if (currentFilters.value.q) query.q = currentFilters.value.q
	if (currentFilters.value.ascen === false) query.ascen = 'false'
	if (currentFilters.value.sort_by !== 'updated_at') query.sort_by = currentFilters.value.sort_by ?? 'updated_at'
	if (currentFilters.value.limit && currentFilters.value.limit > 0) query.limit = String(currentFilters.value.limit)
	router.replace({ query })
}

function applyFilters(filters: InterfaceLinkFilters) {
	currentFilters.value = { ...filters, status: 'deleted' }
	filter_open.value = false
	updateUrl()
	loadLinks()
}

function search(query: string) {
	currentFilters.value.q = query
	updateUrl()
	loadLinks()
}

function getRowId(row: Record<string, unknown>) { return Number(row.id) }

function openActions(id: number | string, event: MouseEvent) {
	const rect = (event.currentTarget as HTMLElement).getBoundingClientRect()
	actionMenuPosition.value = { top: rect.bottom + 4, left: rect.left }
	selectedActionLinkID.value = selectedActionLinkID.value === id ? null : id
}

function closeActions() { selectedActionLinkID.value = null }

async function viewLink(id: number | string) {
	closeActions()
	try { viewingLink.value = (await serveViewLink(String(id))).data }
	catch (error) { notify(String(error), 'error') }
}

async function restoreLink(id: number | string) {
	closeActions()
	try {
		const response = await serveRestoreLink(String(id))
		links.value = links.value.filter(link => link.id !== id)
		notify(response.message, 'success')
	} catch (error) { notify(String(error), 'error') }
}

function requestPermanentDelete(id: number | string) {
	closeActions()
	pendingDelete.value = links.value.find(link => link.id === id) ?? null
}

async function permanentlyDelete() {
	if (!pendingDelete.value) return
	const id = pendingDelete.value.id
	try {
		await servePermanentDeleteLink(String(id))
		links.value = links.value.filter(link => link.id !== id)
		notify('Link permanently deleted', 'success')
	} catch (error) { notify(String(error), 'error') }
	pendingDelete.value = null
}

async function removeExpiredRows() {
	const expired = links.value.filter(link => !timeLeft(link.updated_at))
	for (const link of expired) {
		try { await servePermanentDeleteLink(String(link.id)) } catch { }
	}
	if (expired.length) links.value = links.value.filter(link => timeLeft(link.updated_at))
}

async function loadLinks() {
	try {
		isLoading.value = true
		const response = await serveLinks({ ...currentFilters.value, status: 'deleted' })
		links.value = response.data.filter(link => link.status === 'deleted')
		await removeExpiredRows()
	} catch (error) { notify(String(error), 'error') }
	finally { isLoading.value = false }
}

watch(() => route.query, () => {
	currentFilters.value = { ...currentFilters.value, q: String(route.query.q ?? ''),
		ascen: route.query.ascen !== 'false', sort_by: (route.query.sort_by as InterfaceLinkFilters['sort_by']) || 'updated_at',
		limit: route.query.limit ? Number(route.query.limit) : -1, status: 'deleted' }
	loadLinks()
}, { deep: true })

onMounted(async () => {
	timer = setInterval(async () => { now.value = Date.now(); await removeExpiredRows() }, 60000)
	await loadLinks()
})

onUnmounted(() => { if (timer) clearInterval(timer) })
</script>

<template>
	<CompDashPanel title="Trash box" tagline="Deleted links are kept for 5 days">
		<template #header>
			<div class="relative">
				<CompLinkToolbar class="mb-2" @search="search" @filter="filter_open = !filter_open" @refresh="loadLinks" @open-new="router.push({ name: 'new-link', query: { new: 'true' } })" />
				<CompLinkFilterMenu v-if="filter_open" mode="trash" :initial-filters="{ q: currentFilters.q ?? '', ascen: currentFilters.ascen, sort_by: currentFilters.sort_by, limit: String(currentFilters.limit ?? -1) }" @apply="applyFilters" @close="filter_open = false" @reset="currentFilters = { q: '', ascen: true, sort_by: 'updated_at', status: 'deleted', limit: -1 }; updateUrl(); loadLinks()" />
			</div>
		</template>

		<KDataTable :rows="displayLinks" :columns="['actions', 'id', 'link_name', 'target', 'slug', 'time_left', 'deleted_at']" :slot-columns="['actions']" :loading="isLoading">
			<template #actions="{ row }">
				<div class="relative flex items-center">
					<KButton icon="more_vert" variant="quiet" @click="openActions(getRowId(row), $event)" />
					<div v-if="selectedActionLinkID === row.id" class="fixed z-50" :style="{ top: `${actionMenuPosition.top}px`, left: `${actionMenuPosition.left}px` }">
						<CompTrashActionsMenu @view="viewLink(getRowId(row))" @restore="restoreLink(getRowId(row))" @permanent-delete="requestPermanentDelete(getRowId(row))" @close="closeActions" />
					</div>
				</div>
			</template>
		</KDataTable>

		<KDialog :model-value="Boolean(viewingLink)" mode="elevated" title="Link details" @update:model-value="viewingLink = null" @close="viewingLink = null">
			<CompLinkViewer v-if="viewingLink" :link="viewingLink" @close="viewingLink = null" />
		</KDialog>

		<KDialog :model-value="Boolean(pendingDelete)" mode="elevated" title="Delete permanently" @update:model-value="pendingDelete = null" @close="pendingDelete = null">
			<KPanel><div class="grid gap-4">
				<div class="flex items-center gap-3 rounded-lg p-3" style="background: var(--color-danger); color: white"><KIcon icon="warning" /><p>Delete this link permanently? This cannot be undone.</p></div>
				<p class="text-sm">{{ pendingDelete?.link_name }}</p>
				<div class="flex justify-end gap-2"><KButton label="No" variant="secondary" @click="pendingDelete = null" /><KButton label="Yes, delete" icon="delete_forever" variant="danger" @click="permanentlyDelete" /></div>
			</div></KPanel>
		</KDialog>
	</CompDashPanel>
</template>