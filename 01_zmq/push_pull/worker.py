import zmq
import time
import random

def main():
    # 创建 ZMQ 上下文
    context = zmq.Context()
    
    # 创建 PULL 套接字
    socket = context.socket(zmq.PULL)
    
    # 连接到推送者
    socket.connect("tcp://localhost:5555")
    
    print("工作器已启动...")
    
    while True:
        # 接收任务
        message = socket.recv_string()
        print(f"收到任务: {message}")
        
        # 模拟处理任务
        time.sleep(random.uniform(0.5, 2.0))
        print(f"任务处理完成: {message}")

if __name__ == "__main__":
    main() 