<script lang="ts" setup>

import KButton from '@/Widgets/Actions/KButton.vue'
import KMenu from '@/Widgets/Actions/KMenu.vue'

defineEmits<{
    view: []
    edit: []
    copy_link: []
    delete: []
    close: []
}>()

</script>

<template>

    <KMenu @close="$emit('close')" class="gap-2">

        <KButton
            icon="visibility"
            label="View"
            @click="$emit('view')"
        />

        <KButton
            icon="edit"
            label="Edit"
            @click="$emit('edit')"
        />

        <KButton
            icon="content_copy"
            label="Copy"
            @click="$emit('copy_link')"
        />


        <KButton
            icon="delete"
            label="Delete"
            variant="danger"
            @click="$emit('delete')"
        />

    </KMenu>

</template>