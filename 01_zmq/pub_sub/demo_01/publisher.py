import zmq
import time
import random

def main():
    # 创建 ZMQ 上下文
    context = zmq.Context()
    
    # 创建 PUB 套接字
    socket = context.socket(zmq.PUB)
    
    # 绑定到端口 5555
    socket.bind("tcp://*:5555")
    
    print("发布者已启动...")
    
    # 主题列表
    topics = ["sports", "news", "weather"]
    
    while True:
        # 随机选择一个主题
        topic = random.choice(topics)
        # 生成随机消息
        message = f"主题 {topic} 的更新: {random.randint(1, 100)}"
        
        # 发送消息（格式：主题 消息内容）
        socket.send_string(f"{topic} {message}")
        print(f"已发布: {message}")
        
        time.sleep(1)

if __name__ == "__main__":
    main() 