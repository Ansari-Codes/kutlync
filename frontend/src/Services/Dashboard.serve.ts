import API from '@/Services/Index.serve'
import { BACKEND } from '@/Services/Routes'
import type { InterfaceUserDashboardStats } from '@/Services/Interfaces'
import type { Response } from '@/Services/Interfaces'

export async function serveUserDashStats(): Promise<Response<InterfaceUserDashboardStats>> {
    const response = await API<InterfaceUserDashboardStats>(BACKEND.DASHBOARD.STATS, {}, { method: 'GET' })

    if (!response.success) {
        throw new Error(response.message)
    }

    return response
}

