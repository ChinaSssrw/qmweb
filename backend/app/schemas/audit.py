from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AuditApplyRequest(BaseModel):
    """用户提交审核申请（企业认证）"""
    pass


class AuditReviewRequest(BaseModel):
    user_id: int
    action: str  # approve/reject
    reject_reason: Optional[str] = None


class AuditStatusResponse(BaseModel):
    referrer_status: str = "pending"
    admin_status: str = "pending"
    reject_reason: Optional[str] = None

    model_config = {"from_attributes": True}


class AuditListResponse(BaseModel):
    code: int = 0
    data: list[AuditStatusResponse] = []
    message: str = "ok"
