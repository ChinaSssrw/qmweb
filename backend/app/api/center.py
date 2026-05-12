from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User, UserRole
from app.models.profile import Profile
from app.models.friend import Friend, FriendStatus
from app.models.activity import Activity, ActivityParticipant
from app.models.user_stats import UserStats
from app.schemas.center import UserStatsResponse
from app.utils.wechat import get_current_user

router = APIRouter(prefix="/api/center", tags=["center"])


def _get_or_create_stats(user_id: int, db: Session) -> UserStats:
    stats = db.query(UserStats).filter(UserStats.user_id == user_id).first()
    if not stats:
        stats = UserStats(user_id=user_id)
        db.add(stats)
        db.commit()
        db.refresh(stats)
    return stats


@router.get("/stats")
async def get_center_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """个人中心 - 统计信息"""
    stats = _get_or_create_stats(current_user.id, db)

    friend_count = db.query(Friend).filter(
        (Friend.user_a_id == current_user.id) | (Friend.user_b_id == current_user.id),
        Friend.status == FriendStatus.ACCEPTED.value,
    ).count()

    activity_count = db.query(ActivityParticipant).filter(
        ActivityParticipant.user_id == current_user.id
    ).count()

    return {
        "code": 0,
        "data": UserStatsResponse(
            user_id=current_user.id,
            points=stats.points,
            credit_score=stats.credit_score,
            level=stats.level,
            achievements=stats.achievements or [],
            friend_count=friend_count,
            activity_count=activity_count,
            points_log=stats.points_log or [],
        ),
        "message": "ok",
    }


@router.get("/achievements")
async def get_achievements(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """我的成就徽章"""
    stats = _get_or_create_stats(current_user.id, db)
    return {"code": 0, "data": stats.achievements or [], "message": "ok"}
