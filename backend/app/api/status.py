from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.status_interaction import StatusPost, InteractionStat
from app.models.reaction import Reaction
from app.schemas.status import StatusCreate, StatusResponse, ReactionRequest
from app.utils.wechat import get_current_user

router = APIRouter(prefix="/api/statuses", tags=["status"])


def _get_like_count(post_id: int, db: Session) -> int:
    return db.query(Reaction).filter(Reaction.post_id == post_id).count()


def _format_post(post: StatusPost, user: User, db: Session) -> StatusResponse:
    creator = db.query(User).filter(User.id == post.user_id).first()
    return StatusResponse(
        id=post.id,
        user_id=post.user_id,
        nickname=creator.nickname if creator else "",
        avatar=creator.avatar if creator else None,
        type=post.type,
        content=post.content,
        is_pinned=bool(post.is_pinned),
        like_count=_get_like_count(post.id, db),
        created_at=post.created_at,
    )


@router.get("")
async def list_statuses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """动态状态条 - 所有用户的公开状态"""
    from app.models.friend import Friend, FriendStatus
    from sqlalchemy import or_

    # 好友列表
    friendships = db.query(Friend).filter(
        or_(
            Friend.user_a_id == current_user.id,
            Friend.user_b_id == current_user.id,
        ),
        Friend.status == FriendStatus.ACCEPTED.value,
    ).all()
    friend_ids = set()
    for f in friendships:
        friend_ids.add(f.user_a_id)
        friend_ids.add(f.user_b_id)
    friend_ids.add(current_user.id)  # 包含自己

    posts = (
        db.query(StatusPost)
        .filter(StatusPost.user_id.in_(friend_ids))
        .order_by(StatusPost.is_pinned.desc(), StatusPost.created_at.desc())
        .limit(50)
        .all()
    )

    result = [_format_post(p, current_user, db) for p in posts]
    return {"code": 0, "data": result, "message": "ok"}


@router.post("")
async def create_status(
    body: StatusCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """发布动态"""
    if len(body.content) > 500:
        raise HTTPException(status_code=400, detail="内容不能超过500字")

    post = StatusPost(
        user_id=current_user.id,
        type=body.type,
        content=body.content,
        is_pinned=1 if body.is_pinned else 0,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return {"code": 0, "data": {"id": post.id}, "message": "发布成功"}


@router.delete("/{post_id}")
async def delete_status(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """删除自己的动态"""
    post = db.query(StatusPost).filter(StatusPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="动态不存在")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权删除")
    db.delete(post)
    db.commit()
    return {"code": 0, "message": "已删除"}


@router.post("/react")
async def react_to_post(
    body: ReactionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """点赞/反应动态"""
    post = db.query(StatusPost).filter(StatusPost.id == body.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="动态不存在")

    existing = db.query(Reaction).filter(
        Reaction.post_id == body.post_id,
        Reaction.user_id == current_user.id,
    ).first()
    if existing:
        # 取消点赞
        db.delete(existing)
        db.commit()
        return {"code": 0, "message": "已取消", "data": {"liked": False}}
    else:
        reaction = Reaction(post_id=body.post_id, user_id=current_user.id, type=body.type)
        db.add(reaction)
        db.commit()
        return {"code": 0, "message": "点赞成功", "data": {"liked": True}}
