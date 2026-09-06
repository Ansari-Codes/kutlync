<script setup>
import {RouterView} from 'vue-router'
import KNotificationContainer from '@/Widgets/Feedback/KNotificationContainer.vue'
</script>

<template>
	<div class="min-h-screen">
        <RouterView></RouterView>
		<KNotificationContainer />
	</div>
</template>
