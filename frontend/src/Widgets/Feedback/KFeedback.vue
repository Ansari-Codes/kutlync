<script setup lang="ts">
import { ref } from 'vue'

const props = withDefaults(
    defineProps<{
        message: string
        icon?: string
        variant?: 'success' | 'error' | 'info' | 'warning'
        closable?: boolean
    }>(),
    {
        icon: '',
        variant: 'info',
        closable: false
    }
)

const emit = defineEmits<{
    close: []
}>()

const visible = ref(true)

const close = () => {
    visible.value = false
    emit('close')
}
</script>

<template>
    <div
        v-if="visible"
        class="k-feedback"
        :class="`k-feedback--${props.variant}`"
        role="alert"
    >
        <span
            v-if="props.icon"
            class="material-symbols-outlined k-feedback__icon"
        >
            {{ props.icon }}
        </span>

        <span class="k-feedback__message">
            {{ props.message }}
        </span>

        <button
            v-if="props.closable"
            type="button"
            class="k-feedback__close"
            aria-label="Close"
            @click="close"
        >
            <span class="material-symbols-outlined">
                close
            </span>
        </button>
    </div>
</template>

<style scoped>
@reference "../../style.css";

.k-feedback {
    @apply w-full flex items-center gap-3 rounded-lg border px-4 py-3 text-sm font-medium;
}

.k-feedback__icon {
    @apply shrink-0 text-xl;
}

.k-feedback__message {
    @apply min-w-0 flex-1;
}

.k-feedback__close {
    @apply shrink-0 cursor-pointer rounded-md p-1 transition-colors;
}

.k-feedback__close:hover {
    background: color-mix(
        in srgb,
        currentColor 10%,
        transparent
    );
}

.k-feedback--success {
    background: var(--color-success-soft);
    border-color: var(--color-success);
    color: var(--color-success);
}

.k-feedback--error {
    background: color-mix(
        in srgb,
        var(--color-danger) 12%,
        var(--color-surface)
    );
    border-color: var(--color-danger);
    color: var(--color-danger);
}

.k-feedback--warning {
    background: var(--color-warning-soft);
    border-color: var(--color-warning);
    color: var(--color-warning);
}

.k-feedback--info {
    background: var(--color-accent-soft);
    border-color: var(--color-accent);
    color: var(--color-accent-strong);
}
</style>