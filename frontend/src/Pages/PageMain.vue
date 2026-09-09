<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { serveStatistics } from '@S/Analytics.serve'
import type { InterfaceStatistics } from '@S/Interfaces'
import CompMainHeader from '@C/Main/CompMainHeader.vue'
import CompMainHero from '@C/Main/CompMainHero.vue'
import CompMainStats from '@C/Main/CompMainStats.vue'
import CompMainFeatures from '@C/Main/CompMainFeatures.vue'
import CompMainCta from '@C/Main/CompMainCta.vue'

const statistics = ref<InterfaceStatistics>()
const loadingStats = ref(true)

onMounted(async () => {
    try {
        const response = await serveStatistics()
        if (response.success) statistics.value = response.data
    } catch {
        statistics.value = undefined
    } finally {
        loadingStats.value = false
    }
})
</script>

<template>
    <main class="min-h-screen overflow-hidden bg-[var(--color-page)]">
        <div class="mx-auto max-w-7xl px-5 sm:px-8">
            <CompMainHeader />
            <CompMainHero />
            <CompMainStats :statistics="statistics" :loading="loadingStats" />
            <CompMainFeatures />
            <CompMainCta />
        </div>
    </main>
</template>