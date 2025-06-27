import zmq
import sys

def main():
    # 创建 ZMQ 上下文
    context = zmq.Context()
    
    # 创建 SUB 套接字
    socket = context.socket(zmq.SUB)
    
    # 连接到发布者
    socket.connect("tcp://localhost:5555")
    
    # 设置要订阅的主题
    # 可以订阅多个主题，使用空格分隔
    topic_filter = sys.argv[1] if len(sys.argv) > 1 else "sports"
    socket.setsockopt_string(zmq.SUBSCRIBE, topic_filter)
    
    print(f"订阅者已启动，正在订阅主题: {topic_filter}")
    
    while True:
        # 接收消息
        message = socket.recv_string()
        print(f"收到消息: {message}")

if __name__ == "__main__":
    main() 