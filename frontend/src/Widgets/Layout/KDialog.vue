<script setup lang="ts">
import KPanel from '@/Widgets/Layout/KPanel.vue'

const props = withDefaults(defineProps<{
    modelValue: boolean
    mode?: 'inpage' | 'elevated'
    title?: string
}>(), {
    mode: 'elevated',
    title: ''
})

const emit = defineEmits<{
    'update:modelValue': [value: boolean]
    close: []
}>()

function close() {
    emit('update:modelValue', false)
    emit('close')
}
</script>

<template>
    <Teleport v-if="props.mode === 'elevated'" to="body">
        <div v-if="props.modelValue" class="k-dialog-backdrop" @click.self="close">
            <KPanel :title="props.title" class="border-0! p-0! m-0! k-dialog-panel">
                <button class="k-dialog-close" type="button" aria-label="Close" @click="close">×</button>
                <slot />
            </KPanel>
        </div>
    </Teleport>
    <KPanel v-else-if="props.modelValue" :title="props.title" class="k-dialog-inpage">
        <button class="k-dialog-close" type="button" aria-label="Close" @click="close">×</button>
        <slot />
    </KPanel>
</template>

<style scoped>
@reference "../../style.css";
.k-dialog-backdrop { @apply p-0 m-0 fixed inset-0 z-100 grid place-items-center ; background: rgb(0 0 0 / 45%); }
.k-dialog-panel { @apply relative max-h-[90vh] w-full max-w-2xl overflow-y-auto border-0! p-0!; }
.k-dialog-inpage { @apply relative; }
.k-dialog-close { @apply absolute right-3 top-3 z-10 grid h-8 w-8 place-items-center rounded-full text-xl; color: var(--color-text-muted); }
.k-dialog-close:hover { background: var(--color-surface-muted); color: var(--color-text); }
</style>
