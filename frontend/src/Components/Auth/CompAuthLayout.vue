<script setup lang="ts">
import KCard from '@W/Layout/KCard.vue'
import { computed, type PropType } from 'vue'

type AuthMode = 'login' | 'signup' | 'forgot-password'

const props = defineProps({
    mode: {
        type: String as PropType<AuthMode>,
        default: '',
    },
})

const content = computed(() => {
    return {
        'login': {
            title: 'Welcome back',
            description: 'Sign in to continue to KutLynk.',
        },

        'signup': {
            title: 'Create your account',
            description: 'Start creating shorter, smarter links.',
        },

        'forgot-password': {
            title: 'Reset your password',
            description: 'Enter your email and we’ll help you get back in.',
        },
    }[props.mode]
})
</script>

<template>
    <div class="min-h-screen flex items-center justify-center px-4 py-8" style="background: var(--color-page)">
        <KCard class="w-full max-w-md overflow-hidden kutlync-reveal">
            <template #header>
                <div class="flex flex-col items-center text-center">
                    <h1 class="text-xl font-bold tracking-tight">
                        {{ content.title }}
                    </h1>
                    <p class="max-w-sm text-sm leading-4" style="color: var(--color-text-muted)">
                        {{ content.description }}
                    </p>
                </div>
            </template>

            <slot />
        </KCard>
    </div>
</template>
