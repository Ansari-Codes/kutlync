import API from '@/Services/Index.serve'
import { BACKEND } from '@/Services/Routes'
import type { InterfaceAnalytics, InterfaceStatistics, Response } from '@/Services/Interfaces'

export async function serveAnalytics(days = 30): Promise<Response<InterfaceAnalytics>> {
    const response = await API<InterfaceAnalytics>(`${BACKEND.ANALYTICS}?days=${days}`, {}, { method: 'GET' })
    if (!response.success) throw new Error(response.message)
    return response
}

export async function serveStatistics(): Promise<Response<InterfaceStatistics>> {
    const response = await API<InterfaceStatistics>(`${BACKEND.STATS}`, {}, { method: 'GET' })
    if (!response.success) throw new Error(response.message)
    return response
}
