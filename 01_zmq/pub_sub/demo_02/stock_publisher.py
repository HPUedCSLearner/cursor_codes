import zmq
import time
import random
from datetime import datetime

def generate_stock_data():
    """生成模拟的股票数据"""
    stocks = {
        "AAPL": 150.0,
        "GOOGL": 2800.0,
        "MSFT": 300.0,
        "AMZN": 3300.0,
        "TSLA": 900.0
    }
    
    # 随机选择一个股票
    stock = random.choice(list(stocks.keys()))
    # 生成随机价格变动（-2% 到 +2%）
    change = random.uniform(-0.02, 0.02)
    new_price = stocks[stock] * (1 + change)
    stocks[stock] = new_price
    
    return {
        "stock": stock,
        "price": round(new_price, 2),
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }

def main():
    # 创建 ZMQ 上下文
    context = zmq.Context()
    
    # 创建 PUB 套接字
    socket = context.socket(zmq.PUB)
    
    # 绑定到端口 5555
    socket.bind("tcp://*:5555")
    
    print("股票数据发布者已启动...")
    
    while True:
        # 生成股票数据
        data = generate_stock_data()
        
        # 构建消息（格式：股票代码 价格 时间戳）
        message = f"{data['stock']} {data['price']} {data['timestamp']}"
        
        # 发送消息
        socket.send_string(message)
        print(f"已发布: {message}")
        
        # 等待一秒
        time.sleep(1)

if __name__ == "__main__":
    main() 