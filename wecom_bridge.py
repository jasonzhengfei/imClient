# coding=utf-8
"""
企业微信与现有系统的桥接模块
"""
import json
import logging
import asyncio
import websockets
from datetime import datetime
from wecom_api import WecomAPI
from wecom_config import AUTO_REPLY_RULES, WEBSOCKET_CONFIG

logger = logging.getLogger('wecom_bridge')

class WecomBridge:
    """企业微信桥接器"""
    
    def __init__(self, robot):
        self.robot = robot
        self.wecom_api = WecomAPI()
        self.user_sessions = {}  # 用户会话管理
        
    async def process_wecom_message(self, user_id, content, msg_type="text"):
        """处理企业微信消息"""
        
        # 创建或获取用户会话
        session = self.get_or_create_session(user_id)
        
        # 检查是否需要转人工
        if self.check_transfer_keywords(content):
            return await self.transfer_to_agent(user_id, session)
        
        # 尝试机器人回复
        robot_reply = self.get_robot_reply(content)
        
        if robot_reply and robot_reply != 'noanswer':
            # 机器人可以回答
            await self.send_reply_to_wecom(user_id, robot_reply)
            self.update_session(session, content, robot_reply)
            return robot_reply
        else:
            # 需要人工处理
            return await self.forward_to_agent(user_id, content, session)
    
    def get_or_create_session(self, user_id):
        """获取或创建用户会话"""
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {
                'user_id': user_id,
                'client_chat_id': f'wecom_{user_id}',
                'server_chat_id': None,
                'start_time': datetime.now(),
                'last_active': datetime.now(),
                'messages': [],
                'status': 'robot'  # robot/waiting/agent
            }
        else:
            self.user_sessions[user_id]['last_active'] = datetime.now()
        
        return self.user_sessions[user_id]
    
    def check_transfer_keywords(self, content):
        """检查是否包含转人工关键词"""
        return any(keyword in content for keyword in AUTO_REPLY_RULES['transfer_keywords'])
    
    def get_robot_reply(self, content):
        """获取机器人回复"""
        # 先检查关键词规则
        for rule in AUTO_REPLY_RULES['keyword_rules']:
            if any(keyword in content for keyword in rule['keywords']):
                return rule['reply']
        
        # 使用FAQ机器人
        if self.robot:
            reply = self.robot.answer(content, 'simple_pos')
            if reply and reply != 'noanswer':
                return reply
        
        return None
    
    async def send_reply_to_wecom(self, user_id, content):
        """发送回复到企业微信"""
        return self.wecom_api.send_text_message(user_id, content)
    
    def update_session(self, session, user_msg, reply_msg):
        """更新会话记录"""
        session['messages'].append({
            'time': datetime.now().isoformat(),
            'role': 'user',
            'content': user_msg
        })
        session['messages'].append({
            'time': datetime.now().isoformat(),
            'role': 'robot',
            'content': reply_msg
        })
    
    async def transfer_to_agent(self, user_id, session):
        """转接到人工客服"""
        session['status'] = 'waiting'
        
        # 发送转接提示
        await self.send_reply_to_wecom(user_id, "正在为您转接人工客服，请稍候...")
        
        # 通过WebSocket请求分配客服
        try:
            async with websockets.connect(WEBSOCKET_CONFIG['url']) as websocket:
                client_chat_id = session['client_chat_id']
                
                # 登录
                login_msg = f"cmd@login;type@client;cont@{{'clientChatId':'{client_chat_id}','clientChatName':'企微_{user_id[-4:]}'}}"
                await websocket.send(login_msg)
                
                # 请求分配客服
                get_server_msg = f"cmd@getServerChatEnList;type@;cont@{{'clientChatId':'{client_chat_id}'}}"
                await websocket.send(get_server_msg)
                
                # 等待分配结果
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                
                if "serverChatId" in response:
                    # 解析客服信息
                    import re
                    server_id_match = re.search(r"'serverChatId':'([^']*)'", response)
                    server_name_match = re.search(r"'serverChatName':'([^']*)'", response)
                    
                    if server_id_match and server_name_match:
                        server_id = server_id_match.group(1)
                        server_name = server_name_match.group(1)
                        
                        session['server_chat_id'] = server_id
                        session['status'] = 'agent'
                        
                        await self.send_reply_to_wecom(
                            user_id,
                            f"已为您连接客服 {server_name}，请问有什么可以帮助您的？"
                        )
                        return True
                
                # 没有可用客服
                session['status'] = 'robot'
                await self.send_reply_to_wecom(
                    user_id,
                    "当前客服繁忙，请稍后再试或留言，我们会尽快回复您。"
                )
                return False
                
        except Exception as e:
            logger.error(f"转接人工失败: {e}")
            session['status'] = 'robot'
            await self.send_reply_to_wecom(user_id, AUTO_REPLY_RULES['default_reply'])
            return False
    
    async def forward_to_agent(self, user_id, content, session):
        """转发消息到人工客服"""
        if session['status'] != 'agent' or not session.get('server_chat_id'):
            # 还没有分配客服，先尝试分配
            success = await self.transfer_to_agent(user_id, session)
            if not success:
                return None
        
        # 转发消息到客服
        try:
            async with websockets.connect(WEBSOCKET_CONFIG['url']) as websocket:
                client_chat_id = session['client_chat_id']
                server_chat_id = session['server_chat_id']
                
                # 发送消息
                send_msg = f"cmd@sendMsg;type@client;cont@{{"
                send_msg += f"'serverChatId':'{server_chat_id}','clientChatId':'{client_chat_id}',"
                send_msg += f"'content':'{content}','contentType':'text',"
                send_msg += f"'role':'client','chatState':'client',"
                send_msg += f"'avatarUrl':'static/image/im_client_avatar.png',"
                send_msg += f"'source':'wecom','idcard':'','phone':'','uId':'','orderNo':''"
                send_msg += f"}}"
                
                await websocket.send(send_msg)
                
                # 更新会话
                self.update_session(session, content, "[已转发给客服]")
                
                return True
                
        except Exception as e:
            logger.error(f"转发消息失败: {e}")
            return False
    
    async def handle_agent_reply(self, client_chat_id, content):
        """处理客服回复（从WebSocket接收）"""
        # 从client_chat_id提取user_id
        if client_chat_id.startswith('wecom_'):
            user_id = client_chat_id[6:]  # 去掉'wecom_'前缀
            
            # 发送到企业微信
            await self.send_reply_to_wecom(user_id, content)
            
            # 更新会话
            if user_id in self.user_sessions:
                session = self.user_sessions[user_id]
                session['messages'].append({
                    'time': datetime.now().isoformat(),
                    'role': 'agent',
                    'content': content
                })
    
    def cleanup_sessions(self):
        """清理超时的会话"""
        now = datetime.now()
        timeout_seconds = AUTO_REPLY_RULES.get('timeout_seconds', 300)
        
        expired_users = []
        for user_id, session in self.user_sessions.items():
            if (now - session['last_active']).total_seconds() > timeout_seconds:
                expired_users.append(user_id)
        
        for user_id in expired_users:
            # 发送超时提醒
            asyncio.create_task(
                self.send_reply_to_wecom(
                    user_id,
                    AUTO_REPLY_RULES['timeout_message']
                )
            )
            # 删除会话
            del self.user_sessions[user_id]
            logger.info(f"清理超时会话: {user_id}")