<script setup lang="ts">
withDefaults(defineProps<{
	label?: string;	tone?: 'neutral' | 'success' | 'warning';
}>(), {label: 'Label', tone: 'neutral'});
</script>

<template>
	<span class="k-badge" :class="`k-badge--${tone}`"><span class="k-badge__dot" />{{ label }}</span>
</template>

<style scoped>
@reference "../../style.css";
.k-badge { @apply inline-flex items-center gap-2 rounded-lg px-2.5 py-1 text-xs font-semibold; }
.k-badge__dot { @apply size-1.5 rounded-sm; background: currentColor; }
.k-badge--neutral { background: var(--color-surface-muted); color: var(--color-text-muted); }
.k-badge--success { background: var(--color-success-soft); color: var(--color-success); }
.k-badge--warning { background: var(--color-warning-soft); color: var(--color-warning); }
.k-badge--error { background: var(--color-danger); color: white; }
</style>
