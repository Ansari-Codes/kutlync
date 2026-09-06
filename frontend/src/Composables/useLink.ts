import { ROUTES } from "@/Services/Routes";

export function getShareableLink(slug: string) {
    return window.location.host + ROUTES.VISIT.replace(':slug', encodeURIComponent(slug))
}
