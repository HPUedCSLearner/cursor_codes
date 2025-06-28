#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
异步上下文管理器演示
"""

import asyncio


class AsyncDatabaseConnection:
    """模拟异步数据库连接"""
    
    def __init__(self, host, port, database):
        self.host = host
        self.port = port
        self.database = database
        self.conn = None
        self.is_connected = False
    
    async def __aenter__(self):
        """异步进入上下文"""
        print(f"正在连接数据库: {self.host}:{self.port}/{self.database}")
        await asyncio.sleep(1)  # 模拟连接耗时
        self.conn = f"connection_to_{self.host}_{self.port}_{self.database}"
        self.is_connected = True
        print("数据库连接成功")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步退出上下文"""
        if self.is_connected:
            print("正在关闭数据库连接...")
            await asyncio.sleep(0.5)  # 模拟关闭耗时
            self.conn = None
            self.is_connected = False
            print("数据库连接已关闭")
        
        # 如果有异常，可以选择处理或重新抛出
        if exc_type is not None:
            print(f"数据库操作发生异常: {exc_type.__name__}: {exc_val}")
            # 可以选择返回True来抑制异常，或返回False让异常继续传播
            return False
    
    async def execute_query(self, query):
        """执行查询"""
        if not self.is_connected:
            raise RuntimeError("数据库未连接")
        
        print(f"执行查询: {query}")
        await asyncio.sleep(0.5)  # 模拟查询耗时
        return f"查询结果: {query}"


class AsyncFileHandler:
    """模拟异步文件处理器"""
    
    def __init__(self, filename, mode='r'):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    async def __aenter__(self):
        """异步进入上下文"""
        print(f"正在打开文件: {self.filename}")
        await asyncio.sleep(0.1)  # 模拟文件打开耗时
        self.file = f"file_handle_{self.filename}"
        print(f"文件 {self.filename} 已打开")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步退出上下文"""
        if self.file:
            print(f"正在关闭文件: {self.filename}")
            await asyncio.sleep(0.1)  # 模拟文件关闭耗时
            self.file = None
            print(f"文件 {self.filename} 已关闭")
    
    async def read(self):
        """读取文件内容"""
        if not self.file:
            raise RuntimeError("文件未打开")
        
        print(f"正在读取文件: {self.filename}")
        await asyncio.sleep(0.2)  # 模拟读取耗时
        return f"文件 {self.filename} 的内容"
    
    async def write(self, content):
        """写入文件内容"""
        if not self.file:
            raise RuntimeError("文件未打开")
        
        print(f"正在写入文件: {self.filename}")
        await asyncio.sleep(0.2)  # 模拟写入耗时
        print(f"写入内容: {content}")


class AsyncResourcePool:
    """模拟异步资源池"""
    
    def __init__(self, pool_size=3):
        self.pool_size = pool_size
        self.available_resources = list(range(pool_size))
        self.used_resources = []
    
    async def __aenter__(self):
        """异步进入上下文"""
        print("正在从资源池获取资源...")
        await asyncio.sleep(0.1)  # 模拟获取资源耗时
        
        if not self.available_resources:
            raise RuntimeError("资源池已满，无法获取资源")
        
        resource = self.available_resources.pop()
        self.used_resources.append(resource)
        print(f"已获取资源: {resource}")
        return resource
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步退出上下文"""
        if self.used_resources:
            resource = self.used_resources.pop()
            print(f"正在释放资源: {resource}")
            await asyncio.sleep(0.1)  # 模拟释放资源耗时
            self.available_resources.append(resource)
            print(f"资源 {resource} 已释放")


async def demo_basic_async_context():
    """演示基本异步上下文管理器"""
    print("=== 基本异步上下文管理器 ===")
    
    async with AsyncDatabaseConnection("localhost", 5432, "testdb") as db:
        result = await db.execute_query("SELECT * FROM users")
        print(result)


async def demo_nested_async_context():
    """演示嵌套异步上下文管理器"""
    print("\n=== 嵌套异步上下文管理器 ===")
    
    async with AsyncDatabaseConnection("localhost", 5432, "testdb") as db:
        async with AsyncFileHandler("config.txt", "r") as file:
            content = await file.read()
            print(f"读取到配置: {content}")
            
            result = await db.execute_query("SELECT * FROM config")
            print(result)


async def demo_async_context_with_exception():
    """演示异步上下文管理器中的异常处理"""
    print("\n=== 异步上下文管理器异常处理 ===")
    
    try:
        async with AsyncDatabaseConnection("localhost", 5432, "testdb") as db:
            # 模拟一个异常
            raise ValueError("模拟的数据库操作异常")
    except ValueError as e:
        print(f"捕获到异常: {e}")


async def demo_resource_pool():
    """演示资源池异步上下文管理器"""
    print("\n=== 资源池异步上下文管理器 ===")
    
    pool = AsyncResourcePool(pool_size=2)
    
    async def use_resource(resource_id):
        """使用资源的协程"""
        async with pool as resource:
            print(f"任务 {resource_id} 正在使用资源 {resource}")
            await asyncio.sleep(0.5)  # 模拟使用资源
            print(f"任务 {resource_id} 完成使用资源 {resource}")
    
    # 创建多个并发任务
    tasks = [
        use_resource(i) for i in range(4)
    ]
    
    # 由于资源池大小为2，最多同时有2个任务在使用资源
    await asyncio.gather(*tasks)


async def demo_custom_async_context():
    """演示自定义异步上下文管理器"""
    print("\n=== 自定义异步上下文管理器 ===")
    
    class AsyncTimer:
        """异步计时器上下文管理器"""
        
        def __init__(self, name):
            self.name = name
            self.start_time = None
        
        async def __aenter__(self):
            self.start_time = asyncio.get_event_loop().time()
            print(f"开始计时: {self.name}")
            return self
        
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            end_time = asyncio.get_event_loop().time()
            duration = end_time - self.start_time
            print(f"计时结束: {self.name}, 耗时: {duration:.2f}秒")
    
    async with AsyncTimer("数据库操作"):
        async with AsyncDatabaseConnection("localhost", 5432, "testdb") as db:
            await db.execute_query("SELECT * FROM users")
            await asyncio.sleep(1)  # 模拟操作耗时


if __name__ == "__main__":
    asyncio.run(demo_basic_async_context())
    asyncio.run(demo_nested_async_context())
    asyncio.run(demo_async_context_with_exception())
    asyncio.run(demo_resource_pool())
    asyncio.run(demo_custom_async_context()) 