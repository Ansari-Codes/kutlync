<script setup lang="ts">
import { computed } from 'vue'

import KInput from '@W/Forms/KInput.vue'
import KCheckbox from '@W/Forms/KCheckbox.vue'
import KButton from '@W/Actions/KButton.vue'
import KLink from '@W/Actions/KLink.vue'

type AuthMode =
    | 'login'
    | 'signup'
    | 'forgot-password'

type FormCredentials = Record<string, string | undefined>

const props = defineProps<{
    form: FormCredentials
    mode: AuthMode
    loading?: boolean
}>()

const formKeys = computed<string[]>(() => {
    return Object.keys(props.form)
})

const emit = defineEmits<{
    (e: 'submit', data: FormCredentials): void
}>()

const title = computed<string>(() => {
    return props.mode
        .replace('-', ' ')
        .replace(/^./, (value) => value.toUpperCase())
})

const formatLabel = (key: string): string => {
    return key
        .replace(/([A-Z])/g, ' $1')
        .replace(/^./, (value) => value.toUpperCase())
}

const getInputType = (key: string): string => {
    if (key === 'password' || key === 'confirm') {
        return 'password'
    }

    if (key === 'email') {
        return 'email'
    }

    return 'text'
}

function handleSubmit() {
    if (props.loading) {
        return
    }

    emit('submit', props.form)
}
</script>

<template>
    <form
        class="flex h-full w-full flex-col gap-3 p-2"
        @submit.prevent="handleSubmit"
    >
        <div>
            <div
                v-for="key in formKeys"
                :key="key"
                class="mt-3"
            >
                <KInput
                    v-model="props.form[String(key)]"
                    :label="formatLabel(String(key))"
                    :type="getInputType(String(key))"
                    :placeholder="`Enter your ${formatLabel(String(key)).toLowerCase()}`"
                    :disabled="loading"
                />
            </div>
        </div>

        <KCheckbox
            v-if="mode === 'signup'"
            class="w-full"
            label="Agree to all terms and conditions"
            :disabled="loading"
        />

        <KButton
            type="submit"
            :disabled="loading"
        >
            {{ loading ? 'Please wait...' : title }}
        </KButton>

        <div class="flex w-full flex-col items-center justify-center text-center">
            <p v-if="mode === 'signup'">
                Already have an account?

                <KLink to="/auth/login">
                    Log in
                </KLink>
            </p>

            <p v-else-if="mode === 'login'">
                No account?

                <KLink to="/auth/signup">
                    Create one
                </KLink>

                <br>

                Forgot your password?

                <KLink to="/auth/forgot-pass">
                    Reset it here
                </KLink>
            </p>
        </div>
    </form>
</template>