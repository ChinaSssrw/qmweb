from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.profile import router as profile_router
from app.api.friend import router as friend_router
from app.api.activity import router as activity_router
from app.api.status import router as status_router
from app.api.center import router as center_router
from app.api.audit import router as audit_router
from app.api.stats import router as stats_router

app = FastAPI(title="企盟小程序 API", version="1.0.0")

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(friend_router)
app.include_router(activity_router)
app.include_router(status_router)
app.include_router(center_router)
app.include_router(audit_router)
app.include_router(stats_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
