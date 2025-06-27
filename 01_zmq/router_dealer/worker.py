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
        # 接收多帧消息（envelope + 内容）
        frames = socket.recv_multipart()
        if len(frames) < 2:
            print("收到的消息帧数不足，忽略。")
            continue
        identity, content = frames[0], frames[1]
        try:
            request = content.decode('utf-8')
        except Exception as e:
            print(f"内容解码失败: {e}")
            continue
        print(f"收到请求: {request}")
        
        # 处理请求
        time.sleep(1)
        
        # 发送响应（带上 envelope）
        response = f"已处理: {request}".encode('utf-8')
        socket.send_multipart([identity, response])
        print(f"已发送响应: {response.decode('utf-8')}")

if __name__ == "__main__":
    main() 