<script setup lang="ts">
import KFeedback from './KFeedback.vue'
import { useNotify } from '@/Composables/useNotify'

const { notifications, dismiss } = useNotify()
</script>

<template>
    <div class="k-notification-container" aria-live="polite">
        <KFeedback
            v-for="notification in notifications"
            :key="notification.id"
            :message="notification.message"
            :variant="notification.variant"
            :closable="true"
            @close="dismiss(notification.id)"
        />
    </div>
</template>

<style scoped>
@reference "../../style.css";

.k-notification-container {
    @apply fixed right-4 top-4 z-50 flex w-[min(24rem,calc(100vw-2rem))] flex-col gap-3;
}
</style>
