<script setup lang="ts">
import KButton from '@/Widgets/Actions/KButton.vue'
import KMenu from '@/Widgets/Actions/KMenu.vue'

defineEmits<{
    view: []
    restore: []
    permanentDelete: []
    close: []
}>()
</script>

<template>
    <KMenu class="gap-2" @close="$emit('close')">
        <KButton icon="visibility" label="View" @click="$emit('view')" />
        <KButton icon="restore" label="Restore" @click="$emit('restore')" />
        <KButton icon="delete_forever" label="Delete permanently" variant="danger" @click="$emit('permanentDelete')" />
    </KMenu>
</template>
