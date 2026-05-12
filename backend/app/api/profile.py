from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.profile import Profile
from app.schemas.profile import ProfileResponse, ProfileUpdate
from app.utils.wechat import get_current_user

router = APIRouter(prefix="/api/profile", tags=["profile"])


def _get_or_create_profile(user_id: int, db: Session) -> Profile:
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not profile:
        profile = Profile(user_id=user_id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile


@router.get("", response_model=ProfileResponse)
async def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = _get_or_create_profile(current_user.id, db)
    return profile


@router.put("", response_model=ProfileResponse)
async def update_profile(
    body: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = _get_or_create_profile(current_user.id, db)

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(profile, field, value)

    profile.version += 1
    db.commit()
    db.refresh(profile)
    return profile


@router.post("/voice")
async def voice_input(
    current_user: User = Depends(get_current_user),
):
    return {
        "code": 0,
        "message": "待对接阿里云语音识别API",
        "data": None,
    }


@router.post("/document")
async def document_upload(
    current_user: User = Depends(get_current_user),
):
    return {
        "code": 0,
        "message": "待对接文档解析服务",
        "data": None,
    }
