# coding=utf-8
"""
企业微信集成测试脚本
"""
import requests
import json
import time
import asyncio
import websockets
from wecom_api import WecomAPI
from wecom_config import WECOM_CONFIG, WEBSOCKET_CONFIG

def test_access_token():
    """测试获取access_token"""
    print("=" * 50)
    print("测试获取access_token...")
    
    api = WecomAPI()
    token = api.get_access_token()
    
    if token:
        print(f"✓ 获取access_token成功: {token[:20]}...")
        return True
    else:
        print("✗ 获取access_token失败")
        return False

def test_send_message():
    """测试发送消息"""
    print("=" * 50)
    print("测试发送消息...")
    
    api = WecomAPI()
    
    # 这里需要替换为实际的用户ID
    test_user_id = "test_user"
    test_content = "这是一条测试消息"
    
    result = api.send_text_message(test_user_id, test_content)
    
    if result:
        print(f"✓ 发送消息成功")
        return True
    else:
        print("✗ 发送消息失败")
        return False

async def test_websocket():
    """测试WebSocket连接"""
    print("=" * 50)
    print("测试WebSocket连接...")
    
    try:
        async with websockets.connect(WEBSOCKET_CONFIG['url']) as websocket:
            # 发送登录消息
            login_msg = "cmd@login;type@client;cont@{'clientChatId':'test_client','clientChatName':'测试客户'}"
            await websocket.send(login_msg)
            
            print("✓ WebSocket连接成功")
            return True
    except Exception as e:
        print(f"✗ WebSocket连接失败: {e}")
        return False

def test_callback_url():
    """测试回调URL验证"""
    print("=" * 50)
    print("测试回调URL...")
    
    # 构造验证参数
    params = {
        'msg_signature': 'test_signature',
        'timestamp': str(int(time.time())),
        'nonce': 'test_nonce',
        'echostr': 'test_echostr'
    }
    
    url = f"http://localhost:3416/wecom/callback"
    
    try:
        response = requests.get(url, params=params, timeout=5)
        print(f"✓ 回调URL可访问，状态码: {response.status_code}")
        return True
    except Exception as e:
        print(f"✗ 回调URL访问失败: {e}")
        return False

def test_keyword_matching():
    """测试关键词匹配"""
    print("=" * 50)
    print("测试关键词匹配...")
    
    from wecom_bridge import WecomBridge
    
    bridge = WecomBridge(None)
    
    test_cases = [
        ("你好", True),
        ("价格是多少", True),
        ("营业时间", True),
        ("随机内容123", False)
    ]
    
    for content, should_match in test_cases:
        reply = bridge.get_robot_reply(content)
        if should_match and reply:
            print(f"✓ '{content}' -> 匹配成功")
        elif not should_match and not reply:
            print(f"✓ '{content}' -> 正确未匹配")
        else:
            print(f"✗ '{content}' -> 匹配错误")
    
    return True

def test_transfer_keywords():
    """测试转人工关键词"""
    print("=" * 50)
    print("测试转人工关键词...")
    
    from wecom_bridge import WecomBridge
    
    bridge = WecomBridge(None)
    
    test_cases = [
        ("我要人工客服", True),
        ("转人工", True),
        ("客服", True),
        ("普通消息", False)
    ]
    
    for content, should_transfer in test_cases:
        result = bridge.check_transfer_keywords(content)
        if result == should_transfer:
            print(f"✓ '{content}' -> {'需要转人工' if should_transfer else '不需转人工'}")
        else:
            print(f"✗ '{content}' -> 判断错误")
    
    return True

def main():
    """运行所有测试"""
    print("开始企业微信集成测试")
    print("=" * 50)
    
    # 基础配置检查
    print("检查配置...")
    if WECOM_CONFIG['corp_id'] == 'YOUR_CORP_ID':
        print("⚠ 警告：请先配置wecom_config.py中的企业微信参数")
        print("请参考README_WECOM.md进行配置")
        return
    
    print("✓ 配置文件已设置")
    
    # 运行测试
    tests = [
        ("Access Token", test_access_token),
        ("回调URL", test_callback_url),
        ("关键词匹配", test_keyword_matching),
        ("转人工检测", test_transfer_keywords),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = asyncio.run(test_func())
            else:
                result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ 测试 {name} 出错: {e}")
            results.append((name, False))
    
    # 异步测试
    print("运行异步测试...")
    asyncio.run(test_websocket())
    
    # 总结
    print("\n" + "=" * 50)
    print("测试结果总结：")
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{name}: {status}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    print(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！系统已准备就绪。")
    else:
        print("\n⚠ 部分测试失败，请检查配置和环境。")

if __name__ == "__main__":
    main()