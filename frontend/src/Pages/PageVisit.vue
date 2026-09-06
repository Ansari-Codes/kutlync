<script lang="ts" setup>
import { useNotify } from '@/Composables/useNotify';
import { serveVerifyLink, serveIsSecured } from '@/Services/Links.serve';
import KButton from '@/Widgets/Actions/KButton.vue';
import KInput from '@/Widgets/Forms/KInput.vue';
import KPanel from '@/Widgets/Layout/KPanel.vue';
import { onMounted, ref } from 'vue';

const props = defineProps(["slug"])
const { notify } = useNotify()

const access_code = ref('')
const loading = ref(false)
const is_secured = ref(false)

async function verifyLink() {
    loading.value = true
    console.log(is_secured, access_code)
    if (is_secured.value && !access_code.value) {
        notify("The link is protected! Access code is required!", 'warning')
        return
    }
    try {
        const response = await serveVerifyLink(props.slug, access_code.value)
        if (response.success) {
            window.location.href = (response.data.destination_link)
        }
    } catch (e) {
        notify(String(e), 'error')
        console.log(e)
    }
    loading.value = false
}

onMounted(async () => {
    loading.value = true
    try {
        const response = await serveIsSecured(props.slug)
        is_secured.value = response.data.is_secured
        if (!is_secured.value) await verifyLink()
    } catch (e) {
        notify(String(e), 'error')
    }
    loading.value = false
})

</script>

<template>
    <div v-if="is_secured" class="w-full min-h-screen flex justify-center items-center">
        <KPanel title="Access Code" class="flex-col  w-full md:w-100">
            <KInput placeholder="Access Code" v-model:model-value="access_code" class="w-full mb-2" />
            <KButton @click="verifyLink" class="w-full">Verify</KButton>
        </KPanel>
    </div>
    <div v-else>Hang tight! Redirecting...</div>
</template>
