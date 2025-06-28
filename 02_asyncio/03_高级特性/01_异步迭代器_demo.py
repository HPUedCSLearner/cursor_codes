#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
异步迭代器演示
"""

import asyncio


class AsyncReader:
    """自定义异步迭代器（同时也是异步可迭代对象）"""
    
    def __init__(self, max_count=10):
        self.count = 0
        self.max_count = max_count
    
    async def readline(self):
        """模拟异步读取一行数据"""
        await asyncio.sleep(0.1)  # 模拟IO操作
        self.count += 1
        if self.count > self.max_count:
            return None
        return f"第{self.count}行数据"
    
    def __aiter__(self):
        """返回异步迭代器"""
        return self
    
    async def __anext__(self):
        """获取下一个值"""
        val = await self.readline()
        if val is None:
            raise StopAsyncIteration
        return val


class AsyncNumberGenerator:
    """异步数字生成器"""
    
    def __init__(self, start, end, delay=0.1):
        self.current = start
        self.end = end
        self.delay = delay
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.current >= self.end:
            raise StopAsyncIteration
        
        await asyncio.sleep(self.delay)  # 模拟异步操作
        result = self.current
        self.current += 1
        return result


async def demo_async_iterator_basic():
    """演示基本异步迭代器"""
    print("=== 基本异步迭代器 ===")
    
    obj = AsyncReader(max_count=5)
    async for item in obj:
        print(f"读取到: {item}")


async def demo_async_iterator_with_processing():
    """演示带处理的异步迭代器"""
    print("\n=== 带处理的异步迭代器 ===")
    
    async def process_data(data):
        """处理数据的异步函数"""
        await asyncio.sleep(0.05)
        return f"处理后的: {data}"
    
    obj = AsyncReader(max_count=3)
    async for item in obj:
        processed = await process_data(item)
        print(processed)


async def demo_async_number_generator():
    """演示异步数字生成器"""
    print("\n=== 异步数字生成器 ===")
    
    async for num in AsyncNumberGenerator(1, 6):
        print(f"生成数字: {num}")


async def demo_async_iterator_concurrent():
    """演示并发异步迭代器"""
    print("\n=== 并发异步迭代器 ===")
    
    async def concurrent_reader(name, max_count):
        """并发读取器"""
        reader = AsyncReader(max_count)
        async for item in reader:
            print(f"{name}: {item}")
            await asyncio.sleep(0.1)
    
    # 创建多个并发读取任务
    tasks = [
        concurrent_reader("读取器A", 3),
        concurrent_reader("读取器B", 3),
        concurrent_reader("读取器C", 3)
    ]
    
    await asyncio.gather(*tasks)


async def demo_async_iterator_with_filter():
    """演示带过滤的异步迭代器"""
    print("\n=== 带过滤的异步迭代器 ===")
    
    class FilteredAsyncReader(AsyncReader):
        """带过滤功能的异步读取器"""
        
        def __init__(self, max_count, filter_func):
            super().__init__(max_count)
            self.filter_func = filter_func
        
        async def __anext__(self):
            while True:
                val = await self.readline()
                if val is None:
                    raise StopAsyncIteration
                
                if self.filter_func(val):
                    return val
    
    # 创建过滤函数
    def is_even_line(data):
        """判断是否为偶数行"""
        try:
            line_num = int(data.split('第')[1].split('行')[0])
            return line_num % 2 == 0
        except:
            return False
    
    # 使用过滤的异步迭代器
    filtered_reader = FilteredAsyncReader(10, is_even_line)
    async for item in filtered_reader:
        print(f"过滤后: {item}")


async def demo_async_iterator_with_transform():
    """演示带转换的异步迭代器"""
    print("\n=== 带转换的异步迭代器 ===")
    
    class TransformAsyncReader(AsyncReader):
        """带转换功能的异步读取器"""
        
        def __init__(self, max_count, transform_func):
            super().__init__(max_count)
            self.transform_func = transform_func
        
        async def __anext__(self):
            val = await self.readline()
            if val is None:
                raise StopAsyncIteration
            
            return self.transform_func(val)
    
    # 转换函数
    def transform_data(data):
        """转换数据格式"""
        return f"转换后的数据: {data.upper()}"
    
    # 使用转换的异步迭代器
    transform_reader = TransformAsyncReader(5, transform_data)
    async for item in transform_reader:
        print(item)


if __name__ == "__main__":
    asyncio.run(demo_async_iterator_basic())
    asyncio.run(demo_async_iterator_with_processing())
    asyncio.run(demo_async_number_generator())
    asyncio.run(demo_async_iterator_concurrent())
    asyncio.run(demo_async_iterator_with_filter())
    asyncio.run(demo_async_iterator_with_transform()) 