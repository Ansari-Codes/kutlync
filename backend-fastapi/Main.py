from __future__ import annotations

import os

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Db import DefineTable
from Routers.Auth.route import auth_router
from Routers.Links.route import links_router
from Routers.Links.database import dashboard_stats as get_dashboard_stats
from Routers.Auth.middlewares import current_user_id
from Utils.common import api_response

DefineTable()

app = FastAPI(title="KutLynk API")

origins = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "*").split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
@app.get("/api/health")
async def health():
    return api_response(True, "Healthy", {"status": "ok"})


@app.get("/api/dashboard/stats")
async def user_dashboard_stats(user_id: int | None = Depends(current_user_id)):
    if not user_id:
        return api_response(False, "Unauthorized", None)
    return api_response(True, "Dashboard stats fetched", await get_dashboard_stats(user_id))


app.include_router(auth_router)
app.include_router(links_router)
