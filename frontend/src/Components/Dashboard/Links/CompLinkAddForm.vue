<script setup lang="ts">
import { ref, watch } from 'vue'

import KCheckbox from '@/Widgets/Forms/KCheckbox.vue'
import KInput from '@/Widgets/Forms/KInput.vue'
import KTextarea from '@/Widgets/Forms/KTextarea.vue'
import KButton from '@/Widgets/Actions/KButton.vue'

import type { InterfaceLink, InterfaceLinkInput } from '@/Services/Interfaces'

const props = withDefaults(defineProps<{
    mode?: 'add' | 'update' | 'edit'
    link?: Partial<InterfaceLink>
}>(), {
    mode: 'add'
})

const is_secure = ref(Boolean(props.link?.is_secured))
const security_action = ref<'remove' | 'update'>('update')
const max_age_input = ref(props.link?.max_age_minutes?.toString() ?? '')

const form = ref<{
    link_name: string
    link_description: string
    destination_link: string
    slug: string
    access_code: string
}>({
    link_name: props.link?.link_name ?? '',
    link_description: props.link?.link_description ?? '',
    destination_link: props.link?.destination_link ?? '',
    slug: props.link?.slug ?? '',
    access_code: '',
})

const emit = defineEmits<{
    handleNew: [data: InterfaceLinkInput]
    closeForm: []
}>()

watch(() => props.link, link => {
    is_secure.value = Boolean(link?.is_secured)
    max_age_input.value = link?.max_age_minutes?.toString() ?? ''
    form.value = {
        link_name: link?.link_name ?? '',
        link_description: link?.link_description ?? '',
        destination_link: link?.destination_link ?? '',
        slug: link?.slug ?? '',
        access_code: '',
    }
}, { deep: true })

function handleNew() {
    emit('handleNew', {
        ...form.value,
        max_age_minutes: max_age_input.value ? Number(max_age_input.value) : null,
        access_code: props.mode === 'add'
            ? (is_secure.value ? form.value.access_code : null)
            : (is_secure.value && security_action.value === 'update' ? form.value.access_code : null),
        security_action: props.mode === 'add'
            ? 'keep'
            : security_action.value,
    })
}
</script>

<template>
        <form
            class="w-full flex flex-col gap-5"
            @submit.prevent="handleNew"
        >
            <p v-if="props.mode === 'update' || props.mode === 'edit'" class="rounded-lg px-3 py-2 text-sm" style="background: var(--color-accent-soft); color: var(--color-accent-strong)">
                Update the link details and security settings.
            </p>

            <div class="w-full grid grid-cols-1 md:grid-cols-2 gap-4">
                <KInput
                    v-model="form.link_name"
                    label="Name"
                    placeholder="My Website"
                    maxlength="50"
                />

                <KInput
                    v-model="form.slug"
                    label="Slug"
                    placeholder="my-website"
                />
            </div>

            <!-- Destination -->
            <KInput
                v-model="form.destination_link"
                label="Target Link *"
                placeholder="https://example.com"
            />

            <!-- Description -->
            <KTextarea
                v-model="form.link_description"
                label="Description"
                placeholder="Describe what this link is for..."
                    maxlength="150"
            />

            <KInput
                v-model="max_age_input"
                label="Max age (minutes)"
                type="number"
                placeholder="Leave empty for no expiry"
                min="1"
            />

            <!-- Security -->
            <div class="w-full flex flex-col gap-3">
                <KCheckbox
                    v-if="props.mode === 'add' || !props.link?.is_secured"
                    v-model="is_secure"
                    label="Secure this link"
                />

                <div v-else class="grid gap-3 rounded-lg border p-3" style="border-color: var(--color-border)">
                    <p class="text-sm font-semibold">Link is secured</p>
                    <label class="flex items-center gap-2 text-sm">
                        <input v-model="security_action" type="radio" value="remove">
                        Remove security
                    </label>
                    <label class="flex items-center gap-2 text-sm">
                        <input v-model="security_action" type="radio" value="update">
                        Update security
                    </label>
                </div>

                <KInput
                    v-if="is_secure && (props.mode === 'add' || security_action === 'update')"
                    v-model="form.access_code"
                    label="Access Code"
                    placeholder="Enter access code"
                    class="max-w-md"
                />
            </div>

            <!-- Actions -->
            <div class="w-full flex justify-end gap-2">
                <KButton
                    variant="secondary"
                    label="Cancel"
                    type="button"
                    @click="emit('closeForm')"
                />

                <KButton
                    :label="props.mode === 'update' || props.mode === 'edit' ? 'Update Link' : 'Create Link'"
                    :icon="props.mode === 'update' || props.mode === 'edit' ? 'save' : 'add'"
                    type="submit"
                />
            </div>
        </form>
</template>