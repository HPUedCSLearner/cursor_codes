#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
asyncio与线程池集成演示
"""

import time
import asyncio
import concurrent.futures


def blocking_func(value):
    """阻塞函数，模拟耗时操作"""
    time.sleep(1)
    print(f"阻塞函数执行: {value}")
    return f"阻塞函数结果: {value}"


async def demo_default_executor():
    """演示默认线程池执行器"""
    print("=== 默认线程池执行器 ===")
    
    loop = asyncio.get_running_loop()
    
    # 使用默认的ThreadPoolExecutor
    # 第一步：内部会先调用ThreadPoolExecutor的submit方法去线程池中申请一个线程去执行blocking_func函数
    # 第二步：调用asyncio.wrap_future将concurrent.futures.Future对象包装为asyncio.Future对象
    fut = loop.run_in_executor(None, blocking_func, "默认线程池")
    result = await fut
    print(f'默认线程池结果: {result}')


async def demo_custom_thread_pool():
    """演示自定义线程池"""
    print("\n=== 自定义线程池 ===")
    
    loop = asyncio.get_running_loop()
    
    # 使用自定义线程池
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        # 创建多个任务
        tasks = []
        for i in range(3):
            task = loop.run_in_executor(pool, blocking_func, f"自定义线程池任务{i}")
            tasks.append(task)
        
        # 等待所有任务完成
        results = await asyncio.gather(*tasks)
        print(f'自定义线程池结果: {results}')


async def demo_process_pool():
    """演示进程池"""
    print("\n=== 进程池 ===")
    
    def cpu_intensive_func(n):
        """CPU密集型函数"""
        result = 0
        for i in range(n):
            result += i * i
        print(f"CPU密集型计算完成: {n}")
        return result
    
    loop = asyncio.get_running_loop()
    
    # 使用进程池处理CPU密集型任务
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as pool:
        tasks = []
        for i in [1000000, 2000000, 3000000]:
            task = loop.run_in_executor(pool, cpu_intensive_func, i)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        print(f'进程池结果: {results}')


async def demo_mixed_operations():
    """演示混合操作：异步IO + 线程池"""
    print("\n=== 混合操作演示 ===")
    
    async def async_io_operation(name):
        """模拟异步IO操作"""
        print(f"开始异步IO操作: {name}")
        await asyncio.sleep(1)
        print(f"完成异步IO操作: {name}")
        return f"异步IO结果: {name}"
    
    loop = asyncio.get_running_loop()
    
    # 混合任务：异步IO + 线程池
    async_tasks = [
        async_io_operation("任务1"),
        async_io_operation("任务2")
    ]
    
    thread_tasks = [
        loop.run_in_executor(None, blocking_func, "线程任务1"),
        loop.run_in_executor(None, blocking_func, "线程任务2")
    ]
    
    # 并发执行所有任务
    all_tasks = async_tasks + thread_tasks
    results = await asyncio.gather(*all_tasks)
    
    print(f"混合操作结果: {results}")


async def demo_requests_with_thread_pool():
    """演示使用线程池处理requests（不支持异步的库）"""
    print("\n=== requests + 线程池 ===")
    
    import requests
    
    def download_url(url):
        """使用requests下载URL"""
        print(f"开始下载: {url}")
        response = requests.get(url, timeout=10)
        print(f"下载完成: {url}, 状态码: {response.status_code}")
        return f"{url}: {response.status_code}"
    
    loop = asyncio.get_running_loop()
    
    urls = [
        'https://httpbin.org/get',
        'https://httpbin.org/post',
        'https://httpbin.org/status/200'
    ]
    
    # 使用线程池处理requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        tasks = [
            loop.run_in_executor(pool, download_url, url)
            for url in urls
        ]
        
        results = await asyncio.gather(*tasks)
        print(f"下载结果: {results}")


if __name__ == "__main__":
    asyncio.run(demo_default_executor())
    asyncio.run(demo_custom_thread_pool())
    asyncio.run(demo_process_pool())
    asyncio.run(demo_mixed_operations())
    asyncio.run(demo_requests_with_thread_pool()) 