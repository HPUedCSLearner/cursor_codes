import zmq
import time

def main():
    # 创建 ZMQ 上下文
    context = zmq.Context()
    
    # 创建 ROUTER 套接字（前端）
    frontend = context.socket(zmq.ROUTER)
    frontend.bind("tcp://*:5555")
    
    # 创建 DEALER 套接字（后端）
    backend = context.socket(zmq.DEALER)
    backend.bind("tcp://*:5556")
    
    print("代理已启动...")
    
    # 使用代理模式转发消息
    zmq.proxy(frontend, backend)

if __name__ == "__main__":
    main() 