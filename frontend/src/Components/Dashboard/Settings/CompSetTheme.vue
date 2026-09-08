<script lang="ts" setup>
import KSelect from '@W/Forms/KSelect.vue'

import { useTheme, type Theme } from '@/Composables/useTheme'

const handleTheme = useTheme()
const theme = handleTheme.theme

function handleThemeChange(val: string) {
    const nextTheme = val as Theme
    handleTheme.applyTheme(nextTheme)
}
</script>

<template>
    <KSelect
        label="Theme"
        :model-value="theme"
        @update:model-value="handleThemeChange"
        :options="[
            { label: 'System', value: 'system' },
            { label: 'Dark', value: 'dark' },
            { label: 'Light', value: 'light' }
        ]"
    />
</template>
