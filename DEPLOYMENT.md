# Agent Skill Shop - 部署文档

**版本**: 1.1.0  
**更新时间**: 2026-04-10 08:45  
**负责人**: 运维团队 (titan / msK2iF)

---

## 📋 部署清单

### 环境要求
- [x] Python 3.11+
- [x] MySQL 8.0+
- [x] Nginx
- [x] SSL 证书 (可选)

### 服务信息
| 服务 | 端口 | 协议 | 状态 |
|------|------|------|------|
| 后端 API | 8087 | HTTP | ✅ 运行中 |
| 前端页面 | 8083 | HTTP/HTTPS | ✅ 运行中 |
| 数据库 | 3306 | MySQL | ✅ 1Panel MySQL |

### 数据库配置
```
DB_HOST=1Panel-mysql-wTIi
DB_PORT=3306
DB_USER=titan
DB_PASSWORD=Qh3yXmREsKNCne5D
DB_NAME=titan
```

---

## 🚀 快速部署 (生产环境)

### 方式一：使用启动脚本 (推荐)

```bash
# 进入项目目录
cd /app/working/projects/titanlab/agent-skill-shop

# 启动后端服务
cd backend
nohup python3 -m uvicorn main:app --host 0.0.0.0 --port 8087 > /tmp/agent_skill_shop.log 2>&1 &

# 启动前端服务
cd ../frontend
nohup python3 -m http.server 8083 > /tmp/frontend_8083.log 2>&1 &

# 检查服务状态
lsof -i :8087  # 后端
lsof -i :8083  # 前端
```

### 方式二：使用 start.sh 脚本

```bash
cd /app/working/projects/titanlab/agent-skill-shop
chmod +x start.sh
./start.sh
```

---

## 📋 完整部署步骤 (新服务器)

### 1. 准备环境

```bash
# 创建部署目录
sudo mkdir -p /opt/titanlab/agent-skill-shop
cd /opt/titanlab/agent-skill-shop

# 克隆代码 (或复制项目文件)
cp -r /app/working/projects/titanlab/agent-skill-shop/* .
```

### 2. 配置 Python 虚拟环境

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
cd backend
pip install -r requirements.txt
```

### 3. 配置环境变量

创建 `.env` 文件：

```bash
# 数据库配置
DB_HOST=1Panel-mysql-wTIi
DB_PORT=3306
DB_USER=titan
DB_PASSWORD=Qh3yXmREsKNCne5D
DB_NAME=titan

# JWT 配置
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# 服务配置
HOST=0.0.0.0
PORT=8001
DEBUG=false
```

### 4. 数据库迁移

```bash
cd backend
python3 migrate.py
python3 migrate_skills.py
```

### 5. 启动后端服务

```bash
# 使用 systemd (推荐)
sudo tee /etc/systemd/system/agent-skill-shop.service > /dev/null <<EOF
[Unit]
Description=Agent Skill Shop Backend
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/titanlab/agent-skill-shop/backend
Environment="PATH=/opt/titanlab/agent-skill-shop/venv/bin"
ExecStart=/opt/titanlab/agent-skill-shop/venv/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 启动服务
sudo systemctl daemon-reload
sudo systemctl enable agent-skill-shop
sudo systemctl start agent-skill-shop

