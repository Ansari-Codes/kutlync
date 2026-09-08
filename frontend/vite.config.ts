import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import { defineConfig, loadEnv } from 'vite'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig(({ mode }) => {
    const env = loadEnv(mode, process.cwd(), '')

    return {
        base: env.VITE_BASE || '/',

        plugins: [
            vue(),
            tailwindcss()
        ],

        server: {
            host: '127.0.0.1',
            port: 5173
        },

        resolve: {
            alias: {
                '@': fileURLToPath(new URL('./src', import.meta.url)),
                '@C': fileURLToPath(new URL('./src/Components', import.meta.url)),
                '@W': fileURLToPath(new URL('./src/Widgets', import.meta.url)),
                '@S': fileURLToPath(new URL('./src/Services', import.meta.url))
            }
        }
    }
})