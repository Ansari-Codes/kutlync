<script setup lang="ts">
defineProps<{label: string; pressed?: boolean}>();
defineEmits<{click: []}>();
</script>

<template>
	<button class="k-icon-button" :class="{'k-icon-button--pressed': pressed}" type="button" :aria-label="label" :aria-pressed="pressed" @click="$emit('click')">
		<slot />
	</button>
</template>

<style scoped>
@reference "../../style.css";
.k-icon-button { @apply inline-flex size-10 items-center justify-center rounded-lg text-base transition-colors duration-200; color: var(--color-text-muted); }
.k-icon-button:hover { background: var(--color-surface-muted); color: var(--color-text); }
.k-icon-button:focus-visible { @apply outline-2 outline-offset-2; outline-color: var(--color-accent); }
.k-icon-button--pressed { background: var(--color-accent-soft); color: var(--color-accent); }
</style>
