from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class StatusCreate(BaseModel):
    type: str = "need"  # need/provide
    content: str
    is_pinned: bool = False


class StatusResponse(BaseModel):
    id: int
    user_id: int
    nickname: str = ""
    avatar: Optional[str] = None
    type: str
    content: str
    is_pinned: bool = False
    like_count: int = 0
    created_at: datetime

    model_config = {"from_attributes": True}


class ReactionRequest(BaseModel):
    post_id: int
    type: str = "like"


class StatusListResponse(BaseModel):
    code: int = 0
    data: list[StatusResponse] = []
    message: str = "ok"
