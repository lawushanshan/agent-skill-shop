# 📋 Agent Skill Shop - Spec 文档

**Spec ID**: ASS-001  
**版本**: 1.0.0  
**创建时间**: 2026-04-03  
**状态**: ✅ 已完成 (v1.0)  
**复杂度级别**: L2 (中等需求)

---

## 1. 背景

### 1.1 问题描述

Titan Lab 需要构建一个 AI 智能体技能交易平台，让开发者可以：
- 上传和分享 AI 智能体技能
- 通过技能获得收益
- 一键部署到 ACC 平台

### 1.2 用户故事

| 角色 | 需求 | 价值 |
|------|------|------|
| 开发者 | 上传技能、设置价格、获得收益 | 变现技术能力 |
| 用户 | 发现、购买、部署技能 | 快速获得 AI 能力 |
| 管理员 | 审核技能、管理平台内容 | 保证质量 |

### 1.3 商业目标

- 平台抽成 20%
- 开发者获得 80%
- 支持免费和付费技能

---

## 2. 目标

### 2.1 验收标准

- [x] 用户可以注册/登录
- [x] 开发者可以上传技能
- [x] 管理员可以审核技能
- [x] 用户可以浏览技能列表
- [x] 技能状态管理（草稿/待审核/已发布/已拒绝）
- [x] ACC 平台对接（一键部署）
- [ ] 订单系统（支付暂缓）
- [ ] 评价系统

### 2.2 成功指标

| 指标 | 目标值 | 当前值 |
|------|--------|--------|
| 技能数量 | ≥10 | 0 |
| 开发者数量 | ≥5 | 1 |
| 审核通过率 | ≥80% | - |
| 部署成功率 | ≥95% | 100% |

---

## 3. 技术方案

### 3.1 架构设计

```
┌─────────────────────────────────────────────────────────┐
│                    前端 (Vue 3 CDN)                      │
│  登录/注册 | 首页 | 上传技能 | 管理后台 | 技能详情        │
└─────────────────────────────────────────────────────────┘
                            ↓ HTTP/REST
┌─────────────────────────────────────────────────────────┐
│                  后端 (FastAPI + MySQL)                  │
│  认证 API | 技能 API | 订单 API | ACC 对接 API            │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    数据库 (MySQL)                        │
│  users | skills | orders | reviews                       │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                 ACC 平台 (Agent Control Center)          │
│  技能部署 | Agent 管理 | 状态监控                        │
└─────────────────────────────────────────────────────────┘
```

### 3.2 数据模型

```python
# User 表
id, username, email, password_hash, role, is_active, is_developer

# Skill 表
id, name, description, category, price, is_free, platform_commission,
status, developer_id, download_count, rating, review_count,
acc_agent_id, acc_deployed, acc_deployed_at

# Order 表
id, order_no, user_id, skill_id, amount, platform_fee, 
developer_earning, status, payment_method, paid_at

# Review 表
id, skill_id, user_id, rating, comment, created_at
```

### 3.3 API 端点

| 端点 | 方法 | 权限 | 说明 |
|------|------|------|------|
| /api/auth/register | POST | 公开 | 用户注册 |
| /api/auth/login | POST | 公开 | 用户登录 |
| /api/auth/me | GET | 认证 | 获取当前用户 |
| /api/skills | GET | 公开 | 技能列表 |
| /api/skills | POST | 开发者 | 创建技能 |
| /api/skills/:id | GET | 公开 | 技能详情 |
| /api/skills/:id | PUT | 开发者 | 更新技能 |
| /api/skills/:id | DELETE | 管理员 | 删除技能 |
| /api/skills-all | GET | 管理员 | 所有技能 |
| /api/skills/:id/status | PUT | 管理员 | 更新状态 |
| /api/skills/:id/deploy | POST | 开发者 | 部署到 ACC |
| /api/orders | GET | 认证 | 订单列表 |
| /api/orders | POST | 认证 | 创建订单 |

### 3.4 技术栈

| 层级 | 技术 | 版本 |
|------|------|------|
| 前端 | Vue 3 | 3.x (CDN) |
| 前端路由 | Vue Router | 4.x |
| HTTP 客户端 | Axios | latest |
| 后端 | FastAPI | 0.100+ |
| 数据库 | MySQL | 8.0 |
| ORM | SQLAlchemy | 2.0 |
| 认证 | JWT | PyJWT |
| 密码加密 | hashlib | SHA256 |

---

## 4. 任务拆分

### 4.1 已完成任务 ✅

