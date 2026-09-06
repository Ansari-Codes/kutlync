<script setup lang="ts">
import logo from "@/assets/logo.svg"

const props = withDefaults(
    defineProps<{
        mode?: "full" | "vertical" | "logo",
        width?: number,
        height?: number,
        text_size?: number
    }>(),
    {
        mode: "full",
    }
)
</script>

<template>
    <div v-if="mode === 'full'" class="flex flex-row gap-2 items-center">
        <img :src="logo" alt="Kutlync" :width="width??48" :height="height??48" />
        <span :class="`font-bold`" :style="`font-size: ${text_size??36}px;`">KutLync</span>
    </div>
    <img v-else-if="mode === 'logo'" :src="logo" alt="Kutlync" :width="width??48" :height="height??48" />
    <div v-else-if="mode === 'vertical'" class="flex flex-col gap-1 items-center">
        <img :src="logo" alt="Kutlync" :width="width??64" :height="height??64" />
        <span :class="`font-bold`" :style="`font-size: ${text_size??24}px;`">KutLync</span>
    </div>

</template>