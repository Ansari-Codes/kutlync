from __future__ import annotations

import sqlite3
import time
from datetime import datetime
from collections import defaultdict
from urllib.parse import urlparse

from fastapi import APIRouter, Depends, Header, Path, Request, Response, status

from Routers.Auth.middlewares import current_user_id
from Routers.Links.database import (
    create_link,
    expire_link,
    get_link,
    get_link_by_slug,
    list_links,
    update_link,
    is_link_secured,
    get_raw_link,
)
from Routers.Links.datamodels import FilterQuery, LinkRequest, VerifyRequest
from Models.Model_Link import Model_Link
from Utils.common import api_response, hash_password


links_router = APIRouter(tags=["Links"])
verification_attempts: dict[str, list[float]] = defaultdict(list)


def unauthorized(response: Response):
    response.status_code = status.HTTP_401_UNAUTHORIZED
    return api_response(False, "Unauthorized", None)


def clean_link_payload(payload: LinkRequest) -> dict:
    values = payload.model_dump(exclude_unset=True)
    for key in ("link_name", "link_description", "destination_link", "slug"):
        if key in values and values[key] is not None:
            values[key] = values[key].strip()
    return values


def normalize_destination(value: str | None) -> str | None:
    if not value:
        return None
    candidate = value.strip()
    parsed = urlparse(candidate if "://" in candidate else f"https://{candidate}")
    if parsed.scheme not in {"http", "https"} or not parsed.netloc or "." not in parsed.hostname:
        return None
    return candidate if "://" in candidate else f"https://{candidate}"

@links_router.get("/api/dashboard/links")
async def links(
    response: Response, 
    user_id: int | None = Depends(current_user_id),
    filters: FilterQuery = Depends()
):
    if not user_id:
        return unauthorized(response)
    
    links = await list_links(user_id)

    if filters.status != "deleted":
        links = [link for link in links if link.get("status") != "deleted"]
    
    if filters.q:
        query_lower = filters.q.lower()
        links = [
            link for link in links 
            if (link.get("link_name") and query_lower in link["link_name"].lower()) or
            (link.get("destination_link") and query_lower in link["destination_link"].lower()) or
            (link.get("slug") and query_lower in link["slug"].lower())
        ]
    
    if filters.status:
        links = [link for link in links if link.get("status") == filters.status]
    
    sort_by = filters.sort_by
    ascen = filters.ascen
    
    if sort_by in ["created_at", "updated_at"]:
        links.sort(
            key=lambda x: datetime.fromisoformat(x[sort_by].replace(" ", "T").replace("Z", "+00:00")) if x.get(sort_by) else datetime.min,
            reverse=not ascen
        )
    else:
        links.sort(
            key=lambda x: x.get(sort_by) if x.get(sort_by) is not None else ("" if isinstance(x.get(sort_by), str) else -1), # pyright: ignore[reportArgumentType]
            reverse=not ascen
        )
    
    if filters.limit > 0:
        links = links[:filters.limit]
    
    return api_response(True, "Links fetched successfully", links)


@links_router.post("/api/dashboard/links")
async def add_link(payload: LinkRequest, response: Response, user_id: int | None = Depends(current_user_id)):
    if not user_id:
        return unauthorized(response)
    values = clean_link_payload(payload)
    if "destination_link" in values:
        destination = normalize_destination(values["destination_link"])
        if not destination:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return api_response(False, "A valid destination link is required", None)
        values["destination_link"] = destination
    destination = normalize_destination(values.get("destination_link"))
    if not destination:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return api_response(False, "A valid destination link is required", None)
    values["destination_link"] = destination
    if not values.get("link_name"):
        values["link_name"] = urlparse(destination).hostname or "Untitled link"
    max_age = values.get("max_age_minutes")
    if max_age is not None and (not isinstance(max_age, int) or max_age <= 0):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return api_response(False, "Max age must be a positive number of minutes", None)
    values.setdefault("link_description", "")
    try:
        link = await create_link(user_id, values)
    except sqlite3.IntegrityError:
        response.status_code = status.HTTP_409_CONFLICT
        return api_response(False, "Slug already exists", None)
    return api_response(True, "Link created successfully", link)


@links_router.get("/api/dashboard/links/{link_id}")
async def view_link(link_id: int, response: Response, user_id: int | None = Depends(current_user_id)):
    if not user_id:
        return unauthorized(response)
    link = await get_link(link_id, user_id)
    if link:
        await expire_link(link_id)
        link = await get_link(link_id, user_id)
    if not link:
        response.status_code = status.HTTP_404_NOT_FOUND
        return api_response(False, "Link not found", None)
    return api_response(True, "Link fetched successfully", link)


