"""
Agent Skill Shop - FastAPI 主应用
AI 智能体技能商店平台
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import jwt
import hashlib
from datetime import datetime, timedelta

# JWT Token 认证
security = HTTPBearer()

from app.database import get_db, engine, Base
from app import models
from app.schemas import (
    SkillCreate, SkillResponse, SkillList,
    UserRegister, UserLogin, UserResponse, TokenResponse,
    OrderCreate, OrderResponse, OrderList,
    ReviewCreate, ReviewResponse
)
from app.services.acc_service import acc_service

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

# JWT 配置
SECRET_KEY = "titanlab_agent_skill_shop_secret_2026_change_in_production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 天

# 密码加密（使用 hashlib 替代 bcrypt，避免版本兼容问题）
import hashlib

def hash_password(password: str) -> str:
    """密码加密"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return hash_password(plain_password) == hashed_password

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建 JWT token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = credentials.credentials
        print(f"Token: {token[:50]}...")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Payload: {payload}")
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        print("Token 已过期")
        raise credentials_exception
    except jwt.InvalidTokenError as e:
        print(f"Token 无效：{e}")
        raise credentials_exception
    except Exception as e:
        print(f"认证异常：{e}")
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

app = FastAPI(
    title="Agent Skill Shop",
    description="AI 智能体技能商店平台",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ 健康检查 ============

@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok", "version": "1.0.0"}

# ============ 用户认证 API ============

@app.post("/api/auth/register", response_model=UserResponse)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """用户注册"""
    # 检查邮箱是否已存在
    existing_user = db.query(models.User).filter(
        models.User.email == user_data.email
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="邮箱已被注册")
    
    # 检查用户名是否已存在
    existing_username = db.query(models.User).filter(
        models.User.username == user_data.username
    ).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="用户名已被使用")
    
    # 创建用户
    hashed_password = hash_password(user_data.password)
    db_user = models.User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
        role=user_data.role or "user",
        is_developer=user_data.is_developer or False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/api/auth/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """用户登录"""
    # 查找用户
    user = db.query(models.User).filter(
        models.User.email == credentials.email
    ).first()
    if not user:
        raise HTTPException(status_code=401, detail="邮箱或密码错误")
    
    # 验证密码
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="邮箱或密码错误")
    
    # 检查用户状态
    if not user.is_active:
        raise HTTPException(status_code=403, detail="账户已被禁用")
    
    # 创建 access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.username, "role": user.role},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(user)
    }

@app.get("/api/auth/me", response_model=UserResponse)
async def get_me(current_user: models.User = Depends(get_current_user)):
    """获取当前用户信息"""
    return current_user

# ============ 技能 API ============

@app.get("/api/skills", response_model=SkillList)
async def list_skills(
    skip: int = 0,
    limit: int = 20,
    category: Optional[str] = None,
    search: Optional[str] = None,
    is_free: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """获取技能列表"""
    query = db.query(models.Skill).filter(models.Skill.status == "published")
    
    if category:
        query = query.filter(models.Skill.category == category)
    if search:
        query = query.filter(models.Skill.name.contains(search))
    if is_free is not None:
        query = query.filter(models.Skill.is_free == is_free)
    
    skills = query.offset(skip).limit(limit).all()
    total = query.count()
    
    return SkillList(
        items=[SkillResponse.model_validate(s) for s in skills],
        total=total
    )

@app.get("/api/skills/{skill_id}", response_model=SkillResponse)
async def get_skill(skill_id: int, db: Session = Depends(get_db)):
    """获取技能详情"""
    skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="技能不存在")
    return skill

@app.post("/api/skills", response_model=SkillResponse)
async def create_skill(
    skill: SkillCreate,
    db: Session = Depends(get_db)
):
    """创建技能（开发者）"""
    # 从 JWT 获取用户 ID
    # TODO: 实现 JWT 认证后从这里获取
    developer_id = 1
    
    db_skill = models.Skill(**skill.dict(), developer_id=developer_id)
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

@app.put("/api/skills/{skill_id}", response_model=SkillResponse)
async def update_skill(
    skill_id: int,
    skill_update: SkillCreate,
    db: Session = Depends(get_db)
):
    """更新技能"""
    db_skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()
    if not db_skill:
        raise HTTPException(status_code=404, detail="技能不存在")
    
    # 更新字段
    for field, value in skill_update.dict().items():
        setattr(db_skill, field, value)
    
    db.commit()
    db.refresh(db_skill)
    return db_skill

@app.delete("/api/skills/{skill_id}")
async def delete_skill(
    skill_id: int,
    db: Session = Depends(get_db)
):
    """删除技能"""
    db_skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()
    if not db_skill:
        raise HTTPException(status_code=404, detail="技能不存在")
    
    db.delete(db_skill)
    db.commit()
    return {"message": "技能已删除"}

# ============ 订单 API ============

