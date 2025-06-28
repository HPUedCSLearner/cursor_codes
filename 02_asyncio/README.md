# Python 异步编程 (asyncio) 完整教程

本教程涵盖了Python异步编程的完整知识体系，从基础概念到实战应用。

## 📚 目录结构

```
02_asyncio/
├── 01_协程基础/           # 协程基础概念和实现方式
├── 02_asyncio核心概念/     # asyncio模块核心概念
├── 03_高级特性/           # 异步迭代器、上下文管理器等
├── 04_实战案例/           # 实际项目应用
└── README.md             # 本文件
```

## 🎯 学习目标

- 理解协程的概念和实现方式
- 掌握asyncio模块的核心功能
- 学会异步编程的最佳实践
- 能够构建高性能的异步应用

## 📖 详细内容

### 1. 协程基础 (`01_协程基础/`)

#### 1.1 greenlet实现协程
- **文件**: `01_greenlet_demo.py`
- **内容**: 使用greenlet库实现协程切换
- **特点**: 早期协程实现方式，手动控制切换

#### 1.2 yield关键字
- **文件**: `02_yield_demo.py`
- **内容**: 使用yield实现生成器协程
- **特点**: Python内置的协程实现方式

#### 1.3 asyncio装饰器
- **文件**: `03_asyncio_decorator_demo.py`
- **内容**: Python 3.4+的@asyncio.coroutine装饰器
- **特点**: 早期asyncio实现方式

#### 1.4 async/await关键字
- **文件**: `04_async_await_demo.py`
- **内容**: Python 3.5+的现代异步语法
- **特点**: 推荐的异步编程方式

#### 1.5 协程意义对比
- **文件**: `05_协程意义对比_demo.py`
- **内容**: 同步vs异步下载图片的性能对比
- **特点**: 展示异步编程的性能优势

### 2. asyncio核心概念 (`02_asyncio核心概念/`)

#### 2.1 事件循环
- **文件**: `01_事件循环_demo.py`
- **内容**: 事件循环的基本使用和任务调度
- **特点**: asyncio的核心机制

#### 2.2 await关键字
- **文件**: `02_await关键字_demo.py`
- **内容**: await的使用方式和并发控制
- **特点**: 异步编程的核心语法

#### 2.3 Task对象
- **文件**: `03_Task对象_demo.py`
- **内容**: Task的创建、管理和并发执行
- **特点**: 异步任务的高级管理

#### 2.4 Future对象
- **文件**: `04_Future对象_demo.py`
- **内容**: Future的基本操作和结果处理
- **特点**: 异步操作的底层机制

#### 2.5 线程池集成
- **文件**: `05_线程池集成_demo.py`
- **内容**: asyncio与线程池、进程池的集成
- **特点**: 混合编程模式

### 3. 高级特性 (`03_高级特性/`)

#### 3.1 异步迭代器
- **文件**: `01_异步迭代器_demo.py`
- **内容**: 自定义异步迭代器和async for的使用
- **特点**: 异步数据流处理

#### 3.2 异步上下文管理器
- **文件**: `02_异步上下文管理器_demo.py`
- **内容**: async with的使用和自定义实现
- **特点**: 异步资源管理

### 4. 实战案例 (`04_实战案例/`)

#### 4.1 异步Redis
- **文件**: `01_异步Redis_demo.py`
- **内容**: 使用aioredis进行异步Redis操作
- **特点**: 缓存和消息队列的异步处理

#### 4.2 异步MySQL
- **文件**: `02_异步MySQL_demo.py`
- **内容**: 使用aiomysql进行异步数据库操作
- **特点**: 数据库的异步访问

#### 4.3 FastAPI
- **文件**: `03_FastAPI_demo.py`
- **内容**: 使用FastAPI构建异步Web API
- **特点**: 现代异步Web框架

#### 4.4 异步爬虫
- **文件**: `04_异步爬虫_demo.py`
- **内容**: 使用aiohttp构建高性能爬虫
- **特点**: 网络IO密集型应用

## 🚀 快速开始

### 环境准备

```bash
# 安装基础依赖
pip install asyncio

# 安装实战案例依赖
pip install aiohttp aioredis aiomysql fastapi uvicorn beautifulsoup4 greenlet
```

### 运行示例

```bash
# 运行协程基础示例
python 01_协程基础/01_greenlet_demo.py

# 运行asyncio核心概念示例
python 02_asyncio核心概念/01_事件循环_demo.py

# 运行实战案例
python 04_实战案例/01_异步Redis_demo.py
```

## 📋 学习路径

### 初学者路径
1. 从 `01_协程基础/` 开始，理解协程概念
2. 学习 `02_asyncio核心概念/` 掌握基础语法
3. 尝试 `03_高级特性/` 了解高级用法
4. 实践 `04_实战案例/` 应用所学知识

### 进阶路径
1. 深入理解事件循环机制
2. 掌握Task和Future的高级用法
3. 学习异步设计模式
4. 构建复杂的异步应用

## 🔧 最佳实践

### 1. 异步函数设计
- 使用 `async def` 定义异步函数
- 合理使用 `await` 等待异步操作
- 避免在异步函数中使用阻塞操作

### 2. 错误处理
- 使用 `try/except` 处理异步异常
- 合理设置超时时间
- 实现优雅的错误恢复机制

### 3. 性能优化
- 合理控制并发数量
- 使用连接池管理资源
- 避免创建过多的Task对象

### 4. 调试技巧
- 使用 `asyncio.create_task()` 创建可调试的任务
- 合理使用日志记录异步操作
- 使用调试工具监控事件循环

## 🎓 进阶主题

### 1. 异步设计模式
- 生产者-消费者模式
- 发布-订阅模式
- 异步工厂模式

### 2. 性能调优
- 事件循环优化
- 内存使用优化
- 网络IO优化

### 3. 分布式异步
- 异步微服务
- 异步消息队列
- 异步缓存策略

## 📚 参考资料

- [Python asyncio官方文档](https://docs.python.org/3/library/asyncio.html)
- [PEP 492 - Coroutines with async and await syntax](https://www.python.org/dev/peps/pep-0492/)
- [FastAPI官方文档](https://fastapi.tiangolo.com/)
- [aiohttp官方文档](https://docs.aiohttp.org/)

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个教程！

## 📄 许可证

MIT License

---

**注意**: 运行示例代码前，请确保相关服务（如Redis、MySQL）已正确配置并运行。 




# Others

## vedio link
https://www.bilibili.com/video/BV1NA411g7yf/?spm_id_from=333.1387.favlist.content.click&vd_source=ddaa7cd556186574491ea632ad077d44

## 心得

1. 使用场景
用户级别异步编程，本质是事件循环，感觉和poll，epool很像；
伪并发，其实质是，同一时刻，只能执行一个代码，但当执行到await操作的时候，可以执行其他函数的代码
增加了单线程的并发量，利用率，并且开销小于多线程、多继承