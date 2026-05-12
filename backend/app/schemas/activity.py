from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ActivityCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    max_participants: int = 0
    registration_deadline: Optional[datetime] = None
    cover_image: Optional[str] = None


class ActivityUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    max_participants: Optional[int] = None
    registration_deadline: Optional[datetime] = None
    cover_image: Optional[str] = None
    status: Optional[str] = None


class ActivityResponse(BaseModel):
    id: int
    creator_id: int
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    max_participants: int
    registration_deadline: Optional[datetime] = None
    cover_image: Optional[str] = None
    status: str
    participant_count: int = 0
    created_at: datetime

    model_config = {"from_attributes": True}


class ActivityRegisterRequest(BaseModel):
    activity_id: int
