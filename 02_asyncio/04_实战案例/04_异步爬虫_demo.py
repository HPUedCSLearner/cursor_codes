#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
异步爬虫演示
需要安装: pip install aiohttp beautifulsoup4
"""

import asyncio
import aiohttp
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import os


class AsyncWebCrawler:
    """异步网络爬虫"""
    
    def __init__(self, max_concurrent=10, timeout=30):
        self.max_concurrent = max_concurrent
        self.timeout = timeout
        self.session = None
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.results = []
        self.visited_urls = set()
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        timeout_config = aiohttp.ClientTimeout(total=self.timeout)
        self.session = aiohttp.ClientSession(
            timeout=timeout_config,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()
    
    async def fetch_page(self, url):
        """获取页面内容"""
        async with self.semaphore:  # 限制并发数
            try:
                print(f"正在获取: {url}")
                async with self.session.get(url, ssl=False) as response:
                    if response.status == 200:
                        content = await response.text()
                        return {
                            'url': url,
                            'status': response.status,
                            'content': content,
                            'content_type': response.headers.get('content-type', ''),
                            'size': len(content)
                        }
                    else:
                        return {
                            'url': url,
                            'status': response.status,
                            'error': f"HTTP {response.status}"
                        }
            except Exception as e:
                return {
                    'url': url,
                    'status': 0,
                    'error': str(e)
                }
    
    async def parse_page(self, page_data):
        """解析页面内容"""
        if page_data['status'] != 200 or 'content' not in page_data:
            return page_data
        
        try:
            soup = BeautifulSoup(page_data['content'], 'html.parser')
            
            # 提取标题
            title = soup.find('title')
            page_data['title'] = title.get_text().strip() if title else '无标题'
            
            # 提取链接
            links = soup.find_all('a', href=True)
            page_data['links'] = [urljoin(page_data['url'], link['href']) for link in links]
            
            # 提取文本内容（简化版）
            text_content = soup.get_text()
            page_data['text_length'] = len(text_content)
            page_data['word_count'] = len(text_content.split())
            
            return page_data
        except Exception as e:
            page_data['parse_error'] = str(e)
            return page_data
    
    async def crawl_urls(self, urls):
        """爬取多个URL"""
        print(f"开始爬取 {len(urls)} 个URL...")
        start_time = time.time()
        
        # 创建获取任务
        fetch_tasks = [self.fetch_page(url) for url in urls]
        
        # 并发获取页面
        pages = await asyncio.gather(*fetch_tasks, return_exceptions=True)
        
        # 解析页面
        parse_tasks = []
        for page in pages:
            if isinstance(page, dict):
                parse_tasks.append(self.parse_page(page))
        
        # 并发解析页面
        results = await asyncio.gather(*parse_tasks, return_exceptions=True)
        
        # 过滤有效结果
        self.results = [r for r in results if isinstance(r, dict)]
        
        end_time = time.time()
        print(f"爬取完成，耗时: {end_time - start_time:.2f}秒")
        print(f"成功获取: {len([r for r in self.results if r.get('status') == 200])} 个页面")
        
        return self.results


async def demo_basic_crawler():
    """演示基本爬虫功能"""
    print("=== 基本爬虫功能 ===")
    
    urls = [
        'https://httpbin.org/get',
        'https://httpbin.org/post',
        'https://httpbin.org/status/200',
        'https://httpbin.org/status/404',
        'https://httpbin.org/delay/1',
        'https://httpbin.org/delay/2'
    ]
    
    async with AsyncWebCrawler(max_concurrent=3) as crawler:
        results = await crawler.crawl_urls(urls)
        
        for result in results:
            if result.get('status') == 200:
                print(f"✓ {result['url']} - 大小: {result.get('size', 0)} 字节")
            else:
                print(f"✗ {result['url']} - 错误: {result.get('error', '未知错误')}")


async def demo_content_parsing():
    """演示内容解析功能"""
    print("\n=== 内容解析功能 ===")
    
    urls = [
        'https://httpbin.org/html',
        'https://httpbin.org/json',
        'https://httpbin.org/xml'
    ]
    
    async with AsyncWebCrawler(max_concurrent=2) as crawler:
        results = await crawler.crawl_urls(urls)
        
        for result in results:
            if result.get('status') == 200:
                print(f"页面: {result['url']}")
                print(f"  标题: {result.get('title', 'N/A')}")
                print(f"  内容类型: {result.get('content_type', 'N/A')}")
                print(f"  文本长度: {result.get('text_length', 0)}")
                print(f"  链接数量: {len(result.get('links', []))}")
                print()


async def demo_error_handling():
    """演示错误处理"""
    print("\n=== 错误处理 ===")
    
    urls = [
        'https://httpbin.org/status/500',
        'https://httpbin.org/status/404',
        'https://invalid-domain-that-does-not-exist.com',
        'https://httpbin.org/delay/10',  # 超时
        'https://httpbin.org/get'
    ]
    
    async with AsyncWebCrawler(max_concurrent=2, timeout=5) as crawler:
        results = await crawler.crawl_urls(urls)
        
        for result in results:
            if result.get('status') == 200:
                print(f"✓ {result['url']} - 成功")
            else:
                print(f"✗ {result['url']} - 错误: {result.get('error', f'HTTP {result.get("status")}')}")


async def demo_concurrent_control():
    """演示并发控制"""
    print("\n=== 并发控制 ===")
    
    # 创建多个延迟URL来测试并发控制
    urls = [f'https://httpbin.org/delay/{i % 3 + 1}' for i in range(10)]
    
    start_time = time.time()
    
    async with AsyncWebCrawler(max_concurrent=3) as crawler:
        results = await crawler.crawl_urls(urls)
    
    end_time = time.time()
    
    success_count = len([r for r in results if r.get('status') == 200])
    print(f"并发控制测试完成:")
    print(f"  总URL数: {len(urls)}")
    print(f"  成功数: {success_count}")
    print(f"  总耗时: {end_time - start_time:.2f}秒")
    print(f"  平均每个URL: {(end_time - start_time) / len(urls):.2f}秒")


async def demo_data_extraction():
    """演示数据提取"""
    print("\n=== 数据提取 ===")
    
    urls = [
        'https://httpbin.org/json',
        'https://httpbin.org/html',
        'https://httpbin.org/xml'
    ]
    
    async with AsyncWebCrawler(max_concurrent=2) as crawler:
        results = await crawler.crawl_urls(urls)
        
        extracted_data = []
        
        for result in results:
            if result.get('status') == 200:
                data = {
                    'url': result['url'],
                    'title': result.get('title', 'N/A'),
                    'content_type': result.get('content_type', 'N/A'),
                    'size': result.get('size', 0),
                    'word_count': result.get('word_count', 0)
                }
                extracted_data.append(data)
        
        # 保存提取的数据
        with open('crawled_data.json', 'w', encoding='utf-8') as f:
            json.dump(extracted_data, f, ensure_ascii=False, indent=2)
        
        print(f"数据提取完成，保存到 crawled_data.json")
        print(f"提取了 {len(extracted_data)} 个页面的数据")


async def demo_performance_comparison():
    """演示性能对比（同步 vs 异步）"""
    print("\n=== 性能对比 ===")
    
    urls = [f'https://httpbin.org/delay/1' for _ in range(5)]
    
    # 异步方式
    print("异步方式:")
    start_time = time.time()
    async with AsyncWebCrawler(max_concurrent=5) as crawler:
        results = await crawler.crawl_urls(urls)
    async_time = time.time() - start_time
    print(f"  耗时: {async_time:.2f}秒")
    
    # 模拟同步方式（实际是串行异步）
    print("同步方式（模拟）:")
    start_time = time.time()
    async with AsyncWebCrawler(max_concurrent=1) as crawler:
        results = await crawler.crawl_urls(urls)
    sync_time = time.time() - start_time
    print(f"  耗时: {sync_time:.2f}秒")
    
    print(f"性能提升: {sync_time / async_time:.1f}x")


async def demo_custom_headers():
    """演示自定义请求头"""
    print("\n=== 自定义请求头 ===")
    
    # 创建带自定义头的爬虫
    timeout_config = aiohttp.ClientTimeout(total=30)
    headers = {
        'User-Agent': 'MyCustomBot/1.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }
    
    async with aiohttp.ClientSession(timeout=timeout_config, headers=headers) as session:
        urls = [
            'https://httpbin.org/headers',
            'https://httpbin.org/user-agent'
        ]
        
        for url in urls:
            try:
                async with session.get(url, ssl=False) as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"请求 {url}:")
                        print(f"  响应: {data}")
                        print()
            except Exception as e:
                print(f"请求 {url} 失败: {e}")


if __name__ == "__main__":
    # 运行所有演示
    asyncio.run(demo_basic_crawler())
    asyncio.run(demo_content_parsing())
    asyncio.run(demo_error_handling())
    asyncio.run(demo_concurrent_control())
    asyncio.run(demo_data_extraction())
    asyncio.run(demo_performance_comparison())
    asyncio.run(demo_custom_headers()) 