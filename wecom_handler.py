# coding=utf-8
"""
企业微信消息处理模块
"""
import tornado.web
import tornado.websocket
import xml.etree.ElementTree as ET
import json
import time
import logging
import asyncio
from datetime import datetime
from wecom_config import WECOM_CONFIG, AUTO_REPLY_RULES
from wecom_crypto import WXBizMsgCrypt
from wecom_api import WecomAPI
import websockets

logger = logging.getLogger('wecom_handler')

class WecomCallbackHandler(tornado.web.RequestHandler):
    """企业微信回调处理器"""
    
    def initialize(self):
        """初始化"""
        self.wxcrypt = WXBizMsgCrypt(
            WECOM_CONFIG['token'],
            WECOM_CONFIG['encoding_aes_key'],
            WECOM_CONFIG['corp_id']
        )
        self.wecom_api = WecomAPI()
        self.ws_client = None
    
    def get(self):
        """验证URL有效性（企业微信会调用）"""
        msg_signature = self.get_argument('msg_signature', '')
        timestamp = self.get_argument('timestamp', '')
        nonce = self.get_argument('nonce', '')
        echostr = self.get_argument('echostr', '')
        
        ret, reply_echostr = self.wxcrypt.VerifyURL(msg_signature, timestamp, nonce, echostr)
        
        if ret == 0:
            self.write(reply_echostr)
            logger.info("URL验证成功")
        else:
            logger.error(f"URL验证失败: {ret}")
            self.write("")
    
    async def post(self):
        """处理企业微信推送的消息"""
        msg_signature = self.get_argument('msg_signature', '')
        timestamp = self.get_argument('timestamp', '')
        nonce = self.get_argument('nonce', '')
        
        # 获取POST数据
        post_data = self.request.body.decode('utf-8')
        
        # 解密消息
        ret, xml_content = self.wxcrypt.DecryptMsg(post_data, msg_signature, timestamp, nonce)
        
        if ret != 0:
            logger.error(f"解密消息失败: {ret}")
            self.write("")
            return
        
        # 解析XML消息
        xml_tree = ET.fromstring(xml_content)
        msg_type = xml_tree.find("MsgType").text
        
        # 处理不同类型的消息
        if msg_type == "event":
            await self.handle_event(xml_tree)
        elif msg_type == "text":
            await self.handle_text_message(xml_tree)
        elif msg_type == "image":
            await self.handle_image_message(xml_tree)
        else:
            logger.info(f"收到其他类型消息: {msg_type}")
        
        # 返回成功
        self.write("")
    
    async def handle_event(self, xml_tree):
        """处理事件消息"""
        event = xml_tree.find("Event").text
        
        if event == "kf_msg_or_event":
            # 客服消息事件
            token = xml_tree.find("Token").text
            await self.handle_kf_event(token)
        elif event == "enter_agent":
            # 用户进入应用
            from_user = xml_tree.find("FromUserName").text
            await self.send_welcome_message(from_user)
        else:
            logger.info(f"收到事件: {event}")
    
    async def handle_kf_event(self, token):
        """处理客服事件"""
        # 获取客服消息详情
        # 这里需要调用企业微信API获取具体消息内容
        pass
    
    async def handle_text_message(self, xml_tree):
        """处理文本消息"""
        from_user = xml_tree.find("FromUserName").text
        content = xml_tree.find("Content").text
        msg_id = xml_tree.find("MsgId").text
        
        logger.info(f"收到文本消息 - 用户: {from_user}, 内容: {content}")
        
        # 检查是否需要转人工
        if any(keyword in content for keyword in AUTO_REPLY_RULES['transfer_keywords']):
            await self.transfer_to_agent(from_user, content)
            return
        
        # 尝试关键词匹配
        reply = self.match_keyword_reply(content)
        
        if reply:
            # 发送关键词回复
            self.wecom_api.send_text_message(from_user, reply)
        else:
            # 转发到现有客服系统处理
            await self.forward_to_websocket(from_user, content, "text")
    
    async def handle_image_message(self, xml_tree):
        """处理图片消息"""
        from_user = xml_tree.find("FromUserName").text
        pic_url = xml_tree.find("PicUrl").text
        media_id = xml_tree.find("MediaId").text
        
        logger.info(f"收到图片消息 - 用户: {from_user}, MediaId: {media_id}")
        
        # 转发到现有客服系统
        await self.forward_to_websocket(from_user, pic_url, "image", media_id)
    
    def match_keyword_reply(self, content):
        """匹配关键词回复"""
        for rule in AUTO_REPLY_RULES['keyword_rules']:
            if any(keyword in content for keyword in rule['keywords']):
                return rule['reply']
        return None
    
    async def send_welcome_message(self, user_id):
        """发送欢迎消息"""
        self.wecom_api.send_text_message(user_id, AUTO_REPLY_RULES['welcome_message'])
    
    async def transfer_to_agent(self, user_id, content):
        """转接人工客服"""
        # 发送转接提示
        self.wecom_api.send_text_message(user_id, "正在为您转接人工客服，请稍候...")
        
        # 通过WebSocket通知客服系统
        await self.forward_to_websocket(user_id, content, "transfer")
    
    async def forward_to_websocket(self, user_id, content, msg_type, media_id=None):
        """转发消息到现有WebSocket系统"""
        try:
            # 连接到现有的WebSocket服务器
            from wecom_config import WEBSOCKET_CONFIG
            
            async with websockets.connect(WEBSOCKET_CONFIG['url']) as websocket:
                # 构造消息格式（与现有系统兼容）
                client_chat_id = f"wecom_{user_id}"
                
                # 登录消息
                login_msg = f"cmd@login;type@client;cont@{{'clientChatId':'{client_chat_id}','clientChatName':'企微用户_{user_id[-4:]}'}}"
                await websocket.send(login_msg)
                
                # 发送消息
                if msg_type == "text":
                    # 发送到机器人
                    send_msg = f"cmd@sendMsg;type@robot;cont@{{"
                    send_msg += f"'serverChatId':'','clientChatId':'{client_chat_id}',"
                    send_msg += f"'content':'{content}','contentType':'text',"
                    send_msg += f"'role':'client','chatState':'robot',"
                    send_msg += f"'avatarUrl':'static/image/im_client_avatar.png',"
                    send_msg += f"'source':'wecom','idcard':'','phone':'','uId':'','orderNo':''"
                    send_msg += f"}}"
                    await websocket.send(send_msg)
                elif msg_type == "image":
                    send_msg = f"cmd@sendMsg;type@client;cont@{{"
                    send_msg += f"'serverChatId':'','clientChatId':'{client_chat_id}',"
                    send_msg += f"'content':'[图片]','contentType':'image',"
                    send_msg += f"'fileUrl':'{content}','role':'client',"
                    send_msg += f"'chatState':'client','avatarUrl':'static/image/im_client_avatar.png',"
                    send_msg += f"'source':'wecom','idcard':'','phone':'','uId':'','orderNo':''"
                    send_msg += f"}}"
                    await websocket.send(send_msg)
                elif msg_type == "transfer":
                    # 请求人工客服
                    send_msg = f"cmd@getServerChatEnList;type@;cont@{{'clientChatId':'{client_chat_id}'}}"
                    await websocket.send(send_msg)
                
                # 等待回复
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                
                # 解析回复并发送给企微用户
                await self.handle_websocket_response(user_id, response)
                
        except Exception as e:
            logger.error(f"WebSocket通信失败: {e}")
            # 发送默认回复
            self.wecom_api.send_text_message(user_id, AUTO_REPLY_RULES['default_reply'])
    
    async def handle_websocket_response(self, user_id, response):
        """处理WebSocket响应"""
        try:
            # 解析响应（根据现有系统的格式）
            if "cmd':'sendMsg" in response:
                # 提取消息内容
                import re
                content_match = re.search(r"'content':'([^']*)'", response)
                if content_match:
                    content = content_match.group(1)
                    # 发送给企微用户
                    self.wecom_api.send_text_message(user_id, content)
            elif "serverChatId" in response and "serverChatName" in response:
                # 分配了客服
                import re
                name_match = re.search(r"'serverChatName':'([^']*)'", response)
                if name_match:
                    server_name = name_match.group(1)
                    self.wecom_api.send_text_message(
                        user_id, 
                        f"已为您分配客服 {server_name}，正在连接..."
                    )
        except Exception as e:
            logger.error(f"处理WebSocket响应失败: {e}")


class WecomWebSocketHandler(tornado.websocket.WebSocketHandler):
    """企业微信WebSocket处理器（用于实时通信）"""
    
    clients = set()
    wecom_api = WecomAPI()
    
    def check_origin(self, origin):
        """允许跨域"""
        return True
    
    def open(self):
        """连接建立"""
        self.clients.add(self)
        logger.info("企微WebSocket连接建立")
    
    def on_close(self):
        """连接关闭"""
        self.clients.remove(self)
        logger.info("企微WebSocket连接关闭")
    
    def on_message(self, message):
        """接收消息"""
        try:
            data = json.loads(message)
            cmd = data.get('cmd')
            
            if cmd == 'send_to_wecom':
                # 发送消息到企微用户
                user_id = data.get('user_id')
                content = data.get('content')
                msg_type = data.get('msg_type', 'text')
                
                if msg_type == 'text':
                    self.wecom_api.send_text_message(user_id, content)
                
                # 回复确认
                self.write_message(json.dumps({
                    'status': 'success',
                    'msg': '消息已发送'
                }))
            
        except Exception as e:
            logger.error(f"处理WebSocket消息失败: {e}")
            self.write_message(json.dumps({
                'status': 'error',
                'msg': str(e)
            }))