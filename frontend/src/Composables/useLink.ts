import { ROUTES } from "@/Services/Routes";

export function getShareableLink(slug: string) {
    return window.location.host + (import.meta.env.VITE_BASE=='/' ? '' : import.meta.env.VITE_BASE) + ROUTES.VISIT.replace(':slug', encodeURIComponent(slug))
}
