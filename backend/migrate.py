#!/usr/bin/env python3
"""
数据库迁移脚本 - 添加缺失字段
"""
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

# 数据库配置
DB_HOST = os.getenv("DB_HOST", "1Panel-mysql-wTIi")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "titan")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Qh3yXmREsKNCne5D")
DB_NAME = os.getenv("DB_NAME", "titan")

def migrate():
    """执行数据库迁移"""
    print(f"🔧 连接到数据库 {DB_HOST}:{DB_PORT}/{DB_NAME}")
    
    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    
    cursor = conn.cursor()
    
    try:
        # 检查 users 表是否存在
        cursor.execute("SHOW TABLES LIKE 'users'")
        if not cursor.fetchone():
            print("❌ users 表不存在，等待应用自动创建")
            return
        
        # 检查 is_developer 字段是否存在
        cursor.execute("SHOW COLUMNS FROM users LIKE 'is_developer'")
        if not cursor.fetchone():
            print("➕ 添加 is_developer 字段到 users 表")
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN is_developer BOOLEAN DEFAULT FALSE
            """)
            print("✅ is_developer 字段添加成功")
        else:
            print("✅ is_developer 字段已存在")
        
        # 检查 role 字段是否存在
        cursor.execute("SHOW COLUMNS FROM users LIKE 'role'")
        if not cursor.fetchone():
            print("➕ 添加 role 字段到 users 表")
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN role VARCHAR(50) DEFAULT 'user'
            """)
            print("✅ role 字段添加成功")
        else:
            print("✅ role 字段已存在")
        
        # 检查 is_active 字段是否存在
        cursor.execute("SHOW COLUMNS FROM users LIKE 'is_active'")
        if not cursor.fetchone():
            print("➕ 添加 is_active 字段到 users 表")
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN is_active BOOLEAN DEFAULT TRUE
            """)
            print("✅ is_active 字段添加成功")
        else:
            print("✅ is_active 字段已存在")
        
        conn.commit()
        print("\n🎉 数据库迁移完成！")
        
    except Exception as e:
        print(f"❌ 迁移失败：{e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    migrate()
