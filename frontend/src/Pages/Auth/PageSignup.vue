<script setup lang="ts">
import CompAuthForm from '@C/Auth/CompAuthForm.vue'
import CompAuthContent from '@C/Auth/CompAuthLayout.vue'

import { ref } from 'vue'
import { useRouter } from 'vue-router'

import { serveSignUp } from '@/Services/Auth.serve'

const router = useRouter()

const form = ref({
    username: '',
    email: '',
    password: '',
    confirm: ''
})

const loading = ref(false)

const error = ref('')

async function handleSignUp(data: Record<string, string | undefined>) {
    loading.value = true
    error.value = ''

    try {
        if (String(data.password ?? '') !== String(data.confirm ?? '')) {
            error.value = 'Passwords do not match!'
            return
        }

        const response = await serveSignUp({
            username: String(data.username ?? ''),
            email: String(data.email ?? ''),
            password: String(data.password ?? '')
        })

        if (!response.success) {
            error.value = response.message ?? 'Unable to create account!'
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
    <CompAuthContent mode="signup">
        <p v-if="error" class="mb-4 rounded-lg px-3 py-2 text-sm">
            {{ error }}
        </p>

        <CompAuthForm :form="form" mode="signup" :loading="loading" @submit="handleSignUp" />
    </CompAuthContent>

</template>
