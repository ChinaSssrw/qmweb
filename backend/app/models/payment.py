import enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SAEnum
from datetime import datetime

from app.database import Base


class PaymentType(str, enum.Enum):
    MEMBERSHIP = "membership"
    SPACE = "space"


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    REFUNDED = "refunded"
    FAILED = "failed"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    type = Column(String(20), default=PaymentType.MEMBERSHIP.value)
    amount = Column(Integer, default=0)  # 单位：分
    order_no = Column(String(64), unique=True, nullable=False)
    wx_pay_no = Column(String(64), nullable=True)
    status = Column(String(20), default=PaymentStatus.PENDING.value)
    paid_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
