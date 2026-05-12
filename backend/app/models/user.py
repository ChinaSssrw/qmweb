from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.database import Base


class UserRole(str, enum.Enum):
    NORMAL = "normal"
    MEMBER = "member"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


class UserStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BANNED = "banned"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    wx_openid = Column(String(128), unique=True, index=True, nullable=False)
    nickname = Column(String(64), nullable=False)
    avatar = Column(String(512), nullable=True)
    phone = Column(String(20), nullable=True)
    role = Column(String(20), default=UserRole.NORMAL.value)
    status = Column(String(20), default=UserStatus.ACTIVE.value)
    referrer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    referrer = relationship("User", remote_side=[id], backref="referrals")
    profile = relationship("Profile", uselist=False, back_populates="user")
