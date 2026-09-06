import { computed, onMounted, onBeforeUnmount, ref } from 'vue'

export type Theme = 'light' | 'dark' | 'system'

const theme = ref<Theme>('system')

function resolveThemeValue(value: Theme): 'light' | 'dark' {
    if (value === 'dark' || value === 'light') {
        return value
    }

    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

export function useTheme() {
    const isDark = computed(() => resolveThemeValue(theme.value) === 'dark')

    function applyTheme(nextTheme: Theme) {
        theme.value = nextTheme

        const effectiveTheme = resolveThemeValue(nextTheme)
        document.documentElement.dataset.theme = effectiveTheme
        localStorage.setItem('kutlync-theme', nextTheme)
    }

    function syncSystemTheme() {
        if (theme.value === 'system') {
            document.documentElement.dataset.theme = resolveThemeValue('system')
        }
    }

    function toggleTheme() {
        applyTheme(isDark.value ? 'light' : 'dark')
    }

    onMounted(() => {
        const media = window.matchMedia('(prefers-color-scheme: dark)')
        const updateFromSystem = () => syncSystemTheme()

        media.addEventListener('change', updateFromSystem)

        const storedTheme = localStorage.getItem('kutlync-theme') as Theme | null
        const initialTheme = storedTheme === 'light' || storedTheme === 'dark' || storedTheme === 'system'
            ? storedTheme
            : 'system'

        applyTheme(initialTheme)

        onBeforeUnmount(() => {
            media.removeEventListener('change', updateFromSystem)
        })
    })

    return { theme, isDark, applyTheme, toggleTheme }
}
