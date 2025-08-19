# coding=utf-8
"""
企业微信集成服务器
整合到现有的main.py系统中
"""
import tornado.ioloop
import tornado.web
import tornado.websocket
import logging
import asyncio
from wecom_handler import WecomCallbackHandler, WecomWebSocketHandler
from wecom_config import WECOM_CONFIG

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('wecom_server')

class WecomApplication(tornado.web.Application):
    """企业微信应用"""
    
    def __init__(self):
        handlers = [
            # 企业微信回调接口
            (r'/wecom/callback', WecomCallbackHandler),
            # 企业微信WebSocket接口
            (r'/wecom/ws', WecomWebSocketHandler),
        ]
        
        settings = {
            'debug': True,
            'autoreload': True
        }
        
        super().__init__(handlers, **settings)

def run_wecom_server(port=3417):
    """运行企业微信服务器"""
    app = WecomApplication()
    app.listen(port)
    logger.info(f"企业微信服务器启动在端口 {port}")
    logger.info(f"回调URL: http://your-domain:{port}/wecom/callback")
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    run_wecom_server()