<script setup lang="ts">
import KButton from '@W/Actions/KButton.vue'
import KLink from '@W/Actions/KLink.vue'
</script>

<template>
    <section class="mb-10 overflow-hidden rounded-2xl bg-[var(--color-accent)] px-6 py-12 text-[var(--color-on-accent)] sm:px-12 sm:py-16">
        <div class="flex flex-col items-start justify-between gap-8 md:flex-row md:items-center">
            <div class="max-w-2xl">
                <p class="text-sm font-bold uppercase tracking-[0.18em] opacity-75">Ready when you are</p>
                <h2 class="mt-3 text-3xl font-black tracking-tight sm:text-4xl">Make your next link the one people remember.</h2>
            </div>
            <KButton variant="secondary" label="Get started free" icon="arrow_forward" icon-position="right" @click="$router.push('/auth/signup')" />
        </div>
        <div class="mt-10 flex flex-wrap gap-x-6 gap-y-3 border-t border-white/20 pt-5 text-sm">
            <KLink href="https://github.com/Ansari-Codes/kutlync" target="_blank" rel="noopener noreferrer" class="!text-[var(--color-on-accent)]">View on GitHub</KLink>
        </div>
    </section>
</template>