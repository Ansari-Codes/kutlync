<script setup lang="ts">
import type { InterfaceDashboardSidebar } from '@/Composables/Interfaces';
import { ROUTES } from '@/Services/Routes';
import KButton from '@/Widgets/Actions/KButton.vue';
import KIcon from '@/Widgets/UX/KIcon.vue';
import Logo from '@C/Logo.vue';
import { ref } from 'vue';

const props = defineProps(["current_tab"])

const sidebar: InterfaceDashboardSidebar[] = [
    {
        name: 'Dashboard',
        icon: 'dashboard',
        target: ROUTES.DASHBOARD.BASE
    },
    {
        name: 'Links',
        icon: 'link',
        target: ROUTES.DASHBOARD.LINKS
    },
    {
        name: 'TrashBox',
        icon: 'auto_delete',
        target: ROUTES.DASHBOARD.TRASHBOX
    },
    {
        name: 'Analytics',
        icon: 'analytics',
        target: ROUTES.DASHBOARD.ANALYTICS
    },
    {
        name: 'Settings',
        icon: 'settings',
        target: ROUTES.DASHBOARD.SETTINGS
    },
]

const btn_group_open = ref(true)

</script>
<template>
    <div class="h-full w-full flex flex-col bg-(--color-surface-muted) p-2  gap-3">

        <div class="flex flex-row items-center justify-between w-full h-fit">

            <div class="w-fit sm:w-full justify-center">
                <Logo class="w-full" />
            </div>

            <KButton class="size-12 flex sm:hidden!" @click="btn_group_open = !btn_group_open">
                <KIcon icon="menu" />
            </KButton>

        </div>

        <div v-if="btn_group_open" class="h-full w-full flex flex-col bg-transparent gap-1.5">
            <RouterLink v-for="btn in sidebar" :key="btn.name" :to="btn.target.startsWith('/')
                ? btn.target
                : { name: btn.target }">
                <KButton :variant="current_tab === btn.name.toLowerCase()
                        ? 'secondary'
                        : 'primary'
                    " class="w-full">
                    <div class="w-full flex flex-row gap-3 justify-start items-center pl-3">
                        <KIcon :icon="btn.icon" />
                        {{ btn.name }}
                    </div>
                </KButton>
            </RouterLink>
        </div>

    </div>
</template>