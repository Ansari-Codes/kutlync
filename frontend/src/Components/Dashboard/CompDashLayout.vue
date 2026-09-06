<script setup lang="ts">
</script>

<template>
    <div class="w-screen h-screen overflow-hidden flex flex-col sm:flex-row bg-color-page">

        <aside class="w-full sm:w-64 h-fit sm:h-full shrink-0">
            <slot name="sidebar" />
        </aside>

        <main class="flex-1 min-w-0 min-h-0 h-full overflow-y-auto">
            <slot name="content" />
        </main>

    </div>
</template>