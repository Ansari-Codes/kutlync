<script setup>
import {RouterView} from 'vue-router'
import KNotificationContainer from '@/Widgets/Feedback/KNotificationContainer.vue'
import { useTheme } from '@/Composables/useTheme'

useTheme()
</script>

<template>
	<div class="min-h-screen">
        <RouterView></RouterView>
		<KNotificationContainer />
	</div>
</template>
