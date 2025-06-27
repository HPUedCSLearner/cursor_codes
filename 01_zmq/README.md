# ZMQ 学习示例

这个项目包含了 ZMQ 的主要通信模式的示例代码。每个模式都在独立的目录中，包含完整的示例代码和说明。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 1. 请求-响应模式 (REQ-REP)

最基本的 ZMQ 模式，用于客户端-服务器通信。

运行方法：
```bash
# 终端1：启动服务器
python server.py

# 终端2：启动客户端
python client.py
```

## 2. 发布-订阅模式 (PUB-SUB)

用于一对多的消息发布，支持消息过滤。

运行方法：
```bash
# 终端1：启动发布者
python pub_sub/publisher.py

# 终端2：启动订阅者（可以指定订阅主题）
python pub_sub/subscriber.py sports
python pub_sub/subscriber.py news
python pub_sub/subscriber.py weather
```

## 3. 推-拉模式 (PUSH-PULL)

用于任务分发，适合并行处理。

运行方法：
```bash
# 终端1：启动推送者
python push_pull/ventilator.py

# 终端2和3：启动多个工作器
python push_pull/worker.py
python push_pull/worker.py
```

## 4. 路由器-经销商模式 (ROUTER-DEALER)

用于构建可扩展的请求-响应模式，支持多个客户端和多个工作器。

运行方法：
```bash
# 终端1：启动代理
python router_dealer/broker.py

# 终端2：启动工作器
python router_dealer/worker.py

# 终端3：启动客户端
python router_dealer/client.py
```

## 5. 对等模式 (PAIR)

用于两个对等节点之间的双向通信。

运行方法：
```bash
# 终端1：启动对等节点1
python pair/peer1.py

# 终端2：启动对等节点2
python pair/peer2.py
```

## 模式说明

1. **请求-响应 (REQ-REP)**
   - 最基本的模式
   - 客户端发送请求，服务器响应
   - 严格的一问一答模式

2. **发布-订阅 (PUB-SUB)**
   - 一对多的消息发布
   - 支持消息过滤
   - 发布者不知道订阅者的存在

3. **推-拉 (PUSH-PULL)**
   - 用于任务分发
   - 支持负载均衡
   - 适合并行处理

4. **路由器-经销商 (ROUTER-DEALER)**
   - 可扩展的请求-响应模式
   - 支持多个客户端和多个工作器
   - 适合构建代理服务器

5. **对等模式 (PAIR)**
   - 两个对等节点之间的双向通信
   - 最简单的模式
   - 适合点对点通信

## 注意事项

1. 运行示例时，请确保按照正确的顺序启动各个组件
2. 每个模式都可以启动多个实例进行测试
3. 观察控制台输出，了解消息的流动过程
4. 可以修改代码中的参数（如端口号、消息内容等）进行实验 