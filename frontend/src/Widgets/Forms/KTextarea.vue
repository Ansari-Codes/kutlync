<script setup lang="ts">
defineProps<{label?: string; modelValue?: string; placeholder?: string; rows?: number; maxlength?: string}>();
defineEmits<{ 'update:modelValue': [value: string] }>();
</script>

<template>
	<label class="k-textarea">
		<span v-if="label" class="k-textarea__label">{{ label }}</span>
		<textarea :value="modelValue" :placeholder="placeholder" :rows="rows ?? 3" :maxlength="maxlength" @input="$emit('update:modelValue', ($event.target as HTMLTextAreaElement).value)" />
	</label>
</template>

<style scoped>
@reference "../../style.css";
.k-textarea { @apply grid gap-2; }
.k-textarea__label { @apply text-xs font-semibold uppercase tracking-widest; color: var(--color-text-muted); }
.k-textarea textarea { @apply w-full resize-y rounded-lg px-3 py-2 text-sm outline-none transition-colors; background: var(--color-surface); color: var(--color-text); border: 1px solid var(--color-border); }
.k-textarea textarea:focus { border-color: var(--color-accent); box-shadow: 0 0 0 3px var(--color-accent-soft); }
</style>
