# Agent Skill Shop - AI 智能体技能商店

**项目名称**: Agent Skill Shop  
**项目类型**: AI 智能体技能市场平台  
**创建日期**: 2026-04-01  
**状态**: 🚀 项目启动

---

## 📋 项目概述

Agent Skill Shop 是一个 AI 智能体技能市场和分发平台，允许开发者创建、发布、销售和部署 AI 智能体技能。

### 核心功能

1. **🛒 技能商店** - 浏览、搜索、购买 AI 技能
2. **👨‍ 开发者中心** - 创建、上传、管理技能
3. **🤖 技能部署** - 一键部署到 ACC 智能体中心
4. **💳 支付系统** - ⏳ 待结项（预留接口）
5. **📊 数据分析** - 下载量、收入、用户评价
6. **⭐ 评价系统** - 用户评分和评论

### 商业模式

- **平台抽成**: 20%
- **免费技能**: ✅ 支持（价格设为 0）
- **付费技能**: 开发者获得 80% 收入

---

## 🎯 目标用户

### 技能开发者
- AI 开发者
- 数据科学家
- 机器学习工程师
- 独立开发者

### 技能消费者
- 企业用户
- 个人开发者
- 研究机构
- ACC 平台用户

---

## 🛠️ 技术栈

### 前端
| 技术 | 版本 | 说明 |
|------|------|------|
| Vue 3 | 3.x | 渐进式框架 |
| Ant Design Pro | 5.x | 企业级 UI |
| TypeScript | 5.x | 类型安全 |
| Vite | 5.x | 构建工具 |

### 后端
| 技术 | 版本 | 说明 |
|------|------|------|
| FastAPI | 0.x | Python Web 框架 |
| MySQL | 8.x | 关系数据库 |
| Redis | 7.x | 缓存和会话 |
| Celery | 5.x | 异步任务 |

### 基础设施
| 组件 | 说明 |
|------|------|
| 数据库 | 1Panel MySQL (1Panel-mysql-wTIi:3306/titan) |
| 缓存 | Redis |
| 存储 | 对象存储（技能包） |
| 部署 | Docker + Nginx |

---

## 📁 项目结构

```
agent-skill-shop/
├── README.md                 # 项目说明
├── PROJECT_PLAN.md           # 项目计划
├── TASK_ASSIGNMENT.md        # 任务分配
├── TECH_SPEC.md              # 技术规格
├── backend/                  # 后端
│   ├── app/
│   │   ├── api/              # API 路由
│   │   ├── models/           # 数据模型
│   │   ├── services/         # 业务逻辑
│   │   └── utils/            # 工具函数
│   └── main.py               # 主应用
├── frontend/                 # 前端
│   └── src/
│       ├── components/       # 组件
│       ├── views/            # 页面
│       └── api/              # API 调用
└── docs/                     # 文档
```

---

## 📊 数据库设计

### 核心表

1. **users** - 用户表
2. **skills** - 技能表
3. **categories** - 分类表
4. **orders** - 订单表
5. **reviews** - 评价表
6. **downloads** - 下载记录
7. **developers** - 开发者信息
8. **payouts** - 结算记录

---

## 🚀 快速开始

### 后端启动
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### 前端启动
```bash
cd frontend
npm install
npm run dev
```

### 访问地址
- 前端：http://localhost:5174
- 后端：http://localhost:8001
- API 文档：http://localhost:8001/docs

---

## 👥 团队分工

| 角色 | 职责 |
|------|------|
| CTO | 技术架构、代码审查 |
| 前端工程师 | 前端界面开发 |
| 后端工程师 | 后端 API 开发 |
| 运维工程师 | 环境搭建、部署 |

---

## 📞 沟通方式

- **黑板系统**: `/app/working/workspaces/msK2iF/blackboard_tool.py`
- **智能体**: ADMIN, DEV, OPS, TEST, DOC, SEC

---

## 📄 相关文档

- [项目计划](PROJECT_PLAN.md)
- [任务分配](TASK_ASSIGNMENT.md)
- [技术规格](TECH_SPEC.md)

---

##  成功标准

1. ✅ 技能商店功能完整
2. ✅ 开发者中心可用
3. ✅ 支付系统集成
4. ✅ ACC 平台对接
5. ✅ 按时交付

---

**最后更新**: 2026-04-01  
**维护者**: Titan Lab 团队
