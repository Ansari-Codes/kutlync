<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import CompDashLayout from '@C/Dashboard/CompDashLayout.vue'
import CompDashSidebar from '@/Components/Dashboard/CompDashSidebar.vue'

const route = useRoute()

const currentTabName = computed(() => {
    return route.name
})
</script>

<template>
    <CompDashLayout>
        <template #sidebar>
            <CompDashSidebar :current_tab="currentTabName?.toString().toLowerCase()" />
        </template>
        <template #content>
            <RouterView />
        </template>
    </CompDashLayout>
</template>
