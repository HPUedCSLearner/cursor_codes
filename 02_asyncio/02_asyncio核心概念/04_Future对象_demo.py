#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Future对象演示
"""

import asyncio


async def demo_future_basic():
    """演示Future对象的基本使用"""
    print("=== Future对象基本使用 ===")
    
    # 获取当前事件循环
    loop = asyncio.get_running_loop()
    
    # 创建一个任务（Future对象），这个任务什么都不干
    fut = loop.create_future()
    
    print("Future对象已创建，等待结果...")
    
    # 等待任务最终结果（Future对象），没有结果则会一直等下去
    # 注意：这个例子会一直等待，因为没有设置结果
    # await fut


async def demo_future_with_result():
    """演示设置Future结果"""
    print("\n=== 设置Future结果 ===")
    
    # 获取当前事件循环
    loop = asyncio.get_running_loop()
    
    # 创建一个任务（Future对象），没绑定任何行为
    fut = loop.create_future()
    
    async def set_after(fut):
        """2秒后设置Future的结果"""
        await asyncio.sleep(2)
        fut.set_result("666")
        print("Future结果已设置")
    
    # 创建一个任务（Task对象），绑定了set_after函数
    # 函数内部在2s之后，会给fut赋值
    await loop.create_task(set_after(fut))
    
    # 等待Future对象获取最终结果，否则一直等下去
    data = await fut
    print(f"获取到Future结果: {data}")


async def demo_future_exception():
    """演示Future异常处理"""
    print("\n=== Future异常处理 ===")
    
    loop = asyncio.get_running_loop()
    fut = loop.create_future()
    
    async def set_exception(fut):
        """设置Future异常"""
        await asyncio.sleep(1)
        fut.set_exception(ValueError("这是一个测试异常"))
        print("Future异常已设置")
    
    await loop.create_task(set_exception(fut))
    
    try:
        data = await fut
        print(f"获取到结果: {data}")
    except ValueError as e:
        print(f"捕获到异常: {e}")


async def demo_future_cancel():
    """演示Future取消"""
    print("\n=== Future取消 ===")
    
    loop = asyncio.get_running_loop()
    fut = loop.create_future()
    
    async def cancel_future(fut):
        """1秒后取消Future"""
        await asyncio.sleep(1)
        fut.cancel()
        print("Future已取消")
    
    await loop.create_task(cancel_future(fut))
    
    try:
        data = await fut
        print(f"获取到结果: {data}")
    except asyncio.CancelledError:
        print("Future被取消")


async def demo_future_done_callback():
    """演示Future完成回调"""
    print("\n=== Future完成回调 ===")
    
    def callback(fut):
        """Future完成时的回调函数"""
        if fut.cancelled():
            print("Future被取消")
        elif fut.exception():
            print(f"Future发生异常: {fut.exception()}")
        else:
            print(f"Future完成，结果: {fut.result()}")
    
    loop = asyncio.get_running_loop()
    fut = loop.create_future()
    
    # 添加完成回调
    fut.add_done_callback(callback)
    
    async def set_result(fut):
        """设置Future结果"""
        await asyncio.sleep(1)
        fut.set_result("Future完成")
    
    await loop.create_task(set_result(fut))
    await fut


if __name__ == "__main__":
    # 注意：第一个demo会无限等待，所以注释掉
    # asyncio.run(demo_future_basic())
    
    asyncio.run(demo_future_with_result())
    asyncio.run(demo_future_exception())
    asyncio.run(demo_future_cancel())
    asyncio.run(demo_future_done_callback()) 