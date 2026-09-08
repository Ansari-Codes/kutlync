<script setup lang="ts">
import KIcon from '@/Widgets/UX/KIcon.vue'

withDefaults(defineProps<{
    label?: string
    icon?: string
    iconPosition?: 'left' | 'right'
    type?: 'button' | 'submit' | 'reset'
    variant?: 'primary' | 'secondary' | 'quiet' | 'danger'
    disabled?: boolean
    loading?: boolean
}>(), {
    label: '',
    icon: '',
    iconPosition: 'left',
    type: 'button',
    variant: 'primary',
    disabled: false,
    loading: false,
})
</script>

<template>
    <button
        class="k-button"
        :class="`k-button--${variant}`"
        :type="type"
        :disabled="disabled || loading"
    >
        <KIcon v-if="loading" icon="progress_activity" class="k-button__spinner" />
        <KIcon
            v-else-if="icon && iconPosition === 'left'"
            :icon="icon"
        />

        <slot>{{ label }}</slot>

        <KIcon
            v-if="icon && iconPosition === 'right'"
            :icon="icon"
        />
    </button>
</template>

<style scoped>
@reference "../../style.css";

.k-button {
    @apply cursor-pointer inline-flex min-h-10 items-center justify-center gap-2 rounded-lg px-4 text-sm font-semibold transition-colors duration-200;
}

.k-button:focus-visible {
    @apply outline-2 outline-offset-2;
    outline-color: var(--color-accent);
}

.k-button:disabled {
    @apply cursor-not-allowed opacity-45;
}

.k-button--primary {
    background: var(--color-accent);
    color: var(--color-on-accent);
}

.k-button--primary:hover:not(:disabled) {
    background: var(--color-accent-strong);
}

.k-button--secondary {
    background: var(--color-surface-muted);
    color: var(--color-text);
}

.k-button--secondary:hover:not(:disabled) {
    background: var(--color-border);
}

.k-button--quiet {
    color: var(--color-text-muted);
}

.k-button--danger {
    background: var(--color-danger);
    color:white;
}

.k-button--danger:hover:not(:disabled) {
    background: var(--color-danger);
    color:whitesmoke;
}
.k-button--quiet:hover:not(:disabled) {
    background: var(--color-surface-muted);
    color: var(--color-text);
}
</style>