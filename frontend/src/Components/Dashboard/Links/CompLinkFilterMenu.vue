<script setup lang="ts">
import { reactive, computed } from 'vue'
import KButton from '@W/Actions/KButton.vue'
import KSelect from '@W/Forms/KSelect.vue'
import KInput from '@W/Forms/KInput.vue'

interface FilterValues {
    q: string
    ascen: boolean
    sort_by: string
    status: string
    limit: string
}

const props = defineProps<{
    initialFilters?: Partial<FilterValues>
}>()

const emit = defineEmits<{
    apply: [filters: {
        q: string | null
        ascen: boolean
        sort_by: 'id' | 'link_name' | 'destination_link' | 'slug' | 'visits' | 'max_age_minutes' | 'created_at' | 'updated_at' | 'status'
        status: 'active' | 'deleted' | 'expired' | null
        limit: number
    }]
    close: []
    reset: []
}>()

// Initialize form with props or defaults
const form = reactive({
    q: props.initialFilters?.q ?? '',
    ascen: props.initialFilters?.ascen ?? true,
    sort_by: props.initialFilters?.sort_by ?? 'updated_at',
    status: props.initialFilters?.status ?? '',
    limit: props.initialFilters?.limit ?? '-1'
})

// Sort options
const sortOptions = [
    { label: 'ID', value: 'id' },
    { label: 'Link Name', value: 'link_name' },
    { label: 'Destination URL', value: 'destination_link' },
    { label: 'Slug', value: 'slug' },
    { label: 'Visits', value: 'visits' },
    { label: 'Max Age (minutes)', value: 'max_age_minutes' },
    { label: 'Created At', value: 'created_at' },
    { label: 'Updated At', value: 'updated_at' },
    { label: 'Status', value: 'status' }
]

// Status options
const statusOptions = [
    { label: 'All', value: '' },
    { label: 'Active', value: 'active' },
    { label: 'Expired', value: 'expired' },
    { label: 'Deleted', value: 'deleted' }
]

// Limit options
const limitOptions = [
    { label: 'No limit', value: '-1' },
    { label: '10', value: '10' },
    { label: '25', value: '25' },
    { label: '50', value: '50' },
    { label: '100', value: '100' }
]


// Check if any filter is active (for reset button)
const hasActiveFilters = computed(() => {
    return form.q ||
        form.status ||
        form.limit !== '-1' ||
        !form.ascen ||
        form.sort_by !== 'updated_at'
})

const applyFilters = () => {
    // Build the filter object matching the FilterQuery model
    const filters = {
        q: form.q || null,
        ascen: form.ascen,
        sort_by: form.sort_by as any,
        status: (form.status || null) as 'active' | 'deleted' | 'expired' | null,
        limit: Number(form.limit)
    }

    emit('apply', filters)
}

const resetFilters = () => {
    form.q = ''
    form.ascen = true
    form.sort_by = 'updated_at'
    form.status = ''
    form.limit = '-1'
    emit('reset')
}

</script>

<template>
    <div class="absolute right-0 top-full z-50 mt-2 min-w-[320px] max-w-100 rounded-xl border p-4 shadow-lg"
        style="background: var(--color-surface); border-color: var(--color-border)">

        <div class="space-y-3">
            <KInput v-model="form.q" label="Search" placeholder="Search by name, URL, or slug..." icon="search"
                clearable />
            <div class="flex gap-2">
                <KSelect v-model="form.sort_by" label="Sort by" :options="sortOptions" class="flex-1" />
                <KButton :icon="form.ascen ? 'arrow_downward' : 'arrow_upward'" variant="secondary" class="self-end h-10 w-10 px-0"
                    @click="form.ascen = !form.ascen" :title="form.ascen ? 'Ascending' : 'Descending'" />
            </div>
            <KSelect v-model="form.limit" label="Limit" :options="limitOptions" />
            <KSelect v-model="form.status" label="Status" :options="statusOptions" />
        </div>

        <div class="mt-4 flex justify-evenly items-center gap-2">
            <KButton class="w-full" label="Reset" variant="secondary" :disabled="!hasActiveFilters" @click="resetFilters" />
            <KButton class="w-full" label="Cancel" variant="secondary" @click="emit('close')" />
            <KButton class="w-full" label="Apply" icon="check" variant="primary" @click="applyFilters" />
        </div>
    </div>
</template>
