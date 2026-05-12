from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Space(Base):
    __tablename__ = "spaces"

    id = Column(Integer, primary_key=True, autoincrement=True)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(128), nullable=False)
    address = Column(String(256), nullable=True)
    capacity = Column(Integer, default=0)
    facilities = Column(JSON, default=list)  # ["wifi", "投影", ...]
    photos = Column(JSON, default=list)
    price_per_hour = Column(Integer, default=0)  # 单位：分
    status = Column(String(20), default="pending")  # pending/approved/rejected/offline
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    manager = relationship("User", backref="managed_spaces")


class SpaceBooking(Base):
    __tablename__ = "space_bookings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    space_id = Column(Integer, ForeignKey("spaces.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    amount = Column(Integer, default=0)  # 单位：分
    status = Column(String(20), default="pending")  # pending/paid/using/completed/cancelled
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    space = relationship("Space")
    user = relationship("User")
