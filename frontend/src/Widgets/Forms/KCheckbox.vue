<script setup lang="ts">
withDefaults(defineProps<{label?: string; modelValue?: boolean; disabled?: boolean}>(), {label: 'Checkbox', modelValue: false, disabled: false});
defineEmits<{ 'update:modelValue': [value: boolean] }>();
</script>

<template>
	<label class="k-checkbox" :class="{'k-checkbox--disabled': disabled}">
		<input type="checkbox" :checked="modelValue" :disabled="disabled" @change="$emit('update:modelValue', ($event.target as HTMLInputElement).checked)">
		<span>{{ label }}</span>
	</label>
</template>

<style scoped>
@reference "../../style.css";
.k-checkbox { @apply inline-flex cursor-pointer items-center gap-3 text-sm; color: var(--color-text); }
.k-checkbox input { @apply size-4 cursor-pointer appearance-none rounded-sm; background: var(--color-surface); border: 1px solid var(--color-border); accent-color: var(--color-accent); }
.k-checkbox input:checked { background: var(--color-accent); border-color: var(--color-accent); box-shadow: inset 0 0 0 3px var(--color-surface); }
.k-checkbox input:focus-visible { @apply outline-2 outline-offset-2; outline-color: var(--color-accent); }
.k-checkbox--disabled { @apply cursor-not-allowed opacity-50; }
</style>
