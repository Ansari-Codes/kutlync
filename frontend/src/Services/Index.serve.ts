import { BACKEND_BASE_API_URL } from '@/Services/Routes'
import type { Response } from '@/Services/Interfaces'
import { useAuthStore } from '@/Stores/Auth.store'

export default async function API<T = unknown>(
    path: string,
    data: object = {},
    options: { includeUser?: boolean; method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE' } = {}
): Promise<Response<T>> {
    const authStore = useAuthStore()
    const method = options.method ?? 'POST'
    const headers: Record<string, string> = {
        'Content-Type': 'application/json'
    }

    if (authStore.token) {
        headers.Authorization = `Bearer ${authStore.token}`
    }

    const requestBody = method === 'GET' ? undefined : JSON.stringify(data)
    const url = `${BACKEND_BASE_API_URL}${path}`

    const response = await fetch(url, {
        method,
        headers,
        body: requestBody
    })

    const json = await response.json()

    if (!response.ok) {
        return {
            success: false,
            message: json?.message ?? 'Request failed',
            data: (json?.data ?? null) as T
        }
    }

    return {
        success: true,
        message: json?.message ?? 'Request successful',
        data: (json?.data ?? {}) as T
    }
}