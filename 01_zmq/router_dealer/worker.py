import zmq
import time

def main():
    # 创建 ZMQ 上下文
    context = zmq.Context()
    
    # 创建 DEALER 套接字
    socket = context.socket(zmq.DEALER)
    
    # 连接到代理
    socket.connect("tcp://localhost:5556")
    
    print("工作器已启动...")
    
    while True:
        # 接收请求
        request = socket.recv_string()
        print(f"收到请求: {request}")
        
        # 处理请求
        time.sleep(1)
        
        # 发送响应
        response = f"已处理: {request}"
        socket.send_string(response)
        print(f"已发送响应: {response}")

if __name__ == "__main__":
    main() 