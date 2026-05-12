from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class ProfileResponse(BaseModel):
    basic_info: dict = {}
    contact_info: dict = {}
    tags: dict = {}
    bio: dict = {}
    social: dict = {}
    privacy_settings: dict = {}
    version: int = 1

    model_config = {"from_attributes": True}


class ProfileUpdate(BaseModel):
    basic_info: Optional[dict] = None
    contact_info: Optional[dict] = None
    tags: Optional[dict] = None
    bio: Optional[dict] = None
    social: Optional[dict] = None
    privacy_settings: Optional[dict] = None
