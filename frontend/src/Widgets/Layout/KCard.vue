<script setup lang="ts">
defineProps<{
    title?: string
    description?: string
}>()
</script>

<template>
    <article class="k-card">
        <!-- Header -->
        <header v-if="$slots.header || title || description" class="k-card__header">
            <!-- Custom header takes priority -->
            <slot v-if="$slots.header" name="header" />

            <!-- Default header -->
            <template v-else>
                <h3 v-if="title">
                    {{ title }}
                </h3>

                <p v-if="description">
                    {{ description }}
                </p>
            </template>
        </header>

        <!-- Main content -->
        <div class="k-card__body">
            <slot />
        </div>

        <!-- Custom footer -->
        <footer v-if="$slots.footer" class="k-card__footer">
            <slot name="footer" />
        </footer>
    </article>
</template>

<style scoped>
@reference "../../style.css";

.k-card {
    @apply grid rounded-lg p-4;

    background: var(--color-surface);
    border: 1px solid var(--color-border);
}

.k-card__header h3 {
    @apply text-base font-bold;

    color: var(--color-text);
}

.k-card__body {
    @apply min-w-0;
}

.k-card__footer {
    @apply border-t;

    border-color: var(--color-border);
}
</style>