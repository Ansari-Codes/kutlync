<script setup lang="ts">
withDefaults(defineProps<{
	label?: string;
	modelValue?: string;
	options?: Array<{label: string; value: string}>;
}>(), {options: () => []});

defineEmits<{ 'update:modelValue': [value: string] }>();
</script>

<template>
	<label class="k-select">
		<span v-if="label" class="k-select__label">{{ label }}</span>
		<select :value="modelValue" @change="$emit('update:modelValue', ($event.target as HTMLSelectElement).value)">
			<option v-for="option in options" :key="option.value" :value="option.value">{{ option.label }}</option>
		</select>
	</label>
</template>

<style scoped>
@reference "../../style.css";
.k-select { @apply grid gap-2; }
.k-select__label { @apply text-xs font-semibold uppercase tracking-widest; color: var(--color-text-muted); }
.k-select select { @apply min-h-11 w-full rounded-lg px-3 text-sm outline-none transition-colors; background: var(--color-surface); color: var(--color-text); border: 1px solid var(--color-border); }
.k-select select:focus { border-color: var(--color-accent); box-shadow: 0 0 0 3px var(--color-accent-soft); }
</style>
