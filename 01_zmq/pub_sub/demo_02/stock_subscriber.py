import zmq
import sys

def main():
    # 创建 ZMQ 上下文
    context = zmq.Context()
    
    # 创建 SUB 套接字
    socket = context.socket(zmq.SUB)
    
    # 连接到发布者
    socket.connect("tcp://localhost:5555")
    
    # 获取要订阅的股票代码
    stock_code = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    socket.setsockopt_string(zmq.SUBSCRIBE, stock_code)
    
    print(f"股票订阅者已启动，正在订阅股票: {stock_code}")
    
    # 用于计算价格变化
    last_price = None
    
    while True:
        # 接收消息
        message = socket.recv_string()
        stock, price, timestamp = message.split()
        price = float(price)
        
        # 计算价格变化
        if last_price is not None:
            change = price - last_price
            change_percent = (change / last_price) * 100
            change_symbol = "↑" if change > 0 else "↓" if change < 0 else "="
            print(f"[{timestamp}] {stock}: ${price:.2f} {change_symbol} {abs(change_percent):.2f}%")
        else:
            print(f"[{timestamp}] {stock}: ${price:.2f}")
        
        last_price = price

if __name__ == "__main__":
    main() 