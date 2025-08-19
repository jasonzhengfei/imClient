# coding=utf-8
"""
企业微信消息加解密模块
"""
import base64
import hashlib
import time
import struct
import random
import string
from Crypto.Cipher import AES
import xml.etree.ElementTree as ET

class WXBizMsgCrypt:
    """企业微信消息加解密类"""
    
    def __init__(self, sToken, sEncodingAESKey, sCorpID):
        self.key = base64.b64decode(sEncodingAESKey + "=")
        self.token = sToken
        self.corpid = sCorpID
        # 设置加解密模式为AES的CBC模式
        self.mode = AES.MODE_CBC
    
    def VerifyURL(self, sMsgSignature, sTimeStamp, sNonce, sEchoStr):
        """验证URL有效性"""
        sha1 = hashlib.sha1()
        sha1.update(self._get_signature(self.token, sTimeStamp, sNonce, sEchoStr).encode())
        signature = sha1.hexdigest()
        
        if signature != sMsgSignature:
            return -40001, None  # 签名验证错误
        
        ret, sReplyEchoStr = self._decrypt(sEchoStr)
        return ret, sReplyEchoStr
    
    def DecryptMsg(self, sPostData, sMsgSignature, sTimeStamp, sNonce):
        """解密消息"""
        # 解析XML
        xml_tree = ET.fromstring(sPostData)
        encrypt = xml_tree.find("Encrypt").text
        
        # 验证签名
        sha1 = hashlib.sha1()
        sha1.update(self._get_signature(self.token, sTimeStamp, sNonce, encrypt).encode())
        signature = sha1.hexdigest()
        
        if signature != sMsgSignature:
            return -40001, None  # 签名验证错误
        
        # 解密
        ret, xml_content = self._decrypt(encrypt)
        return ret, xml_content
    
    def EncryptMsg(self, sReplyMsg, sNonce=None, sTimeStamp=None):
        """加密消息"""
        if not sNonce:
            sNonce = self._generate_nonce()
        if not sTimeStamp:
            sTimeStamp = str(int(time.time()))
        
        # 加密
        ret, encrypt = self._encrypt(sReplyMsg)
        if ret != 0:
            return ret, None
        
        # 生成签名
        sha1 = hashlib.sha1()
        sha1.update(self._get_signature(self.token, sTimeStamp, sNonce, encrypt).encode())
        signature = sha1.hexdigest()
        
        # 生成XML
        resp_xml = self._generate_xml(encrypt, signature, sTimeStamp, sNonce)
        return 0, resp_xml
    
    def _get_signature(self, token, timestamp, nonce, encrypt):
        """生成签名"""
        sortlist = [token, timestamp, nonce, encrypt]
        sortlist.sort()
        return ''.join(sortlist)
    
    def _encrypt(self, text):
        """对明文进行加密"""
        # 16位随机字符串
        text = self._get_random_str() + struct.pack("I", len(text.encode())).decode('latin-1') + \
               text + self.corpid
        
        # 补位
        text = self._pkcs7_encode(text)
        
        # 加密
        cryptor = AES.new(self.key, self.mode, self.key[:16])
        ciphertext = cryptor.encrypt(text.encode())
        
        # base64编码
        return 0, base64.b64encode(ciphertext).decode()
    
    def _decrypt(self, text):
        """对密文进行解密"""
        # base64解码
        text = base64.b64decode(text)
        
        # 解密
        cryptor = AES.new(self.key, self.mode, self.key[:16])
        plain_text = cryptor.decrypt(text).decode('latin-1')
        
        # 去除补位
        plain_text = self._pkcs7_decode(plain_text)
        
        # 去除16位随机字符串
        content = plain_text[16:]
        
        # 获取消息长度
        xml_len = struct.unpack("I", content[:4].encode('latin-1'))[0]
        
        # 获取消息内容
        xml_content = content[4:xml_len+4]
        
        # 获取企业ID
        from_corpid = content[xml_len+4:]
        
        if from_corpid != self.corpid:
            return -40008, None  # corpid校验错误
        
        return 0, xml_content
    
    def _get_random_str(self):
        """随机生成16位字符串"""
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))
    
    def _pkcs7_encode(self, text):
        """PKCS7补位"""
        text_length = len(text.encode())
        amount_to_pad = 32 - (text_length % 32)
        if amount_to_pad == 0:
            amount_to_pad = 32
        pad = chr(amount_to_pad)
        return text + pad * amount_to_pad
    
    def _pkcs7_decode(self, text):
        """删除PKCS7补位"""
        pad = ord(text[-1])
        if pad < 1 or pad > 32:
            pad = 0
        return text[:-pad]
    
    def _generate_nonce(self):
        """生成随机字符串"""
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
    
    def _generate_xml(self, encrypt, signature, timestamp, nonce):
        """生成xml消息"""
        resp_xml = """<xml>
<Encrypt><![CDATA[{encrypt}]]></Encrypt>
<MsgSignature><![CDATA[{signature}]]></MsgSignature>
<TimeStamp>{timestamp}</TimeStamp>
<Nonce><![CDATA[{nonce}]]></Nonce>
</xml>""".format(encrypt=encrypt, signature=signature, timestamp=timestamp, nonce=nonce)
        return resp_xml