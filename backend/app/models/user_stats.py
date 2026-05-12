from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from datetime import datetime

from app.database import Base


class UserStats(Base):
    __tablename__ = "user_stats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)
    points = Column(Integer, default=0)  # 积分
    credit_score = Column(Integer, default=100)  # 信用分
    level = Column(Integer, default=1)  # 等级
    achievements = Column(JSON, default=list)  # [{"id": "first_activity", "name": "首次参加活动", "earned_at": "..."}]
    points_log = Column(JSON, default=list)  # [{"points": 10, "reason": "参加活动", "created_at": "..."}]
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
