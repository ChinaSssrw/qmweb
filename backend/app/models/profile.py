from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    basic_info = Column(JSON, default=dict)     # 姓名、头像、公司、职位、地区
    contact_info = Column(JSON, default=dict)   # 手机、微信、邮箱（脱敏）
    tags = Column(JSON, default=dict)           # 行业、职能、标签关键词
    bio = Column(JSON, default=dict)            # 一句话身份描述、详细自我介绍
    social = Column(JSON, default=dict)         # 公众号、视频号等
    privacy_settings = Column(JSON, default=dict)  # 各字段可见层级
    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="profile")
