# coding=utf-8
"""
企业微信API接口模块
"""
import requests
import json
import time
import logging
from wecom_config import WECOM_CONFIG

logger = logging.getLogger('wecom_api')

class WecomAPI:
    """企业微信API接口类"""
    
    def __init__(self):
        self.corp_id = WECOM_CONFIG['corp_id']
        self.agent_id = WECOM_CONFIG['agent_id']
        self.agent_secret = WECOM_CONFIG['agent_secret']
        self.kf_secret = WECOM_CONFIG['kf_secret']
        self.access_token = None
        self.kf_access_token = None
        self.token_expires_at = 0
        self.kf_token_expires_at = 0
        
    def get_access_token(self):
        """获取应用access_token"""
        if self.access_token and time.time() < self.token_expires_at:
            return self.access_token
        
        url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        params = {
            'corpid': self.corp_id,
            'corpsecret': self.agent_secret
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if data.get('errcode') == 0:
                self.access_token = data['access_token']
                # 提前5分钟过期
                self.token_expires_at = time.time() + data['expires_in'] - 300
                logger.info("获取access_token成功")
                return self.access_token
            else:
                logger.error(f"获取access_token失败: {data}")
                return None
        except Exception as e:
            logger.error(f"获取access_token异常: {e}")
            return None
    
    def get_kf_access_token(self):
        """获取客服access_token"""
        if self.kf_access_token and time.time() < self.kf_token_expires_at:
            return self.kf_access_token
        
        url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        params = {
            'corpid': self.corp_id,
            'corpsecret': self.kf_secret
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if data.get('errcode') == 0:
                self.kf_access_token = data['access_token']
                # 提前5分钟过期
                self.kf_token_expires_at = time.time() + data['expires_in'] - 300
                logger.info("获取客服access_token成功")
                return self.kf_access_token
            else:
                logger.error(f"获取客服access_token失败: {data}")
                return None
        except Exception as e:
            logger.error(f"获取客服access_token异常: {e}")
            return None
    
    def send_text_message(self, touser, content, kf_account=None):
        """发送文本消息给用户"""
        access_token = self.get_access_token()
        if not access_token:
            return False
        
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
        
        data = {
            "touser": touser,
            "msgtype": "text",
            "agentid": self.agent_id,
            "text": {
                "content": content
            }
        }
        
        if kf_account:
            data["kf_account"] = kf_account
        
        try:
            response = requests.post(url, json=data)
            result = response.json()
            
            if result.get('errcode') == 0:
                logger.info(f"发送消息成功: {touser}")
                return True
            else:
                logger.error(f"发送消息失败: {result}")
                return False
        except Exception as e:
            logger.error(f"发送消息异常: {e}")
            return False
    
    def send_kf_message(self, open_kfid, external_userid, msgtype, content):
        """发送客服消息"""
        access_token = self.get_kf_access_token()
        if not access_token:
            return False
        
        url = f"https://qyapi.weixin.qq.com/cgi-bin/kf/send_msg?access_token={access_token}"
        
        data = {
            "open_kfid": open_kfid,
            "external_userid": external_userid,
            "msgtype": msgtype
        }
        
        if msgtype == "text":
            data["text"] = {"content": content}
        elif msgtype == "image":
            data["image"] = {"media_id": content}
        elif msgtype == "file":
            data["file"] = {"media_id": content}
        
        try:
            response = requests.post(url, json=data)
            result = response.json()
            
            if result.get('errcode') == 0:
                logger.info(f"发送客服消息成功: {external_userid}")
                return True
            else:
                logger.error(f"发送客服消息失败: {result}")
                return False
        except Exception as e:
            logger.error(f"发送客服消息异常: {e}")
            return False
    
    def get_kf_account_list(self):
        """获取客服账号列表"""
        access_token = self.get_kf_access_token()
        if not access_token:
            return []
        
        url = f"https://qyapi.weixin.qq.com/cgi-bin/kf/account/list?access_token={access_token}"
        
        try:
            response = requests.get(url)
            result = response.json()
            
            if result.get('errcode') == 0:
                return result.get('account_list', [])
            else:
                logger.error(f"获取客服账号列表失败: {result}")
                return []
        except Exception as e:
            logger.error(f"获取客服账号列表异常: {e}")
            return []
    
    def add_kf_account(self, name, media_id):
        """添加客服账号"""
        access_token = self.get_kf_access_token()
        if not access_token:
            return None
        
        url = f"https://qyapi.weixin.qq.com/cgi-bin/kf/account/add?access_token={access_token}"
        
        data = {
            "name": name,
            "media_id": media_id
        }
        
        try:
            response = requests.post(url, json=data)
            result = response.json()
            
            if result.get('errcode') == 0:
                logger.info(f"添加客服账号成功: {name}")
                return result.get('open_kfid')
            else:
                logger.error(f"添加客服账号失败: {result}")
                return None
        except Exception as e:
            logger.error(f"添加客服账号异常: {e}")
            return None
    
    def get_external_contact(self, external_userid):
        """获取外部联系人详情"""
        access_token = self.get_access_token()
        if not access_token:
            return None
        
        url = f"https://qyapi.weixin.qq.com/cgi-bin/externalcontact/get?access_token={access_token}&external_userid={external_userid}"
        
        try:
            response = requests.get(url)
            result = response.json()
            
            if result.get('errcode') == 0:
                return result.get('external_contact')
            else:
                logger.error(f"获取外部联系人失败: {result}")
                return None
        except Exception as e:
            logger.error(f"获取外部联系人异常: {e}")
            return None