@links_router.patch("/api/dashboard/links/{link_id}")
async def edit_link(link_id: int, payload: LinkRequest, response: Response, user_id: int | None = Depends(current_user_id)):
    if not user_id:
        return unauthorized(response)
    existing = await get_link(link_id, user_id)
    if not existing:
        response.status_code = status.HTTP_404_NOT_FOUND
        return api_response(False, "Link not found", None)
    values = clean_link_payload(payload)
    if "destination_link" in values:
        destination = normalize_destination(values["destination_link"])
        if not destination:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return api_response(False, "A valid destination link is required", None)
        values["destination_link"] = destination
    if "max_age_minutes" in values and values["max_age_minutes"] is not None and values["max_age_minutes"] <= 0:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return api_response(False, "Max age must be a positive number of minutes", None)
    try:
        link = await update_link(link_id, user_id, values)
    except sqlite3.IntegrityError:
        response.status_code = status.HTTP_409_CONFLICT
        return api_response(False, "Slug already exists", None)
    return api_response(True, "Link updated successfully", link)


@links_router.delete("/api/dashboard/links/{link_id}")
async def delete_link(link_id: int, response: Response, user_id: int | None = Depends(current_user_id)):
    if not user_id:
        return unauthorized(response)
    changed = await Model_Link.update({"status": "deleted"}, {"id": link_id, "user_id": user_id})
    if not changed:
        response.status_code = status.HTTP_404_NOT_FOUND
        return api_response(False, "Link not found", None)
    return api_response(True, "Link deleted successfully", None)


@links_router.patch("/api/dashboard/links/{link_id}/restore")
async def restore_link(link_id: int, response: Response, user_id: int | None = Depends(current_user_id)):
    if not user_id:
        return unauthorized(response)
    existing = await get_raw_link(link_id, user_id)
    if not existing or existing["status"] != "deleted":
        response.status_code = status.HTTP_404_NOT_FOUND
        return api_response(False, "Deleted link not found", None)
    expires_at = None
    if existing["max_age_minutes"] is not None:
        created = datetime.fromisoformat(existing["created_at"].replace(" ", "T").replace("Z", "+00:00")).replace(tzinfo=None)
        expires_at = created.timestamp() + existing["max_age_minutes"] * 60
    restored_status = "active" if expires_at is None or expires_at > datetime.now().timestamp() else "expired"
    await Model_Link.update({"status": restored_status, "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, {"id": link_id, "user_id": user_id})
    return api_response(True, "Link restored successfully", await get_link(link_id, user_id))


@links_router.delete("/api/dashboard/links/{link_id}/permanent")
async def permanently_delete_link(link_id: int, response: Response, user_id: int | None = Depends(current_user_id)):
    if not user_id:
        return unauthorized(response)
    changed = await Model_Link.delete({"id": link_id, "user_id": user_id})
    if not changed:
        response.status_code = status.HTTP_404_NOT_FOUND
        return api_response(False, "Deleted link not found", None)
    return api_response(True, "Link permanently deleted", None)


@links_router.get("/api/visit/is_secured")
async def link_is_secured(slug: str, response: Response):
    link = await get_link_by_slug(slug)
    if link:
        await expire_link(link['id'])
    if not link:
        response.status_code = status.HTTP_404_NOT_FOUND
        return api_response(False, "Link not found", None)
    return api_response(True, "Link fetched successfully", {'is_secured': (await is_link_secured(slug))})


@links_router.post("/api/visits/verify")
async def verify_link(slug: str, payload: VerifyRequest, request: Request, response: Response):
    link = await get_link_by_slug(slug)
    if not link or link["status"] == "deleted":
        response.status_code = status.HTTP_404_NOT_FOUND
        return api_response(False, "Link not found", None)
    if link["max_age_minutes"] is not None:
        await expire_link(link["id"])
        link = await get_link_by_slug(slug)
        if not link or link["status"] != "active":
            response.status_code = status.HTTP_410_GONE
            return api_response(False, "Link has expired", None)
    if not link["access_code_hash"]:
        await Model_Link.update({"visits": link["visits"] + 1}, {"id": link["id"]})
        return api_response(True, "Link verified", {"destination_link": link["destination_link"]})
    key = f"{request.client.host if request.client else 'unknown'}:{slug}"
    now = time.time()
    verification_attempts[key] = [stamp for stamp in verification_attempts[key] if now - stamp < 60]
    if len(verification_attempts[key]) >= 5:
        response.status_code = status.HTTP_429_TOO_MANY_REQUESTS
        return api_response(False, "Too many attempts. Try again in a minute", None)
    verification_attempts[key].append(now)
    if not payload.access_code or hash_password(payload.access_code) != link["access_code_hash"]:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return api_response(False, "Invalid access code", None)
    await Model_Link.update({"visits": link["visits"] + 1}, {"id": link["id"]})
    return api_response(True, "Link verified", {"destination_link": link["destination_link"]})
