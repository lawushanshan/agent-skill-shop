#!/usr/bin/env python3
"""
数据库迁移 - 添加 ACC 部署相关字段
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
        # 检查 skills 表是否存在
        cursor.execute("SHOW TABLES LIKE 'skills'")
        if not cursor.fetchone():
            print("❌ skills 表不存在")
            return
        
        # 添加 acc_agent_id 字段
        cursor.execute("SHOW COLUMNS FROM skills LIKE 'acc_agent_id'")
        if not cursor.fetchone():
            print("➕ 添加 acc_agent_id 字段到 skills 表")
            cursor.execute("""
                ALTER TABLE skills 
                ADD COLUMN acc_agent_id VARCHAR(100) NULL
            """)
            print("✅ acc_agent_id 字段添加成功")
        else:
            print("✅ acc_agent_id 字段已存在")
        
        # 添加 acc_deployed 字段
        cursor.execute("SHOW COLUMNS FROM skills LIKE 'acc_deployed'")
        if not cursor.fetchone():
            print("➕ 添加 acc_deployed 字段到 skills 表")
            cursor.execute("""
                ALTER TABLE skills 
                ADD COLUMN acc_deployed BOOLEAN DEFAULT FALSE
            """)
            print("✅ acc_deployed 字段添加成功")
        else:
            print("✅ acc_deployed 字段已存在")
        
        # 添加 acc_deployed_at 字段
        cursor.execute("SHOW COLUMNS FROM skills LIKE 'acc_deployed_at'")
        if not cursor.fetchone():
            print("➕ 添加 acc_deployed_at 字段到 skills 表")
            cursor.execute("""
                ALTER TABLE skills 
                ADD COLUMN acc_deployed_at TIMESTAMP NULL
            """)
            print("✅ acc_deployed_at 字段添加成功")
        else:
            print("✅ acc_deployed_at 字段已存在")
        
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
