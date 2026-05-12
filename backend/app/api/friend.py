from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.friend import Friend, FriendStatus, FriendSource
from app.schemas.user import UserResponse
from app.utils.wechat import get_current_user

router = APIRouter(prefix="/api/friends", tags=["friends"])


class FriendRequest(BaseModel):
    user_id: int


class FriendResponse(BaseModel):
    id: int
    user: UserResponse
    status: str
    source: str
    activity_id: Optional[int] = None
    created_at: datetime

    model_config = {"from_attributes": True}


@router.get("")
async def list_friends(
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(Friend).filter(
        or_(Friend.user_a_id == current_user.id, Friend.user_b_id == current_user.id)
    )
    if status:
        query = query.filter(Friend.status == status)
    friends = query.order_by(Friend.created_at.desc()).all()

    result = []
    for f in friends:
        other_user = (
            db.query(User)
            .filter(
                User.id == (f.user_b_id if f.user_a_id == current_user.id else f.user_a_id)
            )
            .first()
        )
        if other_user:
            result.append({
                "id": f.id,
                "user": UserResponse.model_validate(other_user),
                "status": f.status,
                "source": f.source,
                "activity_id": f.activity_id,
                "created_at": f.created_at,
            })
    return {"code": 0, "data": result, "message": "ok"}


@router.post("/request")
async def send_request(
    body: FriendRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if body.user_id == current_user.id:
        raise HTTPException(status_code=400, detail="不能加自己为好友")

    target = db.query(User).filter(User.id == body.user_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="用户不存在")

    existing = (
        db.query(Friend)
        .filter(
            or_(
                (Friend.user_a_id == current_user.id) & (Friend.user_b_id == body.user_id),
                (Friend.user_a_id == body.user_id) & (Friend.user_b_id == current_user.id),
            )
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="已发送过好友申请")

    # 防骚扰检查：1小时内加好友>20且通过率<30%
    one_hour_ago = datetime.utcnow() - timedelta(hours=1)
    recent_requests = (
        db.query(Friend)
        .filter(
            Friend.user_a_id == current_user.id,
            Friend.created_at >= one_hour_ago,
        )
        .count()
    )
    if recent_requests >= 20:
        accepted = (
            db.query(Friend)
            .filter(
                Friend.user_a_id == current_user.id,
                Friend.status == FriendStatus.ACCEPTED.value,
            )
            .count()
        )
        total = (
            db.query(Friend)
            .filter(Friend.user_a_id == current_user.id)
            .count()
        )
        if total > 0 and (accepted / total) < 0.3:
            return {
                "code": 1001,
                "message": "操作频繁，请稍后再试（防骚扰机制触发）",
                "data": None,
            }

    friend = Friend(
        user_a_id=current_user.id,
        user_b_id=body.user_id,
        status=FriendStatus.PENDING.value,
    )
    db.add(friend)
    db.commit()

    return {"code": 0, "message": "好友申请已发送", "data": {"id": friend.id}}


@router.post("/accept")
async def accept_request(
    body: FriendRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    friend = (
        db.query(Friend)
        .filter(
            Friend.user_a_id == body.user_id,
            Friend.user_b_id == current_user.id,
            Friend.status == FriendStatus.PENDING.value,
        )
        .first()
    )
    if not friend:
        raise HTTPException(status_code=404, detail="好友申请不存在")

    friend.status = FriendStatus.ACCEPTED.value
    db.commit()

    return {"code": 0, "message": "已同意好友申请", "data": None}
