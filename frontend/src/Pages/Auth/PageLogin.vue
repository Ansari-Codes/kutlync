<script setup lang="ts">
import CompAuthForm from '@C/Auth/CompAuthForm.vue'
import CompAuthContent from '@C/Auth/CompAuthLayout.vue'

import { ref } from 'vue'
import { useRouter } from 'vue-router'

import { serveLogIn } from '@/Services/Auth.serve'

const router = useRouter()

const form = ref({
    email: '',
    password: ''
})

const loading = ref(false)

const error = ref('')

async function handleLogIn(data: Record<string, string | undefined>) {
    loading.value = true
    error.value = ''

    try {
        const response = await serveLogIn({
            email: String(data.email ?? ''),
            password: String(data.password ?? '')
        })

        if (!response.success) {
            error.value = response.message ?? 'Unable to log in!'
            return
        }

        await router.push('/dashboard')

    } catch (err) {
        error.value = err instanceof Error
            ? err.message
            : 'Something went wrong!'

    } finally {
        loading.value = false
    }
}
</script>

<template>
    <CompAuthContent mode="login">
        <p v-if="error" class="mb-4 rounded-lg px-3 py-2 text-sm">
            {{ error }}
        </p>

        <CompAuthForm :form="form" mode="login" :loading="loading" @submit="handleLogIn" />
    </CompAuthContent>

</template>
