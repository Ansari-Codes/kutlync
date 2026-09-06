export interface Response<T = unknown> {
    success: boolean
    message: string
    data: T
}

export interface ValidationErrors {
    username?: string
    email?: string
    password?: string
}

export interface InterfaceUser {
    id: number | string
    username: string
    email: string
}

export interface InterfaceSignUp {
    username: string
    email: string
    password: string
}

export interface InterfaceLogIn {
    email: string
    password: string
}

export interface InterfaceAuthTokenPayload {
    userId: number
    token: string
}

export interface AuthResult {
    success: boolean
    message?: string
    validation?: ValidationErrors
}

export interface InterfaceHomeStats {
    total_links: number,
    total_users: number,
    total_visits: number,
    average_links_per_day: number,
    average_visits_per_day: number
}

export interface InterfaceUserDashboardStats {
    total_links: number,
    total_visits: number,
    expired_links: number,
    deleted_links: number,
    recent_links: InterfaceLink[],
    near_expiry_links: InterfaceLink[],
}

export interface InterfaceLink {
    id: string,
    link_name: string
    link_description: string
    destination_link: string
    slug: string
    visits: number
    max_age_minutes?: number | null
    created_at: string
    updated_at: string
    status: 'active' | 'deleted' | 'expired'
    is_secured?: boolean
}

export interface InterfaceLinkInput {
    link_name?: string
    link_description?: string
    destination_link: string
    slug?: string
    access_code?: string | null
    max_age_minutes?: number | null
    security_action?: 'keep' | 'remove' | 'update'
}

export interface InterfaceLinkFilters {
    q?: string | null;
    query?: string | null;
    ascen?: boolean;
    sort_by?: 'id' | 'link_name' | 'destination_link' | 'slug' | 'visits' | 'max_age_minutes' | 'created_at' | 'updated_at' | 'status';
    status?: 'active' | 'deleted' | 'expired' | null;
    limit?: number;
    created_range_start?: string;
    created_range_end?: string;
    updated_range_start?: string;
    updated_range_end?: string;
    max_age_minutes_min?: string;
    max_age_minutes_max?: string;
    visits_range?: number | null;
}

