# 企业微信集成使用说明

## 功能概述

本集成方案实现了企业微信与现有在线客服系统的对接，支持：
- 微信用户通过企业微信联系员工
- 自动回复和关键词匹配
- 智能转人工客服
- 消息双向同步

## 系统架构

```
微信用户 <-> 企业微信 <-> 企微集成模块 <-> 现有WebSocket客服系统
                              |
                              v
                         FAQ机器人/自动回复
```

## 配置步骤

### 1. 企业微信后台配置

1. 登录[企业微信管理后台](https://work.weixin.qq.com)
2. 创建自建应用：
   - 应用管理 -> 自建 -> 创建应用
   - 记录 `AgentId` 和 `Secret`

3. 配置客服功能：
   - 客户联系 -> 客服账号 -> 添加客服账号
   - 记录客服的 `Secret`

4. 设置接收消息：
   - 在应用详情页，设置"接收消息"的服务器配置
   - URL: `http://您的域名:3416/wecom/callback`
   - Token: 自定义（需要与配置文件一致）
   - EncodingAESKey: 随机生成

### 2. 修改配置文件

编辑 `wecom_config.py`：

```python
WECOM_CONFIG = {
    'corp_id': '您的企业ID',
    'agent_id': '您的应用ID',
    'agent_secret': '您的应用Secret',
    'kf_secret': '客服Secret',
    'token': '与企微后台一致的Token',
    'encoding_aes_key': '与企微后台一致的EncodingAESKey',
}
```

### 3. 安装依赖

```bash
pip install -r requirements_wecom.txt
```

### 4. 启动服务

#### 方式一：独立启动（推荐用于测试）

```bash
# 启动原有系统
python main.py

# 在另一个终端启动企微服务
python wecom_server.py
```

#### 方式二：整合启动（推荐用于生产）

```bash
# 使用整合版本启动
python main_with_wecom.py
```

## 自动回复配置

### 1. 关键词回复

在 `wecom_config.py` 中配置 `AUTO_REPLY_RULES`：

```python
'keyword_rules': [
    {
        'keywords': ['价格', '费用'],
        'reply': '关于价格问题...'
    }
]
```

### 2. FAQ知识库

系统会自动使用现有的FAQ机器人进行智能回复。

### 3. 转人工规则

当用户发送包含以下关键词时自动转人工：
- 人工
- 客服
- 转人工
- 人工客服

## API接口说明

### 1. 企微回调接口
- URL: `/wecom/callback`
- 方法: GET/POST
- 说明: 接收企业微信推送的消息

### 2. WebSocket接口
- URL: `/wecom/ws`
- 协议: WebSocket
- 说明: 实时消息通信

### 3. 发送消息到企微

```python
from wecom_api import WecomAPI

api = WecomAPI()
api.send_text_message(user_id, "消息内容")
```

## 消息流程

1. **接收消息**：
   - 微信用户发送消息到企业微信
   - 企微通过回调URL推送到系统
   - 系统解密并解析消息

2. **处理消息**：
   - 优先匹配关键词规则
   - 其次使用FAQ机器人
   - 无法回答则转人工

3. **回复消息**：
   - 通过企微API发送回复
   - 支持文本、图片等格式

## 监控和日志

日志文件位置：
- `faqrobot.log` - FAQ机器人日志
- 控制台输出 - 实时日志

## 常见问题

### Q: 如何测试企微集成？
A: 可以使用企业微信的"接口调试工具"进行测试。

### Q: 消息收不到怎么办？
A: 检查：
1. 回调URL是否可访问
2. Token和EncodingAESKey是否正确
3. 防火墙是否开放端口

### Q: 如何添加更多客服？
A: 在 `wecom_config.py` 的 `kf_accounts` 中添加映射关系。

### Q: 如何自定义自动回复规则？
A: 修改 `wecom_config.py` 中的 `AUTO_REPLY_RULES`。

## 安全建议

1. 使用HTTPS部署生产环境
2. 定期更换Secret和Token
3. 限制API调用频率
4. 记录所有消息日志

## 技术支持

如有问题，请查看日志文件或联系技术支持。