<script setup lang="ts">
import CompDashPanel from '@C/Dashboard/CompDashPanel.vue';
import CompSetTheme from '@C/Dashboard/Settings/CompSetTheme.vue';
import KPanel from '@/Widgets/Layout/KPanel.vue'
import KInput from '@/Widgets/Forms/KInput.vue'
import KButton from '@/Widgets/Actions/KButton.vue'
import API from '@/Services/Index.serve'
import { useAuthStore } from '@/Stores/Auth.store'
import { ref } from 'vue'

const auth = useAuthStore()
const profile = ref({ username: auth.user?.username ?? '', email: auth.user?.email ?? '' })
const passwords = ref({ old_password: '', new_password: '', confirm_password: '' })
const message = ref('')
const error = ref('')

async function saveProfile() {
    message.value = ''; error.value = ''
    try {
        const response = await API<{ id: number; username: string; email: string }>('/auth/profile', profile.value, { method: 'PATCH' })
        if (!response.success) throw new Error(response.message)
        auth.authenticate(response.data, auth.token ?? undefined)
        message.value = response.message
    } catch (err) { error.value = String(err) }
}

async function savePassword() {
    message.value = ''; error.value = ''
    try {
        const response = await API<null>('/auth/password', passwords.value, { method: 'PATCH' })
        if (!response.success) throw new Error(response.message)
        passwords.value = { old_password: '', new_password: '', confirm_password: '' }
        message.value = response.message
    } catch (err) { error.value = String(err) }
}
</script>

<template>
    <CompDashPanel title="Settings">
        <div class="grid w-full max-w-2xl gap-5 pb-4">
            <p v-if="message" class="rounded-lg px-3 py-2 text-sm" style="background: var(--color-success-soft); color: var(--color-success)">{{ message }}</p>
            <p v-if="error" class="rounded-lg px-3 py-2 text-sm" style="background: var(--color-danger); color: white">{{ error }}</p>

            <KPanel title="Profile" eyebrow="Personal details">
                <form class="grid gap-4" @submit.prevent="saveProfile">
                    <KInput v-model="profile.username" label="Username" autocomplete="username" />
                    <KInput v-model="profile.email" label="Email" type="email" autocomplete="email" />
                    <div class="flex justify-end"><KButton label="Save profile" icon="save" type="submit" /></div>
                </form>
            </KPanel>

            <KPanel title="Change password" eyebrow="Keep your account secure">
                <form class="grid gap-4" @submit.prevent="savePassword">
                    <KInput v-model="passwords.old_password" label="Current password" type="password" autocomplete="current-password" />
                    <KInput v-model="passwords.new_password" label="New password" type="password" autocomplete="new-password" />
                    <KInput v-model="passwords.confirm_password" label="Confirm new password" type="password" autocomplete="new-password" />
                    <div class="flex justify-end"><KButton label="Update password" icon="lock_reset" type="submit" /></div>
                </form>
            </KPanel>

            <KPanel title="Theme" eyebrow="Appearance">
                <CompSetTheme />
            </KPanel>
        </div>
    </CompDashPanel>
</template>
