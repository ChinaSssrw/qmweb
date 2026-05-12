from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    location = Column(String(256), nullable=True)
    max_participants = Column(Integer, default=0)
    registration_deadline = Column(DateTime, nullable=True)
    space_id = Column(Integer, ForeignKey("spaces.id"), nullable=True)
    cover_image = Column(String(512), nullable=True)
    status = Column(String(20), default="draft")  # draft/published/cancelled/completed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    creator = relationship("User", backref="created_activities")
    participants = relationship("ActivityParticipant", back_populates="activity")


class ActivityParticipant(Base):
    __tablename__ = "activity_participants"

    id = Column(Integer, primary_key=True, autoincrement=True)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    has_checked_in = Column(Integer, default=0)  # 0=未签到, 1=已签到
    checkin_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    activity = relationship("Activity", back_populates="participants")
    user = relationship("User")
