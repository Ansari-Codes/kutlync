<script setup lang="ts">
defineProps<{title?: string; eyebrow?: string}>();
</script>

<template>
	<section class="k-panel">
		<header v-if="title || eyebrow" class="k-panel__header">
			<p v-if="eyebrow" class="k-panel__eyebrow">{{ eyebrow }}</p>
			<h2 v-if="title">{{ title }}</h2>
		</header>
		<div class="k-panel__body"><slot /></div>
	</section>
</template>

<style scoped>
@reference "../../style.css";
.k-panel { background: var(--color-surface); border: 1px solid var(--color-border); border-radius: 0.5rem; }
.k-panel__header { @apply px-5 pt-5; }
.k-panel__eyebrow { @apply mb-1 text-xs font-semibold uppercase tracking-widest; color: var(--color-accent); }
.k-panel h2 { @apply text-lg font-bold; color: var(--color-text); }
.k-panel__body { @apply p-5; }
</style>
