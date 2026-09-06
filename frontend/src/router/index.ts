import { createRouter, createWebHistory } from 'vue-router'

import PageMain from '@/Pages/PageMain.vue'
import PageVisit from '@/Pages/PageVisit.vue'
import PageLogin from '@/Pages/Auth/PageLogin.vue'
import PageSignup from '@/Pages/Auth/PageSignup.vue'
import PageDashboard from '@/Pages/Dashboard/Index.vue'

import { ROUTES } from '@/Services/Routes'
import { serveIsAuthenticated } from '@/Services/Auth.serve'

const dashboardPages = [
    {
        path: ROUTES.DASHBOARD.HOME,
        name: 'dashboard',
        component: () => import('@/Pages/Dashboard/Dashboard.vue'),
        meta: { title: 'Dashboard' }
    },
    {
        path: ROUTES.DASHBOARD.LINKS,
        name: 'links',
        component: () => import('@/Pages/Dashboard/Links.vue'),
        meta: { title: 'Links' }
    },
    {
        path: 'link',
        name: 'new-link',
        component: () => import('@/Pages/Dashboard/Links.vue'),
        meta: { title: 'New Link' }
    },
    {
        path: ROUTES.DASHBOARD.ANALYTICS,
        name: 'analytics',
        component: () => import('@/Pages/Dashboard/Analytics.vue'),
        meta: { title: 'Analytics' }
    },
    {
        path: ROUTES.DASHBOARD.BILLING,
        name: 'billing',
        component: () => import('@/Pages/Dashboard/Billings.vue'),
        meta: { title: 'Billings' }
    },
    {
        path: ROUTES.DASHBOARD.SETTINGS,
        name: 'settings',
        component: () => import('@/Pages/Dashboard/Settings.vue'),
        meta: { title: 'Settings' }
    }
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'main',
            component: PageMain
        },
        {
            path: ROUTES.VISIT,
            name: 'visit',
            props: true,
            component: PageVisit
        },
        {
            path: ROUTES.AUTH.BASE,
            children: [
                {
                    path: ROUTES.AUTH.SIGNUP,
                    name: 'signup',
                    component: PageSignup,
                    meta: {
                        guest: true,
                        redirect: ROUTES.DASHBOARD.BASE
                    }
                },
                {
                    path: ROUTES.AUTH.LOGIN,
                    name: 'login',
                    component: PageLogin,
                    meta: {
                        guest: true,
                        redirect: ROUTES.DASHBOARD.BASE
                    }
                }
            ]
        },
        {
            path: ROUTES.DASHBOARD.BASE,
            name: 'dashboard-base',
            component: PageDashboard,
            meta: { guest: false, redirect: ROUTES.AUTH.LOGIN },
            children: dashboardPages
        },
        {
            path: '/:pathMatch(.*)*',
            redirect: '/'
        }
    ]
})

router.beforeEach((to) => {
    const isAuthed = serveIsAuthenticated()

    const requiresAuth = to.matched.some(
        record => record.meta.guest === false
    )

    const guestOnly = to.matched.some(
        record => record.meta.guest === true
    )

    if (requiresAuth && !isAuthed) {
        return ROUTES.AUTH.LOGIN
    }

    if (guestOnly && isAuthed) {
        return ROUTES.DASHBOARD.BASE
    }

    return true
})

export default router
