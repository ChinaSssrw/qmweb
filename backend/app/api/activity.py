from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from datetime import datetime

from app.database import get_db
from app.models.user import User
from app.models.activity import Activity, ActivityParticipant
from app.schemas.activity import ActivityCreate, ActivityUpdate, ActivityResponse, ActivityRegisterRequest
from app.utils.wechat import get_current_user

router = APIRouter(prefix="/api/activities", tags=["activity"])


@router.get("")
async def list_activities(
    status: str = Query("published", description="draft/published/cancelled/completed"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """活动广场列表"""
    query = db.query(Activity).options(joinedload(Activity.participants)).filter(Activity.status == status)
    total = query.count()
    activities = query.order_by(Activity.start_time.asc()).offset((page - 1) * page_size).limit(page_size).all()

    result = []
    for a in activities:
        result.append(ActivityResponse(
            id=a.id,
            creator_id=a.creator_id,
            title=a.title,
            description=a.description,
            start_time=a.start_time,
            end_time=a.end_time,
            location=a.location,
            max_participants=a.max_participants,
            registration_deadline=a.registration_deadline,
            cover_image=a.cover_image,
            status=a.status,
            participant_count=len(a.participants),
            created_at=a.created_at,
        ))

    return {"code": 0, "data": {"items": result, "total": total, "page": page}, "message": "ok"}


@router.post("")
async def create_activity(
    body: ActivityCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """创建活动"""
    activity = Activity(
        creator_id=current_user.id,
        title=body.title,
        description=body.description,
        start_time=body.start_time,
        end_time=body.end_time,
        location=body.location,
        max_participants=body.max_participants,
        registration_deadline=body.registration_deadline,
        cover_image=body.cover_image,
    )
    # 无需审核直接发布
    activity.status = "published"
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return {"code": 0, "data": {"id": activity.id}, "message": "ok"}


@router.get("/{activity_id}")
async def get_activity(
    activity_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """活动详情"""
    activity = db.query(Activity).options(joinedload(Activity.participants)).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="活动不存在")

    is_registered = db.query(ActivityParticipant).filter(
        ActivityParticipant.activity_id == activity_id,
        ActivityParticipant.user_id == current_user.id,
    ).first() is not None

    return {
        "code": 0,
        "data": {
            "id": activity.id,
            "creator_id": activity.creator_id,
            "title": activity.title,
            "description": activity.description,
            "start_time": activity.start_time.isoformat(),
            "end_time": activity.end_time.isoformat(),
            "location": activity.location,
            "max_participants": activity.max_participants,
            "registration_deadline": activity.registration_deadline.isoformat() if activity.registration_deadline else None,
            "cover_image": activity.cover_image,
            "status": activity.status,
            "participant_count": len(activity.participants),
            "is_registered": is_registered,
            "created_at": activity.created_at.isoformat(),
        },
        "message": "ok",
    }


@router.put("/{activity_id}")
async def update_activity(
    activity_id: int,
    body: ActivityUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """更新活动（仅创建者）"""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="活动不存在")
    if activity.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权修改此活动")

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(activity, field, value)
    db.commit()
    return {"code": 0, "message": "ok"}


@router.post("/register")
async def register_activity(
    body: ActivityRegisterRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """报名活动"""
    activity = db.query(Activity).filter(Activity.id == body.activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="活动不存在")
    if activity.status != "published":
        raise HTTPException(status_code=400, detail="活动未开放报名")

    existing = db.query(ActivityParticipant).filter(
        ActivityParticipant.activity_id == body.activity_id,
        ActivityParticipant.user_id == current_user.id,
    ).first()
    if existing:
        return {"code": 0, "message": "已报名", "data": None}

    current_count = db.query(ActivityParticipant).filter(
        ActivityParticipant.activity_id == body.activity_id
    ).count()
    if activity.max_participants > 0 and current_count >= activity.max_participants:
        raise HTTPException(status_code=400, detail="名额已满")

    participant = ActivityParticipant(activity_id=body.activity_id, user_id=current_user.id)
    db.add(participant)
    db.commit()

    return {"code": 0, "message": "报名成功", "data": None}


@router.post("/{activity_id}/checkin")
async def checkin_activity(
    activity_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """签到"""
    participant = db.query(ActivityParticipant).filter(
        ActivityParticipant.activity_id == activity_id,
        ActivityParticipant.user_id == current_user.id,
    ).first()
    if not participant:
        raise HTTPException(status_code=400, detail="未报名此活动")
    if participant.has_checked_in:
        return {"code": 0, "message": "已签到", "data": None}

    participant.has_checked_in = 1
    participant.checkin_time = datetime.utcnow()
    db.commit()
    return {"code": 0, "message": "签到成功", "data": None}
