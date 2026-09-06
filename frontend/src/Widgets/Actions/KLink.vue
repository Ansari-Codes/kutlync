<script setup lang="ts">
import {computed} from 'vue';
import {RouterLink, type RouteLocationRaw} from 'vue-router';

type LinkTarget = RouteLocationRaw | string;

const props = withDefaults(defineProps<{
	to?: LinkTarget;
	href?: string;
	external?: boolean;
	target?: '_self' | '_blank' | '_parent' | '_top';
	rel?: string;
}>(), {
	external: undefined,
	target: '_self',
});

const isExternal = computed(() => {
	if (props.external !== undefined) return props.external;
	if (props.href) return true;
	if (typeof props.to !== 'string') return false;
	return /^(https?:|mailto:|tel:|\/\/)/i.test(props.to);
});

const linkTarget = computed(() => props.href ?? props.to ?? '#');
const externalRel = computed(() => props.rel ?? (props.target === '_blank' ? 'noopener noreferrer' : undefined));
</script>

<template>
	<a
		v-if="isExternal"
		class="k-link"
		:href="String(linkTarget)"
		:target="target"
		:rel="externalRel"
	>
		<slot />
	</a>
	<RouterLink v-else class="k-link" :to="linkTarget">
		<slot />
	</RouterLink>
</template>

<style scoped>
@reference "../../style.css";
.k-link { @apply inline-flex items-center text-sm font-semibold underline-offset-4 transition-colors duration-200; color: var(--color-accent); }
.k-link:hover { color: var(--color-accent-strong); text-decoration: underline; }
.k-link:focus-visible { @apply rounded-sm outline-2 outline-offset-2; outline-color: var(--color-accent); }
</style>
