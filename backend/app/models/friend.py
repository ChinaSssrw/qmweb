import enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SAEnum
from datetime import datetime

from app.database import Base


class FriendStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class FriendSource(str, enum.Enum):
    DIRECT = "direct"
    ACTIVITY = "activity"


class Friend(Base):
    __tablename__ = "friends"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_a_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    user_b_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    status = Column(String(20), default=FriendStatus.PENDING.value)
    source = Column(String(20), default=FriendSource.DIRECT.value)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
