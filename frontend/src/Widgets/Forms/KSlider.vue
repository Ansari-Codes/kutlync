<script setup lang="ts">
withDefaults(defineProps<{
	label?: string;
	modelValue?: number;
	min?: number;
	max?: number;
	step?: number;
	showValue?: boolean;
}>(), {modelValue: 50, min: 0, max: 100, step: 1, showValue: true});

defineEmits<{ 'update:modelValue': [value: number] }>();
</script>

<template>
	<label class="k-slider">
		<span class="k-slider__heading"><span>{{ label ?? 'Value' }}</span><output v-if="showValue">{{ modelValue }}</output></span>
		<input type="range" :value="modelValue" :min="min" :max="max" :step="step" @input="$emit('update:modelValue', Number(($event.target as HTMLInputElement).value))">
	</label>
</template>

<style scoped>
@reference "../../style.css";
.k-slider { @apply grid gap-3; }
.k-slider__heading { @apply flex justify-between text-xs font-semibold uppercase tracking-widest; color: var(--color-text-muted); }
.k-slider output { color: var(--color-accent); }
.k-slider input { @apply h-1.5 w-full cursor-pointer appearance-none rounded-lg; background: var(--color-surface-muted); accent-color: var(--color-accent); }
.k-slider input::-webkit-slider-thumb { @apply size-4 appearance-none rounded-sm; background: var(--color-accent); }
</style>
