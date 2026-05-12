from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class InteractionStatsResponse(BaseModel):
    user_a_id: int
    user_b_id: int
    co_occurrence_count: int = 0
    details: list = []

    model_config = {"from_attributes": True}


class PointsLogEntry(BaseModel):
    points: int
    reason: str
    created_at: datetime


class PointsLogResponse(BaseModel):
    code: int = 0
    data: list[PointsLogEntry] = []
    message: str = "ok"
