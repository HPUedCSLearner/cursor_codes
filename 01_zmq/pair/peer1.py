import zmq
import time

def main():
    # 创建 ZMQ 上下文
    context = zmq.Context()
    
    # 创建 PAIR 套接字
    socket = context.socket(zmq.PAIR)
    
    # 绑定到端口 5555
    socket.bind("tcp://*:5555")
    
    print("对等节点1已启动...")
    
    while True:
        # 发送消息
        message = "来自对等节点1的消息"
        socket.send_string(message)
        print(f"已发送: {message}")
        
        # 接收消息
        response = socket.recv_string()
        print(f"收到: {response}")
        
        time.sleep(1)

if __name__ == "__main__":
    main() 