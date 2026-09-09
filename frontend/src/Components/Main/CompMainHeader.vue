<script setup lang="ts">
import Logo from '@C/Logo.vue'
import KButton from '@W/Actions/KButton.vue'
import KLink from '@W/Actions/KLink.vue'
</script>

<template>
    <header class="flex items-center justify-between gap-6 py-6">
        <KLink to="/" class="no-underline hover:no-underline">
            <Logo :width="36" :height="36" :text-size="22" />
        </KLink>

        <nav class="items-center gap-3 flex flex-row " aria-label="Main navigation">
            <div class="w-fit gap-3 hidden sm:flex">
                <KLink href="https://github.com/Ansari-Codes/kutlync" target="_blank" rel="noopener noreferrer">
                    GitHub
                </KLink>
                <KButton label="Start shortening" @click="$router.push('/auth/signup')" />
            </div>
            <KLink to="/auth/login" class="sm:hidden no-underline hover:no-underline">
                <KButton label="Login" />
            </KLink>
        </nav>

    </header>
</template>