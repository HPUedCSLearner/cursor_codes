#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
异步MySQL演示
需要安装: pip install aiomysql
"""

import asyncio
import aiomysql


async def demo_mysql_basic():
    """演示基本的MySQL操作"""
    print("=== 基本MySQL操作 ===")
    
    # 连接MySQL
    conn = await aiomysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='password',  # 请修改为你的密码
        db='test',  # 请修改为你的数据库名
        charset='utf8mb4'
    )
    
    try:
        # 创建游标
        cur = await conn.cursor()
        
        # 执行查询
        await cur.execute("SELECT VERSION()")
        version = await cur.fetchone()
        print(f"MySQL版本: {version[0]}")
        
        # 关闭游标
        await cur.close()
        
    finally:
        # 关闭连接
        conn.close()


async def demo_mysql_query():
    """演示MySQL查询操作"""
    print("\n=== MySQL查询操作 ===")
    
    conn = await aiomysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='password',
        db='test',
        charset='utf8mb4'
    )
    
    try:
        cur = await conn.cursor()
        
        # 创建测试表
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE,
            age INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        await cur.execute(create_table_sql)
        print("创建users表")
        
        # 插入数据
        insert_sql = "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)"
        users_data = [
            ('张三', 'zhangsan@example.com', 25),
            ('李四', 'lisi@example.com', 30),
            ('王五', 'wangwu@example.com', 28)
        ]
        
        await cur.executemany(insert_sql, users_data)
        await conn.commit()
        print("插入用户数据")
        
        # 查询数据
        await cur.execute("SELECT * FROM users")
        users = await cur.fetchall()
        print("所有用户:")
        for user in users:
            print(f"  ID: {user[0]}, 姓名: {user[1]}, 邮箱: {user[2]}, 年龄: {user[3]}")
        
        # 条件查询
        await cur.execute("SELECT * FROM users WHERE age > %s", (25,))
        older_users = await cur.fetchall()
        print(f"年龄大于25的用户数量: {len(older_users)}")
        
        await cur.close()
        
    finally:
        conn.close()


async def demo_mysql_dict_cursor():
    """演示使用字典游标"""
    print("\n=== 字典游标操作 ===")
    
    conn = await aiomysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='password',
        db='test',
        charset='utf8mb4'
    )
    
    try:
        # 使用字典游标
        cur = await conn.cursor(aiomysql.DictCursor)
        
        await cur.execute("SELECT * FROM users LIMIT 2")
        users = await cur.fetchall()
        
        print("使用字典游标查询结果:")
        for user in users:
            print(f"  用户: {user['name']}, 邮箱: {user['email']}, 年龄: {user['age']}")
        
        await cur.close()
        
    finally:
        conn.close()


async def demo_mysql_transaction():
    """演示MySQL事务操作"""
    print("\n=== MySQL事务操作 ===")
    
    conn = await aiomysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='password',
        db='test',
        charset='utf8mb4'
    )
    
    try:
        cur = await conn.cursor()
        
        # 开始事务
        await conn.begin()
        
        try:
            # 执行多个操作
            await cur.execute("UPDATE users SET age = age + 1 WHERE name = %s", ('张三',))
            await cur.execute("UPDATE users SET age = age + 1 WHERE name = %s", ('李四',))
            
            # 提交事务
            await conn.commit()
            print("事务提交成功")
            
        except Exception as e:
            # 回滚事务
            await conn.rollback()
            print(f"事务回滚: {e}")
            raise
        
        await cur.close()
        
    finally:
        conn.close()


async def demo_mysql_connection_pool():
    """演示MySQL连接池"""
    print("\n=== MySQL连接池 ===")
    
    # 创建连接池
    pool = await aiomysql.create_pool(
        host='localhost',
        port=3306,
        user='root',
        password='password',
        db='test',
        charset='utf8mb4',
        minsize=1,
        maxsize=10
    )
    
    try:
        async def query_user(user_id):
            """查询单个用户"""
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                    user = await cur.fetchone()
                    if user:
                        print(f"用户ID {user_id}: {user[1]}")
                        return user
                    else:
                        print(f"用户ID {user_id} 不存在")
                        return None
        
        # 并发查询多个用户
        tasks = [query_user(i) for i in range(1, 4)]
        results = await asyncio.gather(*tasks)
        print(f"查询结果: {len([r for r in results if r])} 个用户")
        
    finally:
        pool.close()
        await pool.wait_closed()


async def demo_mysql_batch_operations():
    """演示MySQL批量操作"""
    print("\n=== MySQL批量操作 ===")
    
    conn = await aiomysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='password',
        db='test',
        charset='utf8mb4'
    )
    
    try:
        cur = await conn.cursor()
        
        # 批量插入
        batch_data = [
            ('批量用户1', 'batch1@example.com', 22),
            ('批量用户2', 'batch2@example.com', 24),
            ('批量用户3', 'batch3@example.com', 26),
            ('批量用户4', 'batch4@example.com', 28),
            ('批量用户5', 'batch5@example.com', 30)
        ]
        
        insert_sql = "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)"
        await cur.executemany(insert_sql, batch_data)
        await conn.commit()
        print(f"批量插入 {len(batch_data)} 条记录")
        
        # 批量更新
        update_data = [
            (23, '批量用户1'),
            (25, '批量用户2'),
            (27, '批量用户3')
        ]
        
        update_sql = "UPDATE users SET age = %s WHERE name = %s"
        await cur.executemany(update_sql, update_data)
        await conn.commit()
        print("批量更新完成")
        
        # 查询结果
        await cur.execute("SELECT name, age FROM users WHERE name LIKE '批量用户%'")
        updated_users = await cur.fetchall()
        print("批量操作后的用户:")
        for user in updated_users:
            print(f"  {user[0]}: {user[1]}岁")
        
        await cur.close()
        
    finally:
        conn.close()


async def demo_mysql_error_handling():
    """演示MySQL错误处理"""
    print("\n=== MySQL错误处理 ===")
    
    conn = await aiomysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='password',
        db='test',
        charset='utf8mb4'
    )
    
    try:
        cur = await conn.cursor()
        
        # 尝试插入重复的邮箱（违反唯一约束）
        try:
            await cur.execute(
                "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)",
                ('重复用户', 'zhangsan@example.com', 25)
            )
            await conn.commit()
        except Exception as e:
            print(f"插入失败（预期错误）: {e}")
            await conn.rollback()
        
        # 尝试查询不存在的表
        try:
            await cur.execute("SELECT * FROM non_existent_table")
        except Exception as e:
            print(f"查询失败（预期错误）: {e}")
        
        await cur.close()
        
    finally:
        conn.close()


if __name__ == "__main__":
    # 注意：需要确保MySQL服务器正在运行
    # 请修改连接参数以匹配你的MySQL配置
    
    try:
        asyncio.run(demo_mysql_basic())
        asyncio.run(demo_mysql_query())
        asyncio.run(demo_mysql_dict_cursor())
        asyncio.run(demo_mysql_transaction())
        asyncio.run(demo_mysql_connection_pool())
        asyncio.run(demo_mysql_batch_operations())
        asyncio.run(demo_mysql_error_handling())
    except Exception as e:
        print(f"MySQL连接失败: {e}")
        print("请确保MySQL服务器正在运行，并检查连接参数") 