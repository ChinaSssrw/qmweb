from sqlalchemy import Column, Integer, DateTime, ForeignKey, JSON
from datetime import datetime

from app.database import Base


class StatusPost(Base):
    __tablename__ = "status_posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    type = Column(String(20), default="need")  # need/provide
    content = Column(String(500), nullable=False)
    is_pinned = Column(Integer, default=0)  # 0=不置顶, 1=置顶
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class InteractionStat(Base):
    __tablename__ = "interaction_stats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_a_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    user_b_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    co_occurrence_count = Column(Integer, default=0)
    details = Column(JSON, default=list)  # [{"activity_id": 1, "time": "..."}]
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
