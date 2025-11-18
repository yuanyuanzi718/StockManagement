#!/usr/bin/env python3
"""
查看TradingAgents数据库数据的便捷脚本
"""

from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv
import json

def format_datetime(dt):
    """格式化日期时间"""
    if isinstance(dt, datetime):
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    return str(dt)

def view_database():
    """查看数据库中的所有集合和数据"""
    print("=" * 80)
    print("📊 TradingAgents 数据库查看工具")
    print("=" * 80)
    
    try:
        # 加载环境变量
        load_dotenv()
        
        # 从环境变量或使用默认值获取MongoDB配置
        mongodb_host = os.getenv("MONGODB_HOST", "localhost")
        mongodb_port = int(os.getenv("MONGODB_PORT", "27017"))
        mongodb_username = os.getenv("MONGODB_USERNAME", "admin")
        mongodb_password = os.getenv("MONGODB_PASSWORD", "tradingagents123")
        mongodb_database = os.getenv("MONGODB_DATABASE", "tradingagents")
        mongodb_auth_source = os.getenv("MONGODB_AUTH_SOURCE", "admin")
        
        print(f"\n🔗 连接信息:")
        print(f"   主机: {mongodb_host}:{mongodb_port}")
        print(f"   数据库: {mongodb_database}")
        print(f"   用户: {mongodb_username}")
        
        # 构建连接参数
        connect_kwargs = {
            "host": mongodb_host,
            "port": mongodb_port,
            "serverSelectionTimeoutMS": 5000,
            "connectTimeoutMS": 5000
        }
        
        # 如果有用户名和密码，添加认证信息
        if mongodb_username and mongodb_password:
            connect_kwargs.update({
                "username": mongodb_username,
                "password": mongodb_password,
                "authSource": mongodb_auth_source
            })
        
        # 连接MongoDB
        client = MongoClient(**connect_kwargs)
        
        # 测试连接
        client.admin.command('ping')
        print("✅ MongoDB连接成功\n")
        
        # 选择数据库
        db = client[mongodb_database]
        
        # 获取所有集合
        collections = db.list_collection_names()
        
        if not collections:
            print("⚠️  数据库中暂无集合")
            return
        
        print(f"📚 数据库中共有 {len(collections)} 个集合:\n")
        
        # 遍历所有集合
        for i, collection_name in enumerate(collections, 1):
            collection = db[collection_name]
            count = collection.count_documents({})
            
            print(f"{i}. 📁 {collection_name}")
            print(f"   记录数: {count}")
            
            if count > 0:
                # 获取最新的一条记录
                latest = collection.find_one(sort=[("_id", -1)])
                
                # 显示字段列表
                if latest:
                    fields = list(latest.keys())
                    print(f"   字段数: {len(fields)}")
                    print(f"   字段列表: {', '.join(fields[:10])}" + 
                          (f" ... (共{len(fields)}个)" if len(fields) > 10 else ""))
                    
                    # 显示关键字段
                    if 'created_at' in latest:
                        print(f"   最新数据时间: {format_datetime(latest['created_at'])}")
                    elif 'updated_at' in latest:
                        print(f"   最新更新时间: {format_datetime(latest['updated_at'])}")
                    
                    # 显示特定集合的关键信息
                    if 'symbol' in latest:
                        print(f"   示例股票代码: {latest['symbol']}")
                    if 'stock_symbol' in latest:
                        print(f"   示例股票代码: {latest['stock_symbol']}")
                    if 'analysis_id' in latest:
                        print(f"   示例分析ID: {latest['analysis_id']}")
            
            print()
        
        # 交互式查询
        print("=" * 80)
        print("🔍 交互式查询")
        print("=" * 80)
        print("\n可用的集合:")
        for i, name in enumerate(collections, 1):
            print(f"  {i}. {name}")
        
        print("\n输入数字选择集合查看详细数据，或按回车退出:")
        
        choice = input("请选择 (1-{}): ".format(len(collections))).strip()
        
        if choice and choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(collections):
                view_collection_details(db, collections[idx])
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'client' in locals():
            client.close()
            print("\n👋 连接已关闭")

def view_collection_details(db, collection_name):
    """查看集合的详细数据"""
    print("\n" + "=" * 80)
    print(f"📋 集合: {collection_name}")
    print("=" * 80)
    
    collection = db[collection_name]
    
    # 获取总数
    total = collection.count_documents({})
    print(f"\n总记录数: {total}")
    
    # 获取最新的5条记录
    print(f"\n最新的5条记录:\n")
    
    records = collection.find().sort("_id", -1).limit(5)
    
    for i, record in enumerate(records, 1):
        print(f"--- 记录 {i} ---")
        
        # 转换为JSON格式输出（更易读）
        record_copy = dict(record)
        
        # 处理特殊字段
        if '_id' in record_copy:
            record_copy['_id'] = str(record_copy['_id'])
        
        for key, value in record_copy.items():
            if isinstance(value, datetime):
                record_copy[key] = format_datetime(value)
            elif isinstance(value, str) and len(value) > 200:
                # 长文本截断显示
                record_copy[key] = value[:200] + "... (共{}字符)".format(len(value))
        
        # 美化输出
        print(json.dumps(record_copy, ensure_ascii=False, indent=2))
        print()
    
    # 显示索引信息
    print("=" * 80)
    print("索引信息:")
    print("=" * 80)
    indexes = collection.list_indexes()
    for idx in indexes:
        print(f"  - {idx['name']}: {idx.get('key', {})}")

if __name__ == "__main__":
    view_database()

