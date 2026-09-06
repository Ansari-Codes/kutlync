<script lang="ts" setup>
import KPanel from '@W/Layout/KPanel.vue'
import KSelect from '@W/Forms/KSelect.vue'

import { useTheme, type Theme } from '@/Composables/useTheme'
import { ref } from 'vue'

const handleTheme = useTheme()
const theme = ref<Theme>(handleTheme.theme.value)

function handleThemeChange(val: string) {
    const nextTheme = val as Theme
    handleTheme.applyTheme(nextTheme)
    theme.value = nextTheme
}
</script>

<template>
    <KPanel>
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
    </KPanel>
</template>
