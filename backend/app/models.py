"""
数据模型
"""
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, TIMESTAMP, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from .database import Base

class SkillStatus(str, enum.Enum):
    DRAFT = "draft"
    PENDING = "pending"
    PUBLISHED = "published"
    REJECTED = "rejected"

class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    COMPLETED = "completed"
    REFUNDED = "refunded"

class Skill(Base):
    """技能表"""
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    category = Column(String(100), index=True)
    price = Column(Float, default=0.0)  # 0 表示免费
    platform_commission = Column(Float, default=0.2)  # 平台抽成 20%
    version = Column(String(50), default="1.0.0")
    author = Column(String(100))
    repository = Column(String(500))  # GitHub 仓库
    documentation = Column(Text)  # 文档 URL
    download_url = Column(String(500))  # 下载链接
    preview_images = Column(JSON)  # 预览图
    tags = Column(JSON)  # 标签
    is_free = Column(Boolean, default=False)  # 是否免费
    status = Column(SQLEnum(SkillStatus), default=SkillStatus.DRAFT)
    developer_id = Column(Integer, ForeignKey("users.id"), index=True)
    download_count = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    developer = relationship("User", foreign_keys=[developer_id])
    reviews = relationship("Review", back_populates="skill", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="skill")

class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    avatar_url = Column(String(255))
    role = Column(String(50), default="user")
    is_active = Column(Boolean, default=True)
    is_developer = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    skills = relationship("Skill", foreign_keys="Skill.developer_id", back_populates="developer")
    orders = relationship("Order", back_populates="user")
    reviews = relationship("Review", back_populates="user")

class Order(Base):
    """订单表"""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_no = Column(String(100), unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), index=True)
    amount = Column(Float)  # 订单金额
    platform_fee = Column(Float, default=0.0)  # 平台费用（20%）
    developer_earning = Column(Float, default=0.0)  # 开发者收入（80%）
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.PENDING)
    payment_method = Column(String(50))
    paid_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    # 关系
    user = relationship("User", back_populates="orders")
    skill = relationship("Skill", back_populates="orders")

class Review(Base):
    """评价表"""
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    rating = Column(Integer)  # 1-5
    comment = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    # 关系
    skill = relationship("Skill", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
