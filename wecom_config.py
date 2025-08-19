# coding=utf-8
"""
企业微信配置文件
"""

# 企业微信配置
WECOM_CONFIG = {
    # 企业ID
    'corp_id': 'YOUR_CORP_ID',
    
    # 应用配置
    'agent_id': 'YOUR_AGENT_ID',
    'agent_secret': 'YOUR_AGENT_SECRET',
    
    # 客服消息配置
    'kf_secret': 'YOUR_KF_SECRET',  # 客服消息secret
    
    # 回调配置
    'token': 'YOUR_TOKEN',  # 用于验证回调URL
    'encoding_aes_key': 'YOUR_ENCODING_AES_KEY',  # 用于消息加解密
    
    # 客服账号配置
    'kf_accounts': {
        # 客服账号ID: 员工UserID的映射
        'kf_account_1': 'employee_userid_1',
        'kf_account_2': 'employee_userid_2',
    }
}

# 自动回复规则配置
AUTO_REPLY_RULES = {
    # 关键词回复
    'keyword_rules': [
        {
            'keywords': ['你好', '您好', 'hi', 'hello'],
            'reply': '您好！欢迎咨询，请问有什么可以帮助您的？'
        },
        {
            'keywords': ['价格', '费用', '多少钱'],
            'reply': '关于价格问题，请提供您具体想了解的产品或服务，我们会为您详细介绍。'
        },
        {
            'keywords': ['营业时间', '工作时间', '上班时间'],
            'reply': '我们的工作时间是：周一至周五 9:00-18:00，周末及节假日休息。'
        }
    ],
    
    # 默认回复
    'default_reply': '您好，您的消息已收到，我们会尽快为您处理。如需人工服务，请回复"人工"。',
    
    # 转人工关键词
    'transfer_keywords': ['人工', '客服', '转人工', '人工客服'],
    
    # 欢迎语
    'welcome_message': '您好！欢迎联系我们，我是智能客服助手，有什么可以帮助您的吗？',
    
    # 超时未回复提醒（秒）
    'timeout_seconds': 300,  # 5分钟
    'timeout_message': '您好，由于长时间未收到您的消息，本次会话即将结束。如需继续咨询，请重新发送消息。'
}

# WebSocket服务器配置（连接到现有系统）
WEBSOCKET_CONFIG = {
    'host': 'localhost',
    'port': 3416,
    'url': 'ws://localhost:3416/ws'
}

# 数据库配置（与现有系统保持一致）
DB_CONFIG = {
    'host': '192.168.0.124',
    'port': 3306,
    'db': 'webcast',
    'user': 'root',
    'password': 'ab_276@WQF',
    'charset': 'utf8'
}