import zmq
import time

def main():
    # 创建 ZMQ 上下文
    context = zmq.Context()
    
    # 创建 REQ 套接字（请求套接字）
    socket = context.socket(zmq.REQ)
    
    # 连接到服务器
    socket.connect("tcp://localhost:5555")
    
    print("客户端已启动，准备发送请求...")
    
    for request in range(5):
        # 发送请求
        message = f"请求 #{request + 1}"
        print(f"发送请求: {message}")
        socket.send_string(message)
        
        # 等待响应
        response = socket.recv_string()
        print(f"收到响应: {response}")
        
        # 等待一秒再发送下一个请求
        time.sleep(1)

if __name__ == "__main__":
    main() 