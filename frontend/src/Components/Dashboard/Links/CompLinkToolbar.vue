<script setup lang="ts">
import KButton from '@/Widgets/Actions/KButton.vue';
import { ref } from 'vue';

const input_query = ref("")
void input_query

const emit = defineEmits<{
    search: [query: string]
    filter: []
    refresh: []
    openNew: []
}>()

</script>

<template>
    <div class="w-full flex justify-center items-center">
        <div
            class="
                w-full
                sm:w-fit
                flex flex-col
                sm:flex-row
                items-stretch
                sm:items-center
                gap-2
            "
        >
            <div
                class="
                    w-full sm:w-auto
                    flex flex-row
                    gap-1
                "
            >
                <KButton
                    label="Filter"
                    icon="filter_alt"
                    class="flex-1 sm:flex-none"
                    @click="$emit('filter')"
                />

                <KButton
                    icon="refresh"
                    @click="$emit('refresh')"
                />
                
                <KButton
                    label="New"
                    icon="add"
                    class="flex-1 sm:flex-none"
                    @click="$emit('openNew')"
                />
            </div>
        </div>
    </div>
</template>
