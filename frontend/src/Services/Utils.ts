import type { InterfaceLinkFilters } from "./Interfaces";

export function validateUserName(username: string):boolean {
    return username.length > 0
}
export function validateEmail(email: string):boolean {
    return email.length > 0 && email.includes('@')
}
export function validatePassword(password: string):boolean {
    return password.length > 6
}
export function filtersToQueryParams(filters: InterfaceLinkFilters): URLSearchParams {
    const params = new URLSearchParams();
    
    if (filters.query) params.append('q', filters.query);
    if (filters.ascen !== undefined) params.append('ascen', String(filters.ascen));
    if (filters.sort_by) params.append('sort_by', filters.sort_by);
    if (filters.created_range_start) params.append('created_from', filters.created_range_start);
    if (filters.created_range_end) params.append('created_to', filters.created_range_end);
    if (filters.updated_range_start) params.append('updated_from', filters.updated_range_start);
    if (filters.updated_range_end) params.append('updated_to', filters.updated_range_end);
    if (filters.max_age_minutes_min) params.append('max_age_from', filters.max_age_minutes_min);
    if (filters.max_age_minutes_max) params.append('max_age_to', filters.max_age_minutes_max);
    if (filters.visits_range !== null && filters.visits_range !== undefined) params.append('visits_min', String(filters.visits_range));
    if (filters.status) params.append('status', filters.status);
    if (filters.limit && filters.limit > 0) params.append('limit', String(filters.limit));
    
    return params;
}
