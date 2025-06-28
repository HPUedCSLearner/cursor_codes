#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
greenlet实现协程
需要安装: pip install greenlet
"""

from greenlet import greenlet


def func1():
    print("func1 开始")
    print(1)        # 第1步：输出 1
    gr2.switch()    # 第3步：切换到 func2 函数
    print(2)        # 第6步：输出 2
    gr2.switch()    # 第7步：切换到 func2 函数，从上一次执行的位置继续向后执行
    print("func1 结束")


def func2():
    print("func2 开始")
    print(3)        # 第4步：输出 3
    gr1.switch()    # 第5步：切换到 func1 函数，从上一次执行的位置继续向后执行
    print(4)        # 第8步：输出 4
    print("func2 结束")


if __name__ == "__main__":
    # 创建greenlet对象
    gr1 = greenlet(func1)
    gr2 = greenlet(func2)
    
    print("开始执行协程...")
    gr1.switch() # 第1步：去执行 func1 函数
    print("协程执行完毕") 