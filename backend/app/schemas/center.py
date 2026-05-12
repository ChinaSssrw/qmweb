from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserStatsResponse(BaseModel):
    user_id: int
    points: int = 0
    credit_score: int = 100
    level: int = 1
    achievements: list = []
    friend_count: int = 0
    activity_count: int = 0
    points_log: list = []

    model_config = {"from_attributes": True}


class CenterResponse(BaseModel):
    code: int = 0
    data: UserStatsResponse
    message: str = "ok"
