#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Task对象演示
"""

import asyncio


async def func():
    """模拟一个异步任务"""
    print("任务开始")
    await asyncio.sleep(2)
    print("任务结束")
    return "任务返回值"


async def demo_task_basic():
    """演示Task对象的基本使用"""
    print("=== Task对象基本使用 ===")
    
    print("main开始")
    
    # 创建Task对象，将当前执行func函数任务添加到事件循环
    task1 = asyncio.create_task(func(), name='task1')
    
    # 创建Task对象，将当前执行func函数任务添加到事件循环
    task2 = asyncio.create_task(func(), name='task2')
    
    print("main结束")
    
    # 当执行某协程遇到IO操作时，会自动化切换执行其他任务
    # 此处的await是等待相对应的协程全都执行完毕并获取结果
    ret1 = await task1
    ret2 = await task2
    print(f"任务1结果: {ret1}")
    print(f"任务2结果: {ret2}")


async def demo_task_list():
    """演示Task列表的使用"""
    print("\n=== Task列表使用 ===")
    
    print("main开始")
    
    task_list = [
        asyncio.create_task(func(), name='n1'),
        asyncio.create_task(func(), name='n2'),
        asyncio.create_task(func(), name='n3')
    ]
    
    print("main结束")
    
    # 等待所有任务完成
    done, pending = await asyncio.wait(task_list, timeout=None)
    print(f"完成的任务数量: {len(done)}")
    print(f"未完成的任务数量: {len(pending)}")
    
    # 获取任务结果
    for task in done:
        print(f"任务 {task.get_name()}: {task.result()}")


async def demo_task_gather():
    """演示asyncio.gather的使用"""
    print("\n=== asyncio.gather使用 ===")
    
    # 直接使用协程对象列表
    task_list = [
        func(),
        func(),
        func()
    ]
    
    # 使用gather等待所有任务完成并获取结果
    results = await asyncio.gather(*task_list)
    print(f"所有任务结果: {results}")


async def demo_task_timeout():
    """演示Task超时处理"""
    print("\n=== Task超时处理 ===")
    
    async def long_task():
        print("长时间任务开始")
        await asyncio.sleep(5)
        print("长时间任务结束")
        return "长时间任务完成"
    
    async def short_task():
        print("短时间任务开始")
        await asyncio.sleep(1)
        print("短时间任务结束")
        return "短时间任务完成"
    
    # 创建任务
    task1 = asyncio.create_task(long_task(), name='long_task')
    task2 = asyncio.create_task(short_task(), name='short_task')
    
    # 设置超时时间
    try:
        done, pending = await asyncio.wait([task1, task2], timeout=3)
        print(f"超时前完成的任务: {len(done)}")
        print(f"超时后仍在运行的任务: {len(pending)}")
        
        # 取消未完成的任务
        for task in pending:
            task.cancel()
            print(f"取消任务: {task.get_name()}")
            
    except asyncio.TimeoutError:
        print("任务执行超时")


if __name__ == "__main__":
    asyncio.run(demo_task_basic())
    asyncio.run(demo_task_list())
    asyncio.run(demo_task_gather())
    asyncio.run(demo_task_timeout()) 