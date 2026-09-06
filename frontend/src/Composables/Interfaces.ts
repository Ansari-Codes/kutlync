import { ROUTES } from "@/Services/Routes"

export interface InterfaceDashboardSidebar {
    name: string
    icon: string
    target: typeof ROUTES.DASHBOARD[keyof typeof ROUTES.DASHBOARD]
}


