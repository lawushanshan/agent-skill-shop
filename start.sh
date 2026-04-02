#!/bin/bash

# Agent Skill Shop - 启动脚本
# 端口：前端 8083, 后端 8087

PROJECT_DIR="/app/working/projects/titanlab/agent-skill-shop"
BACKEND_PID_FILE="${PROJECT_DIR}/.backend.pid"
FRONTEND_PID_FILE="${PROJECT_DIR}/.frontend.pid"

start() {
    echo "============================================"
    echo "  Agent Skill Shop 启动脚本"
    echo "  端口：前端 8083, 后端 8087"
    echo "============================================"
    echo ""
    
    # 启动后端
    cd "${PROJECT_DIR}/backend"
    nohup python3 main.py > "${PROJECT_DIR}/backend.log" 2>&1 &
    echo $! > "$BACKEND_PID_FILE"
    echo "✅ 后端已启动 (PID: $(cat $BACKEND_PID_FILE))"
    echo "📡 API 文档：http://localhost:8087/docs"
    echo ""
    
    sleep 2
    
    # 启动前端 (生产环境使用 Python HTTP 服务器)
    cd "${PROJECT_DIR}/frontend"
    nohup python3 -m http.server 8083 > "${PROJECT_DIR}/frontend.log" 2>&1 &
    echo $! > "$FRONTEND_PID_FILE"
    echo "✅ 前端已启动 (PID: $(cat $FRONTEND_PID_FILE))"
    echo "🌐 访问地址：http://localhost:8083/"
    echo ""
    echo "============================================"
}

stop() {
    echo "🛑 停止所有服务..."
    
    if [ -f "$BACKEND_PID_FILE" ]; then
        PID=$(cat "$BACKEND_PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            kill $PID
            rm "$BACKEND_PID_FILE"
            echo "✅ 后端已停止"
        fi
    fi
    
    if [ -f "$FRONTEND_PID_FILE" ]; then
        PID=$(cat "$FRONTEND_PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            kill $PID
            rm "$FRONTEND_PID_FILE"
            echo "✅ 前端已停止"
        fi
    fi
    
    echo ""
}

restart() {
    stop
    sleep 1
    start
}

status() {
    echo "=== 服务状态 ==="
    
    if [ -f "$BACKEND_PID_FILE" ]; then
        PID=$(cat "$BACKEND_PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            echo "后端 (8087): ✅ 运行中 (PID: $PID)"
        else
            echo "后端 (8087): ❌ 已停止"
        fi
    else
        echo "后端 (8087): ❌ 未启动"
    fi
    
    if [ -f "$FRONTEND_PID_FILE" ]; then
        PID=$(cat "$FRONTEND_PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            echo "前端 (8083): ✅ 运行中 (PID: $PID)"
        else
            echo "前端 (8083): ❌ 已停止"
        fi
    else
        echo "前端 (8083): ❌ 未启动"
    fi
    
    echo ""
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    *)
        echo "用法：$0 {start|stop|restart|status}"
        exit 1
        ;;
esac
