#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
异步Redis演示
需要安装: pip install aioredis
"""

import asyncio
import aioredis


async def demo_redis_basic():
    """演示基本的Redis操作"""
    print("=== 基本Redis操作 ===")
    
    # 创建Redis连接
    redis = await aioredis.create_redis('redis://localhost:6379')
    
    try:
        # 设置值
        await redis.set('name', '张三')
        print("设置 name = 张三")
        
        # 获取值
        value = await redis.get('name', encoding='utf-8')
        print(f"获取 name = {value}")
        
        # 设置过期时间
        await redis.expire('name', 60)
        print("设置 name 过期时间为60秒")
        
        # 检查键是否存在
        exists = await redis.exists('name')
        print(f"键 'name' 是否存在: {exists}")
        
    finally:
        # 关闭连接
        redis.close()
        await redis.wait_closed()


async def demo_redis_hash():
    """演示Redis哈希操作"""
    print("\n=== Redis哈希操作 ===")
    
    redis = await aioredis.create_redis('redis://localhost:6379')
    
    try:
        # 设置哈希值
        await redis.hmset_dict('user:1', {
            'name': '李四',
            'age': '25',
            'email': 'lisi@example.com'
        })
        print("设置用户哈希值")
        
        # 获取哈希值
        user_data = await redis.hgetall('user:1', encoding='utf-8')
        print(f"用户数据: {user_data}")
        
        # 获取单个字段
        name = await redis.hget('user:1', 'name', encoding='utf-8')
        print(f"用户名: {name}")
        
        # 检查字段是否存在
        has_age = await redis.hexists('user:1', 'age')
        print(f"是否存在age字段: {has_age}")
        
    finally:
        redis.close()
        await redis.wait_closed()


async def demo_redis_list():
    """演示Redis列表操作"""
    print("\n=== Redis列表操作 ===")
    
    redis = await aioredis.create_redis('redis://localhost:6379')
    
    try:
        # 清空列表
        await redis.delete('tasks')
        
        # 添加元素到列表
        await redis.lpush('tasks', '任务1', '任务2', '任务3')
        print("添加任务到列表")
        
        # 获取列表长度
        length = await redis.llen('tasks')
        print(f"任务列表长度: {length}")
        
        # 获取列表元素
        tasks = await redis.lrange('tasks', 0, -1, encoding='utf-8')
        print(f"所有任务: {tasks}")
        
        # 弹出元素
        task = await redis.rpop('tasks', encoding='utf-8')
        print(f"弹出的任务: {task}")
        
    finally:
        redis.close()
        await redis.wait_closed()


async def demo_redis_set():
    """演示Redis集合操作"""
    print("\n=== Redis集合操作 ===")
    
    redis = await aioredis.create_redis('redis://localhost:6379')
    
    try:
        # 清空集合
        await redis.delete('tags')
        
        # 添加元素到集合
        await redis.sadd('tags', 'python', 'async', 'redis', 'demo')
        print("添加标签到集合")
        
        # 获取集合大小
        size = await redis.scard('tags')
        print(f"标签集合大小: {size}")
        
        # 获取所有元素
        tags = await redis.smembers('tags', encoding='utf-8')
        print(f"所有标签: {tags}")
        
        # 检查元素是否存在
        has_python = await redis.sismember('tags', 'python')
        print(f"是否包含python标签: {has_python}")
        
    finally:
        redis.close()
        await redis.wait_closed()


async def demo_redis_pipeline():
    """演示Redis管道操作"""
    print("\n=== Redis管道操作 ===")
    
    redis = await aioredis.create_redis('redis://localhost:6379')
    
    try:
        # 使用管道批量执行命令
        async with redis.pipeline() as pipe:
            await pipe.set('counter', 0)
            await pipe.incr('counter')
            await pipe.incr('counter')
            await pipe.incr('counter')
            await pipe.expire('counter', 300)
            
            # 执行所有命令
            results = await pipe.execute()
            print(f"管道执行结果: {results}")
        
        # 获取最终结果
        counter = await redis.get('counter', encoding='utf-8')
        print(f"计数器最终值: {counter}")
        
    finally:
        redis.close()
        await redis.wait_closed()


async def demo_redis_pubsub():
    """演示Redis发布订阅"""
    print("\n=== Redis发布订阅 ===")
    
    redis = await aioredis.create_redis('redis://localhost:6379')
    
    try:
        # 创建订阅者
        sub = await redis.subscribe('news')
        
        # 发布消息的协程
        async def publisher():
            await asyncio.sleep(1)
            await redis.publish('news', '重要新闻1')
            await asyncio.sleep(1)
            await redis.publish('news', '重要新闻2')
            await asyncio.sleep(1)
            await redis.publish('news', '重要新闻3')
        
        # 订阅者协程
        async def subscriber():
            try:
                async for message in sub[0]:
                    print(f"收到消息: {message.decode('utf-8')}")
            except asyncio.CancelledError:
                print("订阅者被取消")
        
        # 并发运行发布者和订阅者
        pub_task = asyncio.create_task(publisher())
        sub_task = asyncio.create_task(subscriber())
        
        # 等待发布完成
        await pub_task
        
        # 取消订阅者
        sub_task.cancel()
        try:
            await sub_task
        except asyncio.CancelledError:
            pass
        
        # 取消订阅
        await redis.unsubscribe('news')
        
    finally:
        redis.close()
        await redis.wait_closed()


async def demo_redis_connection_pool():
    """演示Redis连接池"""
    print("\n=== Redis连接池 ===")
    
    # 创建连接池
    pool = await aioredis.create_redis_pool('redis://localhost:6379', minsize=1, maxsize=10)
    
    try:
        # 并发执行多个Redis操作
        async def redis_operation(operation_id):
            async with pool.get() as redis:
                key = f"operation_{operation_id}"
                await redis.set(key, f"操作{operation_id}的结果")
                result = await redis.get(key, encoding='utf-8')
                print(f"操作{operation_id}: {result}")
                return result
        
        # 创建多个并发任务
        tasks = [redis_operation(i) for i in range(5)]
        results = await asyncio.gather(*tasks)
        print(f"所有操作结果: {results}")
        
    finally:
        pool.close()
        await pool.wait_closed()


if __name__ == "__main__":
    # 注意：需要确保Redis服务器正在运行
    # 如果Redis不在本地或端口不是6379，请修改连接地址
    
    try:
        asyncio.run(demo_redis_basic())
        asyncio.run(demo_redis_hash())
        asyncio.run(demo_redis_list())
        asyncio.run(demo_redis_set())
        asyncio.run(demo_redis_pipeline())
        asyncio.run(demo_redis_pubsub())
        asyncio.run(demo_redis_connection_pool())
    except Exception as e:
        print(f"Redis连接失败: {e}")
        print("请确保Redis服务器正在运行，或者修改连接地址") 