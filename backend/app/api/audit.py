from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.user import User, UserRole
from app.models.audit import AuditRecord
from app.schemas.audit import AuditApplyRequest, AuditReviewRequest, AuditStatusResponse
from app.utils.wechat import get_current_user

router = APIRouter(prefix="/api/audit", tags=["audit"])


@router.get("/status")
async def get_audit_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """查询当前审核状态"""
    record = db.query(AuditRecord).filter(AuditRecord.user_id == current_user.id).first()
    if not record:
        return {
            "code": 0,
            "data": {"referrer_status": "none", "admin_status": "none", "reject_reason": None},
            "message": "ok",
        }
    return {"code": 0, "data": AuditStatusResponse.model_validate(record), "message": "ok"}


@router.post("/apply")
async def apply_audit(
    body: AuditApplyRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """提交审核申请（推荐人+管理员两级）"""
    existing = db.query(AuditRecord).filter(AuditRecord.user_id == current_user.id).first()
    if existing:
        if existing.admin_status == "pending" or existing.referrer_status == "pending":
            raise HTTPException(status_code=400, detail="已有审核中的申请")

    record = AuditRecord(
        user_id=current_user.id,
        referrer_id=current_user.referrer_id,
    )
    if current_user.referrer_id:
        record.referrer_status = "pending"
    db.add(record)
    db.commit()
    return {"code": 0, "message": "审核申请已提交", "data": None}


@router.get("/pending")
async def list_pending(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """管理员/推荐人 - 查看待审核列表"""
    records = []

    # 推荐人待审
    if current_user.referrals:
        ref_pending = db.query(AuditRecord).filter(
            AuditRecord.referrer_id == current_user.id,
            AuditRecord.referrer_status == "pending",
        ).all()
        records.extend(ref_pending)

    # 管理员待审
    if current_user.role in (UserRole.ADMIN.value, UserRole.SUPER_ADMIN.value):
        admin_pending = db.query(AuditRecord).filter(
            AuditRecord.admin_status == "pending",
        ).all()
        records.extend(admin_pending)

    # 去重
    seen = set()
    unique = []
    for r in records:
        if r.id not in seen:
            seen.add(r.id)
            user = db.query(User).filter(User.id == r.user_id).first()
            unique.append({
                "audit_id": r.id,
                "user_id": r.user_id,
                "nickname": user.nickname if user else "未知",
                "referrer_status": r.referrer_status,
                "admin_status": r.admin_status,
                "applied_at": r.applied_at.isoformat(),
            })

    return {"code": 0, "data": unique, "message": "ok"}


@router.post("/review")
async def review_audit(
    body: AuditReviewRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """审核（推荐人或管理员）"""
    record = db.query(AuditRecord).filter(AuditRecord.user_id == body.user_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="审核记录不存在")

    # 推荐人审核
    if record.referrer_id == current_user.id and record.referrer_status == "pending":
        record.referrer_status = "approved" if body.action == "approve" else "rejected"

    # 管理员审核
    elif current_user.role in (UserRole.ADMIN.value, UserRole.SUPER_ADMIN.value) and record.admin_status == "pending":
        record.admin_status = "approved" if body.action == "approve" else "rejected"

    else:
        raise HTTPException(status_code=403, detail="无权审核或已审核")

    if body.action == "reject" and body.reject_reason:
        record.reject_reason = body.reject_reason

    if body.action == "reject":
        record.completed_at = datetime.utcnow()

    # 两级都通过 → 提升为 member
    if record.referrer_status == "approved" and record.admin_status == "approved":
        user = db.query(User).filter(User.id == body.user_id).first()
        if user:
            user.role = UserRole.MEMBER.value
        record.completed_at = datetime.utcnow()

    db.commit()
    action_text = "通过" if body.action == "approve" else "驳回"
    return {"code": 0, "message": f"已{action_text}", "data": None}
