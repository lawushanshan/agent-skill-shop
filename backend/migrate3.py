#!/usr/bin/env python3
"""
数据库迁移脚本 #3 - 添加 skills 表 is_free 字段
"""
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "1Panel-mysql-wTIi")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "titan")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Qh3yXmREsKNCne5D")
DB_NAME = os.getenv("DB_NAME", "titan")

def migrate():
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
        # 检查 is_free 字段是否存在
        cursor.execute("SHOW COLUMNS FROM skills LIKE 'is_free'")
        if not cursor.fetchone():
            print("➕ 添加 is_free 字段到 skills 表")
            cursor.execute("""
                ALTER TABLE skills 
                ADD COLUMN is_free BOOLEAN DEFAULT FALSE
            """)
            print("✅ is_free 字段添加成功")
        else:
            print("✅ is_free 字段已存在")
        
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
