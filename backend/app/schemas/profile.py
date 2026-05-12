from typing import Optional
from pydantic import BaseModel


class ProfileUpdate(BaseModel):
    basic_info: Optional[dict] = None
    contact_info: Optional[dict] = None
    tags: Optional[dict] = None
    bio: Optional[dict] = None
    social: Optional[dict] = None
    privacy_settings: Optional[dict] = None
