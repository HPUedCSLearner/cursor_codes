#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
yield关键字实现协程
"""

def func1():
    print("func1 开始")
    yield 1
    print("func1 调用 func2")
    yield from func2()
    print("func1 继续")
    yield 2
    print("func1 结束")


def func2():
    print("func2 开始")
    yield 3
    print("func2 继续")
    yield 4
    print("func2 结束")


if __name__ == "__main__":
    print("开始执行yield协程...")
    f1 = func1()
    for item in f1:
        print(f"获取到值: {item}")
    print("yield协程执行完毕") 