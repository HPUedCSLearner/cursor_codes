#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
await关键字演示
"""

import asyncio


async def others():
    """模拟一个异步操作"""
    print("others开始")
    await asyncio.sleep(2)
    print('others结束')
    return 'others返回值'


async def func1():
    """演示基本的await使用"""
    print("func1开始")
    
    # 遇到IO操作挂起当前协程，等IO操作完成之后再继续往下执行
    # 当前协程挂起时，事件循环可以去执行其他协程
    response = await others()
    
    print("IO请求结束，结果为：", response)


async def func2():
    """演示多个await的使用"""
    print("func2开始")
    
    # 第一个await
    response1 = await others()
    print("第一个IO请求结束，结果为：", response1)
    
    # 第二个await
    response2 = await others()
    print("第二个IO请求结束，结果为：", response2)


async def func3():
    """演示await的并发执行"""
    print("func3开始")
    
    # 创建多个任务，让它们并发执行
    task1 = asyncio.create_task(others())
    task2 = asyncio.create_task(others())
    
    # 等待所有任务完成
    response1, response2 = await asyncio.gather(task1, task2)
    print("并发IO请求结束，结果：", response1, response2)


async def demo_await():
    """演示不同的await使用方式"""
    print("=== await基本使用 ===")
    await func1()
    
    print("\n=== 多个await顺序执行 ===")
    await func2()
    
    print("\n=== await并发执行 ===")
    await func3()


if __name__ == "__main__":
    asyncio.run(demo_await()) 