import zmq
import time
import random

def main():
    # 创建 ZMQ 上下文
    context = zmq.Context()
    
    # 创建 PUSH 套接字
    socket = context.socket(zmq.PUSH)
    
    # 绑定到端口 5555
    socket.bind("tcp://*:5555")
    
    print("推送者已启动...")
    
    # 等待所有工作器连接
    print("等待工作器连接...")
    time.sleep(1)
    
    # 发送任务
    for task_id in range(10):
        # 生成随机工作负载
        workload = random.randint(1, 100)
        message = f"任务 #{task_id} 工作负载: {workload}"
        
        # 发送任务
        socket.send_string(message)
        print(f"已发送: {message}")
        
        time.sleep(0.5)

if __name__ == "__main__":
    main() 