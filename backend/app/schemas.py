"""
Pydantic Schemas - API 请求/响应验证
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class SkillStatus(str, Enum):
    DRAFT = "draft"
    PENDING = "pending"
    PUBLISHED = "published"
    REJECTED = "rejected"

class OrderStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    COMPLETED = "completed"
    REFUNDED = "refunded"

# ============ 技能 ============

class SkillCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category: str
    price: float = Field(default=0.0, ge=0)
    is_free: bool = False  # 是否免费
    platform_commission: float = 0.2  # 平台抽成 20%
    version: str = "1.0.0"
    author: Optional[str] = None
    repository: Optional[str] = None
    documentation: Optional[str] = None
    tags: Optional[List[str]] = None

class SkillResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    category: str
    price: float
    is_free: bool = False
    platform_commission: float = 0.2
    version: str = "1.0.0"
    author: Optional[str] = None
    repository: Optional[str] = None
    documentation: Optional[str] = None
    download_url: Optional[str] = None
    preview_images: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    status: SkillStatus
    download_count: int
    rating: float
    review_count: int
    developer_id: int
    developer_name: Optional[str] = None  # 开发者名称
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class SkillList(BaseModel):
    items: List[SkillResponse]
    total: int

# ============ 用户 ============

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    is_developer: bool = False
    role: Optional[str] = "user"

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    avatar_url: Optional[str] = None
    role: Optional[str] = "user"
    is_developer: bool = False
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# ============ 订单 ============

class OrderCreate(BaseModel):
    skill_id: int

class OrderResponse(BaseModel):
    id: int
    order_no: str
    user_id: int
    skill_id: int
    amount: float
    platform_fee: float = 0.0  # 平台费用
    developer_earning: float = 0.0  # 开发者收入
    status: OrderStatus
    payment_method: Optional[str] = None
    paid_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class OrderList(BaseModel):
    items: List[OrderResponse]
    total: int

# ============ 评价 ============

class ReviewCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class ReviewResponse(BaseModel):
    id: int
    skill_id: int
    user_id: int
    rating: int
    comment: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
