<script lang="ts" setup>

import { onMounted, onUnmounted, ref } from 'vue'

const emit = defineEmits<{
    close: []
}>()

const menuRef = ref<HTMLElement | null>(null)

function handleOutsideClick(event: MouseEvent) {

    const target = event.target as Node

    if (
        menuRef.value &&
        !menuRef.value.contains(target)
    ) {
        emit('close')
    }

}

onMounted(() => {

    document.addEventListener(
        'click',
        handleOutsideClick,
        true
    )

})

onUnmounted(() => {

    document.removeEventListener(
        'click',
        handleOutsideClick,
        true
    )

})

</script>

<template>

    <div
        ref="menuRef"
        class="k-menu"
    >
        <slot />
    </div>

</template>

<style scoped>

@reference "../../style.css";

.k-menu {
    @apply p-1.5 rounded-lg border shadow-lg flex flex-col w-fit;

    background: var(--color-surface);
    border-color: var(--color-border);
}

</style>