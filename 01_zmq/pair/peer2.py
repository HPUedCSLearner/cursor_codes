import zmq
import time

def main():
    # 创建 ZMQ 上下文
    context = zmq.Context()
    
    # 创建 PAIR 套接字
    socket = context.socket(zmq.PAIR)
    
    # 连接到对等节点1
    socket.connect("tcp://localhost:5555")
    
    print("对等节点2已启动...")
    
    while True:
        # 接收消息
        message = socket.recv_string()
        print(f"收到: {message}")
        
        # 发送响应
        response = "来自对等节点2的响应"
        socket.send_string(response)
        print(f"已发送: {response}")
        
        time.sleep(1)

if __name__ == "__main__":
    main() 