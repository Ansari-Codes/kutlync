from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from Models.Model_Link import Model_Link
from Utils.common import hash_password

LINK_FIELDS = "id, link_name, link_description, destination_link, slug, visits, max_age_minutes, created_at, updated_at, status"
RAW_LINK_FIELDS = LINK_FIELDS + ", access_code_hash"


def public_link(link: dict[str, Any] | None) -> dict[str, Any] | None:
    if link is None:
        return None
    result = {key: value for key, value in link.items() if key != "access_code_hash"}
    result["is_secured"] = bool(link.get("access_code_hash"))
    return result


async def expire_link(link_id: int) -> None:
    link = await get_link(link_id)
    if not link: return
    current_status = link["status"]
    if current_status == "deleted": return
    if link["max_age_minutes"] is None: return
    created = datetime.fromisoformat(link["created_at"].replace(" ", "T").replace("Z", "+00:00"))
    if created.tzinfo is None:
        created = created.replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    age_seconds = (now - created).total_seconds()
    max_age_seconds = link["max_age_minutes"] * 60
    if age_seconds >= max_age_seconds: new_status = "expired"
    else: new_status = "active"
    if current_status == new_status: return
    await Model_Link.update({"status": new_status,"updated_at": now.strftime("%Y-%m-%d %H:%M:%S")},{"id": link_id})

async def expire_user_links(user_id: int) -> None:
    links = await Model_Link.select(where={"user_id": user_id})
    for link in links:
        await expire_link(link["id"])


async def get_link(link_id: int, user_id: int | None = None) -> dict[str, Any] | None:
    where = {"id": link_id}
    if user_id is not None:
        where["user_id"] = user_id
    links = await Model_Link.select(columns=RAW_LINK_FIELDS, where=where, limit=1)
    return public_link(links[0]) if links else None


async def get_raw_link(link_id: int, user_id: int | None = None) -> dict[str, Any] | None:
    where = {"id": link_id}
    if user_id is not None:
        where["user_id"] = user_id
    links = await Model_Link.select(columns=RAW_LINK_FIELDS, where=where, limit=1)
    return links[0] if links else None


async def get_link_by_slug(slug: str) -> dict[str, Any] | None:
    links = await Model_Link.select(columns=RAW_LINK_FIELDS, where={"slug": slug}, limit=1)
    return links[0] if links else None


async def is_link_secured(identifier: str, by: "id"|"slug" = "slug") -> bool | None:
    val = await Model_Link.select(columns="access_code_hash", where={by: identifier}, limit=1)
    return bool(val[0]['access_code_hash'])


async def list_links(user_id: int) -> list[dict[str, Any]]:
    await expire_user_links(user_id)
    links = await Model_Link.select(columns=RAW_LINK_FIELDS, where={"user_id": user_id})
    return [public_link(link) for link in links]  # type: ignore[misc]

async def dashboard_stats(user_id: int) -> dict[str, Any]:
    links = await list_links(user_id)
    now = datetime.now(timezone.utc)

    active = [link for link in links if link["status"] == "active"]
    expired = [link for link in links if link["status"] == "expired"]
    deleted = [link for link in links if link["status"] == "deleted"]
    
    recent = sorted(links, key=lambda link: link["updated_at"], reverse=True)[:5]

    # Calculate near expiry links (active links expiring within 5 minutes)
    def age_minutes(link: dict[str, Any]) -> float | None:
        if link.get("max_age_minutes") is None:
            return None
        created = datetime.fromisoformat(link["created_at"].replace(" ", "T").replace("Z", "+00:00"))
        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)
        return (created.timestamp() + link["max_age_minutes"] * 60 - now.timestamp()) / 60

    near_expiry = [
        link for link in active 
        if (age := age_minutes(link)) is not None and 0 < age < 5
    ]
    near_expiry.sort(key=lambda link: age_minutes(link) or 0)

    result = {
        "total_links": len(active),
        "total_visits": sum(link["visits"] for link in active),
        "expired_links": len(expired),
        "deleted_links": len(deleted),
        "recent_links": recent,
        "near_expiry_links": near_expiry[:3],  # Limit to 3 near-expiry links
    }
    
    return result


async def create_link(user_id: int, values: dict[str, Any]) -> dict[str, Any]:
    values["user_id"] = user_id
    if values.get("access_code"):
        values["access_code_hash"] = hash_password(values.pop("access_code"))
    else:
        values.pop("access_code", None)
        values["access_code_hash"] = None
    requested_slug = values.pop("slug", None)
    values["slug"] = requested_slug or f"pending-{datetime.now(timezone.utc).timestamp()}"
    link_id = await Model_Link.insert(values)
    if not requested_slug:
        await Model_Link.update({"slug": f"link{link_id}"}, {"id": link_id})
    return await get_link(link_id)  # type: ignore[return-value]

from datetime import datetime as dt

async def update_link(link_id: int, user_id: int, values: dict[str, Any]) -> dict[str, Any] | None:
    security_action = values.pop("security_action", "keep")
    access_code = values.pop("access_code", None)
    if security_action == "remove":
        values["access_code_hash"] = None
    elif security_action == "update":
        values["access_code_hash"] = hash_password(access_code) if access_code else None
    values["updated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    await Model_Link.update(values, {"id": link_id, "user_id": user_id})
    await expire_link(link_id)
    return await get_link(link_id)
