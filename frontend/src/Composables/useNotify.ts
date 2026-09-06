import { ref } from 'vue'

export type NotificationVariant = 'success' | 'error' | 'info' | 'warning'

export interface NotificationItem {
    id: number
    message: string
    variant: NotificationVariant
}

const notifications = ref<NotificationItem[]>([])
let nextId = 0

export function useNotify() {
    function notify(message: string, variant: NotificationVariant = 'info', duration = 4000) {
        const id = ++nextId
        notifications.value.push({ id, message, variant })
        if (duration > 0) window.setTimeout(() => dismiss(id), duration)
    }

    function dismiss(id: number) {
        notifications.value = notifications.value.filter(notification => notification.id !== id)
    }

    return { notifications, notify, dismiss }
}
