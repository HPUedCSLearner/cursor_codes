#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
事件循环 (Event Loop) 演示
"""

import asyncio


async def task1():
    print("任务1开始")
    await asyncio.sleep(2)
    print("任务1结束")
    return "任务1结果"


async def task2():
    print("任务2开始")
    await asyncio.sleep(1)
    print("任务2结束")
    return "任务2结果"


async def task3():
    print("任务3开始")
    await asyncio.sleep(3)
    print("任务3结束")
    return "任务3结果"


def demo_event_loop():
    """演示事件循环的基本使用"""
    print("=== 事件循环演示 ===")
    
    # 获取事件循环
    loop = asyncio.get_event_loop()
    
    # 创建任务列表
    tasks = [
        asyncio.ensure_future(task1()),
        asyncio.ensure_future(task2()),
        asyncio.ensure_future(task3())
    ]
    
    print("开始运行事件循环...")
    # 运行事件循环直到所有任务完成
    loop.run_until_complete(asyncio.wait(tasks))
    print("事件循环运行完毕")


def demo_asyncio_run():
    """演示asyncio.run()的使用 (Python 3.7+)"""
    print("\n=== asyncio.run() 演示 ===")
    
    async def main():
        # 创建任务
        t1 = asyncio.create_task(task1())
        t2 = asyncio.create_task(task2())
        t3 = asyncio.create_task(task3())
        
        # 等待所有任务完成
        results = await asyncio.gather(t1, t2, t3)
        print(f"所有任务结果: {results}")
    
    # 使用asyncio.run()运行
    asyncio.run(main())


if __name__ == "__main__":
    demo_event_loop()
    demo_asyncio_run() 