@app.get("/api/orders", response_model=OrderList)
async def list_orders(db: Session = Depends(get_db)):
    """获取订单列表"""
    orders = db.query(models.Order).all()
    return OrderList(
        items=[OrderResponse.model_validate(o) for o in orders],
        total=len(orders)
    )

@app.post("/api/orders", response_model=OrderResponse)
async def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    """创建订单"""
    # 检查技能是否存在
    skill = db.query(models.Skill).filter(models.Skill.id == order.skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="技能不存在")
    
    # 检查是否是免费技能
    if skill.is_free:
        # 免费技能直接完成订单
        import uuid
        from datetime import datetime
        db_order = models.Order(
            user_id=1,  # TODO: 从 JWT 获取
            skill_id=order.skill_id,
            order_no=f"FREE_{uuid.uuid4().hex[:12]}",
            amount=0.0,
            platform_fee=0.0,
            developer_earning=0.0,
            status="completed",
            paid_at=datetime.utcnow()
        )
    else:
        # 付费技能，计算平台抽成
        import uuid
        platform_fee = skill.price * 0.2  # 平台抽成 20%
        developer_earning = skill.price * 0.8  # 开发者获得 80%
        
        db_order = models.Order(
            user_id=1,  # TODO: 从 JWT 获取
            skill_id=order.skill_id,
            order_no=f"ORD_{uuid.uuid4().hex[:12]}",
            amount=skill.price,
            platform_fee=platform_fee,
            developer_earning=developer_earning,
            status="pending"  # 待支付
        )
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

# ============ 评价 API ============

@app.post("/api/skills/{skill_id}/reviews", response_model=ReviewResponse)
async def create_review(
    skill_id: int,
    review: ReviewCreate,
    db: Session = Depends(get_db)
):
    """创建技能评价"""
    db_review = models.Review(
        skill_id=skill_id,
        user_id=1,  # TODO: 从 JWT 获取
        rating=review.rating,
        comment=review.comment
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

# ============ ACC 对接 API ============

@app.post("/api/skills/{skill_id}/deploy", response_model=dict)
async def deploy_skill_to_acc(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """部署技能到 ACC 平台"""
    # 获取技能
    skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    # 检查是否已部署
    if skill.acc_deployed:
        return {
            "status": "already_deployed",
            "agent_id": skill.acc_agent_id,
            "url": f"http://localhost:8082/agents/{skill.acc_agent_id}"
        }
    
    # 部署到 ACC
    skill_data = {
        "id": skill.id,
        "name": skill.name,
        "description": skill.description,
        "category": skill.category,
        "version": skill.version,
        "author": skill.author or current_user.get('username', 'Unknown')
    }
    
    result = await acc_service.deploy_skill_to_acc(skill_data)
    
    if not result:
        raise HTTPException(status_code=500, detail="Failed to deploy to ACC")
    
    # 更新技能记录
    skill.acc_agent_id = result["agent_id"]
    skill.acc_deployed = True
    skill.acc_deployed_at = datetime.utcnow()
    db.commit()
    
    return {
        "status": "success",
        "agent_id": result["agent_id"],
        "url": result["url"],
        "deployed_at": result["deployed_at"]
    }


@app.get("/api/skills/{skill_id}/acc-status")
async def get_acc_deployment_status(
    skill_id: int,
    db: Session = Depends(get_db)
):
    """获取技能在 ACC 的部署状态"""
    skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    if not skill.acc_deployed:
        return {
            "deployed": False,
            "message": "Skill not deployed to ACC"
        }
    
    # 从 ACC 获取最新状态
    agent_status = await acc_service.get_agent_status(skill.acc_agent_id)
    
    return {
        "deployed": True,
        "agent_id": skill.acc_agent_id,
        "acc_url": f"http://localhost:8082/agents/{skill.acc_agent_id}",
        "deployed_at": skill.acc_deployed_at.isoformat() if skill.acc_deployed_at else None,
        "agent_status": agent_status
    }


@app.delete("/api/skills/{skill_id}/deploy")
async def undeploy_skill_from_acc(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """从 ACC 移除技能"""
    skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    if not skill.acc_deployed:
        return {"status": "not_deployed"}
    
    # 从 ACC 移除
    success = await acc_service.undeploy_skill(skill.acc_agent_id)
    
    if success:
        # 更新技能记录
        skill.acc_deployed = False
        skill.acc_agent_id = None
        skill.acc_deployed_at = None
        db.commit()
        return {"status": "success", "message": "Removed from ACC"}
    else:
        raise HTTPException(status_code=500, detail="Failed to remove from ACC")


# ============ 启动信息 ============

@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    print("=" * 60)
    print("🚀 Agent Skill Shop 启动成功！")
    print("=" * 60)
    print(f"📡 API 文档：http://localhost:8087/docs")
    print(f"🔍 Redoc: http://localhost:8087/redoc")
    print(f"❤️  健康检查：http://localhost:8087/health")
    print("=" * 60)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8087)
