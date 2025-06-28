#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
async/await关键字实现协程 (Python 3.5+)
"""

import asyncio


async def func1():
    print("func1 开始")
    # 网络IO请求：下载一张图片
    await asyncio.sleep(2)  # 遇到IO耗时操作，自动化切换到tasks中的其他任务
    print("func1 结束")


async def func2():
    print("func2 开始")
    # 网络IO请求：下载一张图片
    await asyncio.sleep(2)  # 遇到IO耗时操作，自动化切换到tasks中的其他任务
    print("func2 结束")


if __name__ == "__main__":
    print("开始执行async/await协程...")
    
    tasks = [
        asyncio.ensure_future(func1()),
        asyncio.ensure_future(func2())
    ]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    
    print("async/await协程执行完毕") 