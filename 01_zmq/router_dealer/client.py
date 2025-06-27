import zmq
import time
import random

def main():
    # 创建 ZMQ 上下文
    context = zmq.Context()
    
    # 创建 DEALER 套接字
    socket = context.socket(zmq.DEALER)
    
    # 连接到代理
    socket.connect("tcp://localhost:5555")
    
    print("客户端已启动...")
    
    # 发送请求
    for request in range(5):
        # 生成随机请求
        message = f"请求 #{request + 1}"
        print(f"发送请求: {message}")
        
        # 发送请求
        socket.send_string(message)
        
        # 等待响应
        response = socket.recv_string()
        print(f"收到响应: {response}")
        
        time.sleep(1)

if __name__ == "__main__":
    main() 