| ID | 任务 | 状态 | 完成时间 |
|----|------|------|----------|
| T01 | 后端框架搭建 | ✅ | 2026-04-01 |
| T02 | 前端框架搭建 | ✅ | 2026-04-01 |
| T03 | 用户认证系统 | ✅ | 2026-04-01 |
| T04 | 技能管理 API | ✅ | 2026-04-01 |
| T05 | 订单系统 | ✅ | 2026-04-02 |
| T06 | ACC 对接 | ✅ | 2026-04-02 |
| T07 | 前端登录/注册 | ✅ | 2026-04-03 |
| T08 | 前端上传技能 | ✅ | 2026-04-03 |
| T09 | 前端管理后台 | ✅ | 2026-04-03 |
| T10 | 退出登录修复 | ✅ | 2026-04-03 |

### 4.2 待完成任务 📋

| ID | 任务 | 优先级 | 预计工时 | 状态 |
|----|------|--------|----------|------|
| T11 | 技能详情页面 | P1 | 2h | 🔄 进行中 |
| T12 | 个人中心页面 | P1 | 4h | 🔄 进行中 |
| T13 | 我的技能页面 | P1 | 4h | 🔄 进行中 |
| T14 | 评价系统 | P2 | 6h | 📋 待办 |
| T15 | 支付系统 (暂缓) | P3 | - | 🚫 暂缓 |
| T16 | 搜索功能增强 | P2 | 3h | 📋 待办 |
| T17 | 技能分类筛选 | P2 | 2h | 📋 待办 |
| T18 | 部署文档完善 | P1 | 2h | 📋 待办 |
| T19 | 开发者引导流程 | P1 | 3h | 📋 待办 |
| T20 | 首次登录引导 | P1 | 2h | 📋 待办 |

---

## 5. 测试计划

### 5.1 单元测试

```python
# 测试用户认证
test_register()
test_login_success()
test_login_wrong_password()
test_jwt_token_validation()

# 测试技能管理
test_create_skill()
test_update_skill()
test_delete_skill()
test_skill_status_transition()

# 测试订单系统
test_create_free_order()
test_create_paid_order()
test_platform_commission_calculation()
```

### 5.2 集成测试

```bash
# API 测试
curl -X POST http://localhost:8087/api/auth/register ...
curl -X POST http://localhost:8087/api/auth/login ...
curl -X GET http://localhost:8087/api/skills ...

# 前端测试
访问 http://localhost:8083/#/login
访问 http://localhost:8083/#/upload
访问 http://localhost:8083/#/admin
```

### 5.3 端到端测试

| 场景 | 步骤 | 预期结果 |
|------|------|----------|
| 开发者上传技能 | 登录→上传→提交 | 技能进入待审核 |
| 管理员审核 | 登录→管理后台→通过 | 技能已发布 |
| 用户浏览 | 访问首页→筛选 | 显示已发布技能 |
| 部署到 ACC | 点击部署→等待 | 部署成功 |

---

## 6. 风险评估

### 6.1 技术风险

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| JWT 认证失效 | 低 | 高 | 添加 token 刷新机制 |
| ACC 接口变更 | 中 | 中 | 添加适配层 |
| 数据库连接超时 | 中 | 高 | 连接池配置 |
| 前端 CDN 加载失败 | 低 | 中 | 添加本地备份 |

### 6.2 依赖风险

| 依赖 | 风险 | 备选方案 |
|------|------|----------|
| ACC 平台 | 接口变更 | 添加版本兼容 |
| MySQL | 连接问题 | 添加重试机制 |
| Vue 3 CDN | 加载失败 | 本地部署 |

---

## 7. 变更记录

| 版本 | 日期 | 变更内容 | 作者 |
|------|------|----------|------|
| 1.0.0 | 2026-04-03 | 初始版本 | CTO Tom |
| 1.0.1 | TBD | 待补充 | - |

---

## 8. 附录

### 8.1 测试账号

```
管理员：
邮箱：admin@titanlab.com
密码：admin123456

开发者：
邮箱：testdev1@titanlab.com
密码：test123456
```

### 8.2 部署信息

```
前端：http://服务器 IP:8083
后端：http://服务器 IP:8087
数据库：1Panel-mysql-wTIi:3306/titan
```

### 8.3 相关文档

- [项目 README](../README.md)
- [部署文档](../DEPLOYMENT.md)
- [快速开始](../QUICK_START.md)
- [24 小时冲刺计划](../24H_SPRINT.md)

---

**Spec 状态**: ✅ 已完成  
**下次更新**: 功能迭代时  
**Spec 审查**: 待安排
