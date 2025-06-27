import zmq
import time

def main():
    # 创建 ZMQ 上下文
    context = zmq.Context()
    
    # 创建 REP 套接字（响应套接字）
    socket = context.socket(zmq.REP)
    
    # 绑定到端口 5555
    socket.bind("tcp://*:5555")
    
    print("服务器启动，等待客户端连接...")
    
    while True:
        # 等待客户端请求
        message = socket.recv_string()
        print(f"收到请求: {message}")
        
        # 模拟处理时间
        time.sleep(1)
        
        # 发送响应
        response = f"服务器已处理您的请求: {message}"
        socket.send_string(response)

if __name__ == "__main__":
    main() 