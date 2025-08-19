# coding=utf-8
"""
整合了企业微信功能的主服务器
"""
import tornado.ioloop
import tornado.web
import tornado.websocket
import os
import time
import logging
from collections import deque
import asyncio
import websockets
import json
import jieba
import jieba.posseg as pseg
import pymysql
import datetime

# 导入原有的模块
from main import (
    FAQrobot, ConnectHandler, MainHandler, RefreshHandler,
    words, serverChatDic, clientChatDic, clientChatEnList, serverChatEnList,
    zhishiku, loginSocket, agentDoClose, setStatus, getServerChatEnList,
    selectServerChatId, sendMsg, sendBuss, getKnList, getKnList10,
    serverQuit, getTransferUserSeatList, transNewSeat, retry_operation
)

# 导入企业微信模块
from wecom_handler import WecomCallbackHandler, WecomWebSocketHandler
from wecom_bridge import WecomBridge

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('main_with_wecom')

class IntegratedApplication(tornado.web.Application):
    """整合的应用程序"""
    
    def __init__(self, robot):
        self.robot = robot
        self.wecom_bridge = WecomBridge(robot)
        
        handlers = [
            # 原有的处理器
            (r'/index', MainHandler),
            (r'/ws', ConnectHandler),
            (r'/refresh', RefreshHandler),
            
            # 企业微信处理器
            (r'/wecom/callback', WecomCallbackHandler),
            (r'/wecom/ws', WecomWebSocketHandler),
        ]
        
        settings = {
            'debug': False,
            'autoreload': False
        }
        
        super().__init__(handlers, **settings)
        
        # 将robot和bridge传递给处理器
        for handler in handlers:
            handler[1].robot = robot
            handler[1].wecom_bridge = self.wecom_bridge

def main():
    """主函数"""
    # 初始化机器人
    robot = FAQrobot('0000', usedVec=False)
    
    # 创建应用
    app = IntegratedApplication(robot)
    
    # 监听端口
    port = 3416
    app.listen(port)
    
    logger.info(f"整合服务器启动在端口 {port}")
    logger.info(f"WebSocket地址: ws://localhost:{port}/ws")
    logger.info(f"企业微信回调地址: http://your-domain:{port}/wecom/callback")
    
    # 启动事件循环
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()