# 检查状态
sudo systemctl status agent-skill-shop
```

### 6. 配置 Nginx

```bash
sudo tee /etc/nginx/sites-available/agent-skill-shop > /dev/null <<EOF
server {
    listen 80;
    server_name skills.titanlab.com;  # 替换为实际域名

    # 前端静态文件
    location / {
        root /opt/titanlab/agent-skill-shop/frontend;
        try_files \$uri \$uri/ /index.html;
    }

    # 后端 API 代理
    location /api/ {
        proxy_pass http://localhost:8087;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # 健康检查
    location /health {
        proxy_pass http://localhost:8087;
    }

    # API 文档
    location /docs {
        proxy_pass http://localhost:8087;
    }
}
EOF

# 启用配置
sudo ln -s /etc/nginx/sites-available/agent-skill-shop /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 7. 配置 SSL (可选)

```bash
# 使用 Let's Encrypt
sudo certbot --nginx -d skills.titanlab.com
```

### 8. 配置日志

```bash
# 创建日志目录
sudo mkdir -p /var/log/agent-skill-shop
sudo chown www-data:www-data /var/log/agent-skill-shop

# 配置日志轮转
sudo tee /etc/logrotate.d/agent-skill-shop > /dev/null <<EOF
/var/log/agent-skill-shop/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload agent-skill-shop > /dev/null 2>&1 || true
    endscript
}
EOF
```

---

## ✅ 验证部署

### 1. 健康检查

```bash
curl http://localhost:8087/health
# 预期输出：{"status":"ok","version":"1.0.0"}
```

### 2. 前端访问

```bash
curl http://localhost/ | grep "<title>"
# 预期输出：<title>Agent Skill Shop - AI 智能体技能商店</title>
```

### 3. API 测试

```bash
# 注册测试
curl -X POST http://localhost/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@titanlab.com","password":"test123456"}'

# 登录测试
curl -X POST http://localhost/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@titanlab.com","password":"test123456"}'
```

---

## 🔧 故障排查

### 后端服务无法启动

```bash
# 查看日志
sudo journalctl -u agent-skill-shop -f

# 检查端口占用
sudo lsof -i :8001

# 检查数据库连接
mysql -h 1Panel-mysql-wTIi -u titan -p
```

### 前端无法访问

```bash
# 检查 Nginx 配置
sudo nginx -t

# 查看 Nginx 日志
sudo tail -f /var/log/nginx/error.log

# 检查文件权限
ls -la /opt/titanlab/agent-skill-shop/frontend
```

### 数据库连接失败

```bash
# 测试数据库连接
mysql -h 1Panel-mysql-wTIi -u titan -pQh3yXmREsKNCne5D titan

# 检查数据库用户权限
mysql -h 1Panel-mysql-wTIi -u root -p
> SHOW GRANTS FOR 'titan'@'%';
```

---

## 📊 监控配置

### Prometheus 指标 (可选)

```bash
# 安装 prometheus-client
pip install prometheus-client

# 添加指标端点
# http://localhost:8001/metrics
```

### Grafana 仪表板 (可选)

导入仪表板 ID: 监控后端性能、数据库连接、API 响应时间

---

## 📞 联系方式

- **项目负责人**: ADMIN (用户小胖)
- **技术支持**: CTO Tom (default)
- **运维团队**: titan (msK2iF)

---

##  测试账号

| 角色 | 邮箱 | 密码 | 功能 |
|------|------|------|------|
| 开发者 | testdev1@titanlab.com | test123456 | 上传/管理技能 |
| 管理员 | admin@titanlab.com | admin123456 | 审核/管理所有技能 |

---

## 🔌 API 端点列表

### 用户认证
| 方法 | 端点 | 说明 |
|------|------|------|
| POST | /api/auth/register | 用户注册 |
| POST | /api/auth/login | 用户登录 |
| GET | /api/auth/me | 获取当前用户 |

### 技能管理
| 方法 | 端点 | 说明 |
|------|------|------|
| GET | /api/skills | 获取技能列表 |
| GET | /api/skills/{id} | 获取技能详情 |
| POST | /api/skills | 创建技能 (开发者) |
| PUT | /api/skills/{id} | 更新技能 |
| DELETE | /api/skills/{id} | 删除技能 (管理员) |
| GET | /api/skills-all | 获取所有技能 (管理员) |
| PUT | /api/skills/{id}/status | 更新技能状态 (管理员) |

### 订单系统
| 方法 | 端点 | 说明 |
|------|------|------|
| GET | /api/orders | 获取订单列表 |
| POST | /api/orders | 创建订单 |

### 评价系统
| 方法 | 端点 | 说明 |
|------|------|------|
| POST | /api/skills/{id}/reviews | 创建评价 |
| GET | /api/skills/{id}/reviews | 获取技能评价 |

### ACC 对接
| 方法 | 端点 | 说明 |
|------|------|------|
| POST | /api/skills/{id}/deploy | 部署到 ACC |
| DELETE | /api/skills/{id}/deploy | 从 ACC 移除 |

### 其他
| 方法 | 端点 | 说明 |
|------|------|------|
| GET | /health | 健康检查 |
| GET | /docs | Swagger API 文档 |
| GET | /redoc | Redoc API 文档 |

---

## 📝 更新日志

| 日期 | 版本 | 更新内容 | 负责人 |
|------|------|---------|--------|
| 2026-04-10 | 1.1.0 | 添加快速部署、API 端点列表、测试账号 | CTO Tom |
| 2026-04-01 | 1.0.0 | 初始版本 | CTO Tom |

---

**部署完成后请通知 ADMIN 进行验收测试！**
