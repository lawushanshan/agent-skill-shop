#!/bin/bash
# Agent Skill Shop - 功能测试脚本

echo "======================================"
echo "Agent Skill Shop - 功能测试"
echo "======================================"
echo ""

BASE_URL="http://localhost:8001"

# 1. 健康检查
echo "1. 健康检查..."
curl -s "$BASE_URL/health" | python3 -m json.tool
echo ""

# 2. 用户注册
echo "2. 用户注册测试..."
REGISTER_RESULT=$(curl -s -X POST "$BASE_URL/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser2",
    "email": "testuser2@titanlab.com",
    "password": "test123456",
    "is_developer": true
  }')
echo "$REGISTER_RESULT" | python3 -m json.tool
echo ""

# 3. 用户登录
echo "3. 用户登录测试..."
LOGIN_RESULT=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser2@titanlab.com",
    "password": "test123456"
  }')
echo "$LOGIN_RESULT" | python3 -m json.tool
TOKEN=$(echo "$LOGIN_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")
echo ""

# 4. 创建技能
echo "4. 创建技能测试..."
SKILL_RESULT=$(curl -s -X POST "$BASE_URL/api/skills" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "AI 智能客服",
    "description": "基于 AI 的智能客服系统，支持自动回复、情感分析等功能",
    "category": "nlp",
    "price": 99.0,
    "is_free": false,
    "version": "1.0.0",
    "author": "Titan Lab",
    "tags": ["AI", "NLP", "客服"]
  }')
echo "$SKILL_RESULT" | python3 -m json.tool
SKILL_ID=$(echo "$SKILL_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))")
echo ""

# 5. 获取技能列表
echo "5. 获取技能列表..."
curl -s "$BASE_URL/api/skills?limit=10" | python3 -m json.tool
echo ""

# 6. 获取技能详情
echo "6. 获取技能详情 (ID: $SKILL_ID)..."
curl -s "$BASE_URL/api/skills/$SKILL_ID" | python3 -m json.tool
echo ""

# 7. 创建订单（付费技能）
echo "7. 创建订单测试..."
ORDER_RESULT=$(curl -s -X POST "$BASE_URL/api/orders" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"skill_id\": $SKILL_ID}")
echo "$ORDER_RESULT" | python3 -m json.tool
echo ""

# 8. 创建免费技能
echo "8. 创建免费技能..."
FREE_SKILL=$(curl -s -X POST "$BASE_URL/api/skills" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "免费 AI 工具",
    "description": "免费的 AI 工具包",
    "category": "automation",
    "price": 0,
    "is_free": true,
    "version": "1.0.0",
    "author": "Titan Lab",
    "tags": ["AI", "免费"]
  }')
echo "$FREE_SKILL" | python3 -m json.tool
FREE_SKILL_ID=$(echo "$FREE_SKILL" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))")
echo ""

# 9. 领取免费技能
echo "9. 领取免费技能 (ID: $FREE_SKILL_ID)..."
FREE_ORDER=$(curl -s -X POST "$BASE_URL/api/orders" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"skill_id\": $FREE_SKILL_ID}")
echo "$FREE_ORDER" | python3 -m json.tool
echo ""

# 10. 获取订单列表
echo "10. 获取订单列表..."
curl -s "$BASE_URL/api/orders" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo ""

echo "======================================"
echo "测试完成！"
echo "======================================"
echo ""
echo "前端访问：http://localhost:5174"
echo "后端 API: http://localhost:8001"
echo "API 文档：http://localhost:8001/docs"
