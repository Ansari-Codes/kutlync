export const BACKEND_BASE_API_URL = 'http://127.0.0.1:3333/api'

export const ROUTES = {
    HEALTH: '/health',
    AUTH: {
        BASE: '/auth',
        LOGIN: 'login',
        SIGNUP: 'signup',
        FORGOT_PASS: 'forgot-password'
    },
    DASHBOARD: {
        BASE: '/dashboard',
        HOME: '',
        LINKS: 'links',
        TRASHBOX: 'trashbox',
        SETTINGS: 'settings'
    },
    VISIT: '/s/:slug'
} as const

export const BACKEND = {
    HEALTH: '/health',
    STATS: '/stats',
    LINKS: '/dashboard/links',
    AUTH: {
        BASE: '/auth',
        LOGIN: '/auth/login',
        SIGNUP: '/auth/signup',
        FORGOT_PASS: '/auth/forgot-password'
    },
    DASHBOARD: {
        BASE: '/dashboard',
        STATS: '/dashboard/stats',
        LINKS: '/dashboard/links',
        VERIFY: (slug: string) => `/visits/verify?slug=${slug}`,
        SETTINGS: '/dashboard/settings'
    },
    IS_SECURED: (slug: string) => `/visit/is_secured?slug=${slug}`,
    ANALYTICS: '/dashboard/analytics'
} as const
