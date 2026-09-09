<script setup lang="ts">
import KButton from '@W/Actions/KButton.vue'
import KLink from '@W/Actions/KLink.vue'
const origin = window.location.origin
</script>

<template>
    <section class="grid items-center gap-12 pb-20 pt-12 lg:grid-cols-[1.1fr_0.9fr] lg:pb-28 lg:pt-20">
        <div class="kutlync-reveal max-w-2xl">
            <p class="mb-5 flex items-center gap-2 text-sm font-bold uppercase tracking-[0.18em] text-[var(--color-accent)]">
                <span class="h-2 w-2 rounded-full bg-[var(--color-accent)]" />
                Links, made lighter
            </p>
            <h1 class="max-w-2xl text-5xl font-black leading-[0.98] tracking-tight text-[var(--color-text)] sm:text-7xl">
                One short link.
                <span class="text-[var(--color-accent)]">Everywhere.</span>
            </h1>
            <p class="mt-7 max-w-xl text-lg leading-8 text-[var(--color-text-muted)] sm:text-xl">
                KutLync turns long, forgettable URLs into clean links you can share, understand, and grow with.
            </p>
            <div class="mt-9 flex flex-wrap items-center gap-4">
                <KButton label="Create your first link" icon="arrow_forward" icon-position="right" @click="$router.push('/auth/signup')" />
                <KLink to="/documentation" class="gap-2 no-underline hover:no-underline">
                    See how it works
                    <span aria-hidden="true">&#8594;</span>
                </KLink>
            </div>
        </div>

        <div class="kutlync-reveal relative [animation-delay:150ms]" aria-label="Link preview">
            <div class="absolute -inset-3 rounded-[2rem] bg-[var(--color-accent-soft)] opacity-70" />
            <div class="relative rounded-2xl border border-[var(--color-border)] bg-[var(--color-surface)] p-2 shadow-[0_24px_60px_rgba(21,122,110,0.12)] sm:p-7">
                <div class="flex items-center justify-between border-b border-[var(--color-border)] pb-5">
                    <div class="flex items-center gap-3">
                        <span class="grid h-10 w-10 place-items-center rounded-xl bg-[var(--color-accent-soft)] text-[var(--color-accent)]">&#8599;</span>
                        <div>
                            <p class="text-sm font-bold text-[var(--color-text)]">Campaign launch</p>
                            <p class="text-xs text-[var(--color-text-muted)]">{{ origin }}/s/launch</p>
                        </div>
                    </div>
                    <span class="rounded-full bg-[var(--color-success-soft)] px-3 py-1 text-xs font-bold text-[var(--color-success)]">Active</span>
                </div>
                <div class="grid grid-cols-3 gap-3 pt-6">
                    <div v-for="item in [{ label: 'Visits', value: '2,481' }, { label: 'Created', value: 'Today' }, { label: 'Status', value: 'Live' }]" :key="item.label" class="rounded-xl bg-[var(--color-surface-muted)] p-3">
                        <p class="text-xs text-[var(--color-text-muted)]">{{ item.label }}</p>
                        <p class="mt-2 text-lg font-black text-[var(--color-text)]">{{ item.value }}</p>
                    </div>
                </div>
                <div class="mt-5 flex items-center justify-between rounded-xl border border-[var(--color-border)] px-4 py-3">
                    <span class="truncate text-sm text-[var(--color-text-muted)]">https://your-site.com/summer-launch</span>
                    <span class="ml-3 text-[var(--color-accent)]">&#128203;</span>
                </div>
            </div>
        </div>
    </section>
</template>