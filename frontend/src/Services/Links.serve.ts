import API from '@/Services/Index.serve'

import { BACKEND } from '@/Services/Routes'

import type {
    InterfaceUserDashboardStats,
    InterfaceLink,
    InterfaceLinkInput,
    InterfaceLinkFilters
} from '@/Services/Interfaces'

import type { Response } from '@/Services/Interfaces'


export function servePrepareLinks(links: InterfaceLink[]): InterfaceLink[] {
    return links.map(link => ({
        ...link,
        created_at: `${link.created_at.replace(' ', 'T')}Z`,
        updated_at: `${link.updated_at.replace(' ', 'T')}Z`,
    }))
}

export async function serveUserDashStats(): Promise<Response<InterfaceUserDashboardStats>> {
    const response = await API<InterfaceUserDashboardStats>(
        BACKEND.DASHBOARD.STATS,
        {},
        { method: 'GET' }
    )

    if (!response.success) {
        throw new Error(response.message)
    }

    return response
}


// Add a link
export async function serveAddLink(
    link: InterfaceLinkInput
): Promise<Response<InterfaceLink>> {
    const response = await API<InterfaceLink>(
        BACKEND.LINKS,
        link,
        { method: 'POST' }
    )

    if (!response.success) {
        throw new Error(response.message)
    }

    response.data = servePrepareLinks([response.data])[0]

    return response
}


// Remove a link
export async function serveRemoveLink(
    id: string
): Promise<Response<InterfaceLink>> {
    const response = await API<InterfaceLink>(
        `${BACKEND.LINKS}/${id}`,
        {},
        { method: 'DELETE' }
    )

    if (!response.success) {
        throw new Error(response.message)
    }

    response.data = servePrepareLinks([response.data])[0]

    return response
}


// Edit a link
export async function serveEditLink(
    id: string,
    link: Partial<InterfaceLinkInput>
): Promise<Response<InterfaceLink>> {
    const response = await API<InterfaceLink>(
        `${BACKEND.LINKS}/${id}`,
        link,
        { method: 'PATCH' }
    )

    if (!response.success) {
        throw new Error(response.message)
    }

    response.data = servePrepareLinks([response.data])[0]

    return response
}


// Delete a link
export async function serveDeleteLink(
    id: string
): Promise<Response<InterfaceLink>> {
    const response = await API<InterfaceLink>(
        `${BACKEND.LINKS}/${id}`,
        {},
        { method: 'DELETE' }
    )

    if (!response.success) {
        throw new Error(response.message)
    }
    
    return response
}

export async function serveRestoreLink(id: string): Promise<Response<InterfaceLink>> {
    const response = await API<InterfaceLink>(`${BACKEND.LINKS}/${id}/restore`, {}, { method: 'PATCH' })
    if (!response.success) throw new Error(response.message)
    response.data = servePrepareLinks([response.data])[0]
    return response
}

export async function servePermanentDeleteLink(id: string): Promise<Response<null>> {
    const response = await API<null>(`${BACKEND.LINKS}/${id}/permanent`, {}, { method: 'DELETE' })
    if (!response.success) throw new Error(response.message)
    return response
}


// View a link
export async function serveViewLink(
    id: string
): Promise<Response<InterfaceLink>> {
    const response = await API<InterfaceLink>(
        `${BACKEND.LINKS}/${id}`,
        {},
        { method: 'GET' }
    )

    if (!response.success) {
        throw new Error(response.message)
    }

    response.data = servePrepareLinks([response.data])[0]

    return response
}


export async function serveLinks(filters?: InterfaceLinkFilters): Promise<Response<InterfaceLink[]>> {
    // Build the path with query parameters
    let path = BACKEND.LINKS; // This is '/dashboard/links'
    
    if (filters) {
        const params = new URLSearchParams();
        
        // Add all filter parameters that are actually used
        if (filters.q) params.append('q', filters.q);
        if (filters.ascen !== undefined) params.append('ascen', String(filters.ascen));
        if (filters.sort_by && filters.sort_by !== 'updated_at') params.append('sort_by', filters.sort_by);
        if (filters.status) params.append('status', filters.status);
        if (filters.limit && filters.limit > 0) params.append('limit', String(filters.limit));
        
        const queryString = params.toString();
        if (queryString) {
            path += `?${queryString}`;
        }
    }

    console.log('Request path:', path); // Should log: /dashboard/links?q=test&status=active
    
    const response = await API<InterfaceLink[]>(
        path,
        {},
        { method: 'GET' }
    )

    if (!response.success) {
        throw new Error(response.message)
    }

    response.data = servePrepareLinks(response.data)

    return response
}


// Verify a link
export async function serveVerifyLink(
    slug: string,
    access_code?: string
): Promise<Response<{ destination_link: string }>> {
    const response = await API<{ destination_link: string }>(
        BACKEND.DASHBOARD.VERIFY(encodeURIComponent(slug)),
        access_code ? { access_code } : {},
        { method: 'POST' }
    )

    if (!response.success) {
        throw new Error(response.message)
    }

    return response
}


export async function serveIsSecured(
    slug: string,
): Promise<Response<{ is_secured: boolean }>> {
    const response = await API<{ is_secured: boolean }>(
        BACKEND.IS_SECURED(encodeURIComponent(slug)),
        {},
        { method: 'GET' }
    )

    if (!response.success) {
        throw new Error(response.message)
    }

    return response
}
