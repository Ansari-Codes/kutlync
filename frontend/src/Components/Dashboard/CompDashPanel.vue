<script setup lang="ts">
const props = defineProps(["title", "tagline"])
</script>

<template>
    <div class="w-full h-full p-2 sm:p-6 bg-white dark:bg-(--color-page)">
        <div class="w-full h-fit flex flex-col sm:flex-row justify-between items-center">
            <div class="shrink-0 hidden sm:flex w-fit h-full flex-col pb-2">
                <span class="text-xl w-fit h-fit font-bold text(--color-text)">{{ title }}</span>
                <span v-if="tagline" class="text-sm">{{ tagline }}</span>
            </div>
            <div class="shrink-0 w-full sm:w-fit">
                <slot name="header" />
            </div>
        </div>
        <slot />
    </div>
</template>