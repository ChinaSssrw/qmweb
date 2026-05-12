from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.profile import router as profile_router
from app.api.friend import router as friend_router

app = FastAPI(title="企盟小程序 API", version="1.0.0")

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(friend_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
