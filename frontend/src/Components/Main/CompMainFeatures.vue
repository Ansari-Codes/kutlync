<script setup lang="ts">
const features = [
    { icon: '01', title: 'Share with clarity', text: 'Give every destination a memorable name that feels right in a message, campaign, or bio.' },
    { icon: '02', title: 'Understand the journey', text: 'See how your links perform with useful analytics that keep the signal easy to find.' },
    { icon: '03', title: 'Stay in control', text: 'Create, edit, secure, and retire links from one calm, focused workspace.' },
]
</script>

<template>
    <section class="py-20 sm:py-28">
        <div class="max-w-xl">
            <p class="text-sm font-bold uppercase tracking-[0.18em] text-[var(--color-accent)]">Built for momentum</p>
            <h2 class="mt-4 text-3xl font-black tracking-tight text-[var(--color-text)] sm:text-5xl">Your links should work as hard as you do.</h2>
        </div>
        <div class="mt-12 grid gap-5 md:grid-cols-3">
            <article v-for="feature in features" :key="feature.icon" class="rounded-2xl border border-[var(--color-border)] bg-[var(--color-surface)] p-6 transition-transform duration-200 hover:-translate-y-1">
                <span class="text-sm font-black text-[var(--color-accent)]">{{ feature.icon }}</span>
                <h3 class="mt-12 text-xl font-bold text-[var(--color-text)]">{{ feature.title }}</h3>
                <p class="mt-3 leading-7 text-[var(--color-text-muted)]">{{ feature.text }}</p>
            </article>
        </div>
    </section>
</template>