#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
协程意义：同步 vs 异步下载图片对比
"""

import time
import requests
import aiohttp
import asyncio


def download_image_sync(url):
    """同步下载图片"""
    print("开始下载:", url)
    # 发送网络请求，下载图片
    response = requests.get(url)
    print("下载完成")
    # 图片保存到本地文件
    file_name = url.rsplit('_')[-1]
    with open(file_name, mode='wb') as file_object:
        file_object.write(response.content)
    return file_name


async def download_image_async(session, url):
    """异步下载图片"""
    print("开始下载:", url)
    async with session.get(url, verify_ssl=False) as response:
        content = await response.content.read()
        file_name = url.rsplit('_')[-1]
        with open(file_name, mode='wb') as file_object:
            file_object.write(content)
        print('下载完成', url)
        return file_name


def sync_download():
    """同步下载方式"""
    print("=== 同步下载方式 ===")
    start_time = time.time()
    
    url_list = [
        'https://www3.autoimg.cn/newsdfs/g26/M02/35/A9/120x90_0_autohomecar__ChsEe12AXQ6AOOH_AAFocMs8nzU621.jpg',
        'https://www2.autoimg.cn/newsdfs/g30/M01/3C/E2/120x90_0_autohomecar__ChcCSV2BBICAUntfAADjJFd6800429.jpg',
        'https://www3.autoimg.cn/newsdfs/g26/M0B/3C/65/120x90_0_autohomecar__ChcCP12BFCmAIO83AAGq7vK0sGY193.jpg'
    ]
    
    for url in url_list:
        download_image_sync(url)
    
    end_time = time.time()
    print(f"同步下载耗时: {end_time - start_time:.2f}秒")


async def async_download():
    """异步下载方式"""
    print("=== 异步下载方式 ===")
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        url_list = [
            'https://www3.autoimg.cn/newsdfs/g26/M02/35/A9/120x90_0_autohomecar__ChsEe12AXQ6AOOH_AAFocMs8nzU621.jpg',
            'https://www2.autoimg.cn/newsdfs/g30/M01/3C/E2/120x90_0_autohomecar__ChcCSV2BBICAUntfAADjJFd6800429.jpg',
            'https://www3.autoimg.cn/newsdfs/g26/M0B/3C/65/120x90_0_autohomecar__ChcCP12BFCmAIO83AAGq7vK0sGY193.jpg'
        ]
        
        tasks = [asyncio.create_task(download_image_async(session, url)) for url in url_list]
        await asyncio.wait(tasks)
    
    end_time = time.time()
    print(f"异步下载耗时: {end_time - start_time:.2f}秒")


if __name__ == "__main__":
    # 同步下载
    sync_download()
    print()
    
    # 异步下载
    asyncio.run(async_download()) 