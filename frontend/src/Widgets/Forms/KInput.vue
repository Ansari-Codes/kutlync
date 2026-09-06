<script setup lang="ts">
defineProps<{
	label?: string;
	modelValue?: string;
	placeholder?: string;
	type?: string;
	maxlength?: string;
	min?: string;
	error?: string;
}>();

defineEmits<{ 'update:modelValue': [value: string] }>();
</script>

<template>
	<label class="k-input" :class="{'k-input--error': error}">
		<span v-if="label" class="k-input__label">{{ label }}</span>
		<input
			:type="type ?? 'text'"
			:value="modelValue"
			:placeholder="placeholder"
			:maxlength="maxlength"
			:min="min"
			:aria-invalid="Boolean(error)"
			@input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
		>
		<span v-if="error" class="k-input__error">{{ error }}</span>
	</label>
</template>

<style scoped>
@reference "../../style.css";
.k-input { @apply grid gap-1; }
.k-input__label { @apply text-xs font-semibold uppercase tracking-widest; color: var(--color-text-muted); }
.k-input input { @apply min-h-11 w-full rounded-lg px-3 text-sm outline-none transition-colors; background: var(--color-surface); color: var(--color-text); border: 1px solid var(--color-border); }
.k-input input::placeholder { color: var(--color-text-faint); }
.k-input input:focus { border-color: var(--color-accent); box-shadow: 0 0 0 3px var(--color-accent-soft); }
.k-input--error input { border-color: var(--color-danger); }
.k-input__error { @apply text-xs; color: var(--color-danger); }
</style>
