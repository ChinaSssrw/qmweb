from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.status_interaction import InteractionStat
from app.models.friend import Friend, FriendStatus
from app.models.activity import ActivityParticipant
from app.models.user_stats import UserStats
from app.schemas.stats import InteractionStatsResponse, PointsLogEntry
from app.utils.wechat import get_current_user

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("/interactions")
async def get_interaction_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """与我互动最多的用户"""
    stats = (
        db.query(InteractionStat)
        .filter(
            (InteractionStat.user_a_id == current_user.id) | (InteractionStat.user_b_id == current_user.id)
        )
        .order_by(InteractionStat.co_occurrence_count.desc())
        .limit(20)
        .all()
    )

    result = []
    for s in stats:
        other_id = s.user_b_id if s.user_a_id == current_user.id else s.user_a_id
        other_user = db.query(User).filter(User.id == other_id).first()
        result.append({
            "user_id": other_id,
            "nickname": other_user.nickname if other_user else "未知",
            "co_occurrence_count": s.co_occurrence_count,
            "details": s.details or [],
        })

    return {"code": 0, "data": result, "message": "ok"}


@router.get("/points-log")
async def get_points_log(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """积分变动记录"""
    stats = db.query(UserStats).filter(UserStats.user_id == current_user.id).first()
    if not stats or not stats.points_log:
        return {"code": 0, "data": [], "message": "ok"}

    sorted_log = sorted(stats.points_log, key=lambda x: x.get("created_at", ""), reverse=True)
    return {"code": 0, "data": sorted_log, "message": "ok"}


@router.get("/summary")
async def get_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """我的行为汇总"""
    stats = db.query(UserStats).filter(UserStats.user_id == current_user.id).first()

    friend_count = db.query(Friend).filter(
        (Friend.user_a_id == current_user.id) | (Friend.user_b_id == current_user.id),
        Friend.status == FriendStatus.ACCEPTED.value,
    ).count()

    activity_count = db.query(ActivityParticipant).filter(
        ActivityParticipant.user_id == current_user.id
    ).count()

    return {
        "code": 0,
        "data": {
            "points": stats.points if stats else 0,
            "credit_score": stats.credit_score if stats else 100,
            "level": stats.level if stats else 1,
            "friend_count": friend_count,
            "activity_count": activity_count,
        },
        "message": "ok",
    }
