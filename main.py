# coding=utf-8
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
import json
import datetime
import logging

words = []
serverChatDic = {}
clientChatDic = {}
clientChatEnList = []
serverChatEnList = []
from utils import (
    get_logger,
    similarity,
)

jieba.dt.tmp_dir = "./"
jieba.default_logger.setLevel(logging.ERROR)
logger = get_logger('faqrobot', logfile="faqrobot.log")

# db = pymysql.connect(host='192.168.0.39', port=3306, db='webcast', user='wx', password='KISaJx~6V)Vk',charset='utf8')
db = pymysql.connect(host='192.168.0.124',port=3306,db='webcast',user='root',password='ab_276@WQF')
# 使用cursor()方法获取操作游标
cursor = db.cursor()


class zhishiku(object):
    def __init__(self, q):  # a是答案（必须是1给）, q是问题（1个或多个）
        self.q = [q]
        self.a = ""
        self.sim = 0
        self.q_vec = []
        self.q_word = []

    def __str__(self):
        return 'q=' + str(self.q) + '\na=' + str(self.a) + '\nq_word=' + str(self.q_word) + '\nq_vec=' + str(self.q_vec)
        # return 'a=' + str(self.a) + '\nq=' + str(self.q)


class FAQrobot(object):
    def __init__(self, zhishitxt='0000', lastTxtLen=10, usedVec=False):
        # usedVec 如果是True 在初始化时会解析词向量，加快计算句子相似度的速度
        self.lastTxt = deque([], lastTxtLen)
        self.zhishitxt = zhishitxt
        self.usedVec = usedVec
        self.reload()
        self.loadWords()

    def loadWords(self):
        print('敏感词加载')
        sql = "SELECT content from minWords"
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                word = row[0]
                wordArr = word.split(',')
                for q in wordArr:
                    words.append(q)
        except:
            print("敏感词加载载入异常")
            # print(words)

    def load_qa(self):
        print('问答知识库开始载入')
        sql = "update user set chatStatus='0' "
        cursor.execute(sql)
        db.commit()
        self.zhishiku = []
        # SQL 查询语句
        sql = "SELECT * FROM  faq where projId=1"
        # sql="SELECT id,keywords,content FROM knContent"
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            # print(results)
            for row in results:
                answer = row[2]
                question = row[1]
                questions = question.split(';')
                i = 0
                for q in questions:
                    if i != 0:
                        self.zhishiku[-1].q.append(q)
                    else:
                        self.zhishiku.append(zhishiku(q))
                        self.zhishiku[-1].a += '\n' + answer
                        i = i + 1
        except:
            print("问答知识库载入异常")
        # db.close()
        # print(self.zhishiku)
        for t in self.zhishiku:
            for question in t.q:
                t.q_word.append(set(jieba.cut(question)))

    def load_embedding(self):
        from gensim.models import Word2Vec
        if not os.path.exists('Word60.model'):
            self.vecModel = None
            return

        # 载入60维的词向量(Word60.model，Word60.model.syn0.npy，Word60.model.syn1neg.npy）
        self.vecModel = Word2Vec.load('Word60.model')
        for t in self.zhishiku:
            t.q_vec = []
            for question in t.q_word:
                t.q_vec.append({t for t in question if t in self.vecModel.index2word})

    def reload(self):
        self.load_qa()
        self.load_embedding()

        print('问答知识库载入完毕')

    def maxSimTxt(self, intxt, simCondision=0.1, simType='simple'):
        self.lastTxt.append(intxt)
        if simType not in ('simple', 'simple_pos', 'vec'):
            return 'error:  maxSimTxt的simType类型不存在: {}'.format(simType)
        # 如果没有加载词向量，那么降级成 simple_pos 方法
        embedding = self.vecModel
        if simType == 'vec' and not embedding:
            simType = 'simple_pos'

        for t in self.zhishiku:
            questions = t.q_vec if simType == 'vec' else t.q_word
            in_vec = jieba.lcut(intxt) if simType == 'simple' else pseg.lcut(intxt)
            # print('in_vec')
            # print(in_vec)
            t.sim = max(
                similarity(in_vec, question, method=simType, embedding=embedding)
                for question in questions
            )
        maxSim = max(self.zhishiku, key=lambda x: x.sim)
        # logger.info('maxSim=' + format(maxSim.sim, '.0%'))

        if maxSim.sim < simCondision:
            # return '抱歉，我没有理解您的意思。'
            return 'noanswer'

        return maxSim.a

    def answer(self, intxt, simType='simple'):
        """simType=simple, simple_POS, vec, all"""
        if not intxt:
            return ''

        if simType == 'all':  # 用于测试不同类型方法的准确度，返回空文本
            for method in ('simple', 'simple_pos', 'vec'):
                outtext = 'method:\t' + self.maxSim(intxt, simType=method)
                print(outtext)
            return ''
        else:
            outtxt = self.maxSimTxt(intxt, simType=simType)
            # 输出回复内容，并计入日志
        return outtxt

    def sensitive(self, content):
        # print('sensitive')
        # print(words)
        for q in words:
            if content.find(q) >= 0:
                content = content.replace(q, "***")
        return content


class ConnectHandler(tornado.websocket.WebSocketHandler):
    async def test(self, sql):
        print("test sql:", sql)
        cursor.execute(sql)
        db.commit()

    async def querysql(self, sql):
        print("querysql sql:", sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        print("querysql result:", result)
        return result

    def check_origin(self, origin):
        '''重写同源检查 解决跨域问题'''
        return True

    def open(self):
        print('new websocket conn')
        '''新的websocket连接后被调动'''
        # self.write_message('Welcome')
        pass

    def on_close(self):
        '''websocket连接关闭后被调用'''
        print('onclose')
        logger.debug('onclose')
        # print("serverChatEnList")
        # print(serverChatEnList)
        # print("clientChatEnList")
        # print(clientChatEnList)
        print('clientChatDic = ', clientChatDic)
        try:
            if serverChatDic:
                print('s1')
                u = serverChatDic.values()
                if u:
                    print('u')
                    print(u)
                    v = -1
                    temp_list = list(u)
                    if self in temp_list:
                        v = temp_list.index(self)
                    print(v)
                    if v >= 0:
                        print('v')
                        key = list(serverChatDic.keys())[v]
                        print('key')
                        if key:
                            print('k1')
                            serverChatDic.pop(key)
                            print('k2')
                            print(serverChatEnList)
                            for se in serverChatEnList:
                                print('s2')
                                if se['serverChatId'] == key:
                                    print('s3')
                                    lastTime = str(datetime.datetime.now())
                                    # sql = "update user set chatLastTime='"+lastTime+"',chatStatus='0' where userSeatNo='"+se['serverChatName']+"'"
                                    # cursor.execute(sql)
                                    # db.commit()
                                    closeServerChatId = se['serverChatId']
                                    closeServerChatName = se['serverChatName']
                                    print(closeServerChatId)
                                    pcreateTime = str(datetime.datetime.now())
                                    for sec in clientChatEnList:
                                        cclientChatId = sec['serverChatId']
                                        if cclientChatId == closeServerChatId:
                                            pclientChatId = sec['clientChatId']
                                            msg1 = "{'cmd':'sendMsg','serverChatId':'" + closeServerChatId + "','clientChatId':'" + pclientChatId + "','avatarUrl':'" + "static/image/im_client_avatar.png" + "','content':'" + "坐席" + closeServerChatName + "已离线，自动断开" + "','fileUrl':'" + "" + "','contentType':'" + "text" + "','role':'" + "sys" + "','chatState':'" + "0" + "','createTime':'" + pcreateTime + "'}";
                                            print("msql")
                                            print(msg1)
                                            clientChatDic.get(pclientChatId).write_message(msg1)
                                    if serverChatEnList:
                                        serverChatEnList.remove(se)
                    else:
                        print('v null')
            else:
                print("serverChatDic null")
        except:
            print("serverChatDic error")
        try:
            if clientChatDic:
                print('1')
                u = clientChatDic.values()
                if u:
                    v = -1
                    temp_list = list(u)
                    if self in temp_list:
                        v = temp_list.index(self)
                    if v >= 0:
                        key = list(clientChatDic.keys())[v]
                        if key:
                            clientChatDic.pop(key)
                            for se in clientChatEnList:
                                if se['clientChatId'] == key:
                                    print('2')
                                    clientChatId = se['clientChatId']
                                    for i in range(0, len(serverChatEnList)):
                                        if serverChatEnList[i]['clientChatId'] == clientChatId:
                                            count = int(serverChatEnList[i]['count'])
                                            print('3')
                                            if count > 0:
                                                print('4')
                                                count = count - 1
                                                serverChatEnList[i]['count'] = count
                                                pcreateTime = str(datetime.datetime.now())
                                                # msgq = "{'cmd':'sendMsg','serverChatId':'" + serverChatId + "','clientChatId':'" + key + "','avatarUrl':'static/image/im_client_avatar.png','content':'客户已结束会话','fileUrl':' ','contentType':'text','role':'agent','chatState':'agent','createTime':'" + pcreateTime + "','idcard':' ','phone':' ','uId':' ','orderNo':' '}";
                                                # print(msgq)
                                                # serverChatDic.get(serverChatId).write_message(msgq)
                                                break
                                    clientChatEnList.remove(se)
            else:
                print("clientChatDic null")
        except:
            print("clientChatDic error")
        print("serverChatEnList2 = ", serverChatEnList)
        print("clientChatEnList2 = ", clientChatEnList)

    async def on_message(self, message):
        '''接收到客户端消息时被调用'''
        # response_text = robot.answer(message, 'vec')
        # self.write_message('new message :' + response_text)  # 向客服端发送
        ss = message.split(';')
        cmd = ss[0].split('@')[1]
        type = ss[1].split('@')[1]
        cont = ss[2].split('@')[1]
        cmd = cmd.strip()
        if cmd != 'herbert':
            print("收到message:", message)
            print("serverChatEnList:", serverChatEnList)
            print("clientChatEnList:", clientChatEnList)
        if cmd == 'login':
            loginSocket(self, type, cont)
        if cmd == 'agentDoClose':
            agentDoClose(cont)
        if cmd == 'setStatus':
            await setStatus(self, type, cont)
        if cmd == 'getServerChatEnList':
            await getServerChatEnList(self, cont)
        if cmd == 'selectServerChatId':
            await selectServerChatId(self, cont)
        if cmd == 'sendMsg':
            await sendMsg(self, type, cont)
        if cmd == 'sendBuss':
            sendBuss(cont)
        if cmd == 'getKnList':
            getKnList(self, cont)
        if cmd == 'getKnList10':
            getKnList10(self, cont)
        if cmd == 'serverQuit':
            await serverQuit(self, cont)
        if cmd == 'getTransferUserSeatList':
            getTransferUserSeatList(self)
        if cmd == 'transNewSeat':
            await transNewSeat(self, cont)


# 20250717 增加发送消息重试 失败时打印日志
def retry_operation(type, id, msg):
    max_retries: int = 5  # 最大重试次数
    for attempt in range(max_retries):
        try:
            if type == 'server':
                serverChatDic.get(id).write_message(msg)
                print("发送消息到服务端：", id, msg)
            if type == 'client':
                clientChatDic.get(id).write_message(msg)
                print("发送消息到客户端：", id, msg)
            break
        except Exception as e:
            print("发送消息失败: " + e)

def loginSocket(self, type, cont):
    print("login cont:", cont)
    if type.strip() == "agent":
        cont = cont.replace("'", '"')
        cont = cont.replace(";", ",")
        serverChatEn = json.loads(cont)
        if serverChatEn['serverChatName'] == 'undefined':
            print("undefined")
        else:
            if serverChatEn['serverChatId'] in serverChatDic:
                serverChatDic.pop(serverChatEn['serverChatId'])
            serverChatDic.update({serverChatEn['serverChatId']: self})
            for se in serverChatEnList:
                if se['serverChatId'] == serverChatEn['serverChatId']:
                    if serverChatEnList:
                        serverChatEnList.remove(se)
                elif se['serverChatName'] == serverChatEn['serverChatName']:
                    if serverChatEnList:
                        serverChatEnList.remove(se)
            serverChatEnList.append(serverChatEn)
    elif type.strip() == "client":
        cont = cont.replace("'", '"')
        ClientChatEn = json.loads(cont)
        if ClientChatEn['clientChatId'] in clientChatDic:
            clientChatDic.pop(ClientChatEn['clientChatId'])
        clientChatDic.update({ClientChatEn['clientChatId']: self})
        for cl in clientChatEnList:
            if cl['clientChatId'] == ClientChatEn['clientChatId'] or cl['clientChatName'] == ClientChatEn[
                'clientChatName']:
                if clientChatEnList:
                    clientChatEnList.remove(cl)
        clientChatEnList.append(ClientChatEn)

def agentDoClose(cont):
    print("agentDoClose cont:", cont)
    cont = cont.replace("'", '"')
    sendMsgInfo = json.loads(cont)
    closeServerChatId = str(sendMsgInfo['serverChatId'])
    pclientChatId = str(sendMsgInfo['clientChatId'])
    closeServerChatName = str(sendMsgInfo['serverChatName'])
    pcreateTime = str(datetime.datetime.now())
    msg1 = "{'cmd':'sendMsg','serverChatId':'" + closeServerChatId + "','clientChatId':'" + pclientChatId + "','avatarUrl':'" + "static/image/im_client_avatar.png" + "','content':'" + "坐席" + closeServerChatName + "已离线，自动断开" + "','fileUrl':'" + "" + "','contentType':'" + "text" + "','role':'" + "sys" + "','chatState':'" + "0" + "','createTime':'" + pcreateTime + "'}";
    retry_operation('client', pclientChatId, msg1)

async def setStatus(self, type, cont):
    print("setStatus cont:", cont)
    cont = cont.replace("'", '"')
    serverChatEn = json.loads(cont)
    for i in range(0, len(serverChatEnList)):
        if serverChatEnList[i]['serverChatId'] == serverChatEn['serverChatId']:
            serverChatEnList[i]['status'] = serverChatEn['status']
            lastTime = str(datetime.datetime.now())
            sql = "update user set chatLastTime='" + lastTime + "',chatStatus='" + serverChatEn[
                'status'] + "' where userSeatNo='" + serverChatEn['serverChatName'] + "'"
            await self.test(sql)
            break

async def getServerChatEnList(self, cont):
    print("getServerChatEnList cont:", cont)
    msg = ""
    cont = cont.replace("'", '"')
    clientChatEn = json.loads(cont)
    clientChatId = clientChatEn['clientChatId']
    serverChatName = ""
    # db = pymysql.connect(host='192.168.0.39', port=3306, db='webcast', user='wx', password='KISaJx~6V)Vk', charset='utf8')
    # cursor = db.cursor()
    sql = "select serverChatName from wechatTalk where clientChatId='" + clientChatId + "' and serverChatName<>'' order by id desc limit 1"
    results = await self.querysql(sql)
    for row in results:
        serverChatName = row[0]
        break
    count = 16
    k = -1
    if serverChatName == "":
        for i in range(0, len(serverChatEnList)):
            if serverChatEnList[i]['status'] == '1':
                count2 = int(serverChatEnList[i]['count'])
                if count2 < count:
                    count = count2
                    k = i
    else:
        for i in range(0, len(serverChatEnList)):
            if serverChatEnList[i]['serverChatName'] == serverChatName:
                if serverChatEnList[i]['status'] == '1':
                    count = int(serverChatEnList[i]['count'])
                    count2 = count
                    k = i
                    break
        if k == -1:
            for i in range(0, len(serverChatEnList)):
                if serverChatEnList[i]['status'] == '1':
                    count2 = int(serverChatEnList[i]['count'])
                    if count2 < count:
                        count = count2
                        k = i
    if count < 16 and k != -1:
        serverChatId = str(serverChatEnList[k]['serverChatId'])
        serverChatName = serverChatEnList[k]['serverChatName']
        avatarUrl = serverChatEnList[k]['avatarUrl']
        serverChatEnList[k]['count'] = count2 + 1
        msg = msg + "{'serverChatId':'" + serverChatId + "','serverChatName':'" + serverChatName + "','avatarUrl':'" + avatarUrl + "'}"
        for i in range(0, len(clientChatEnList)):
            if clientChatEnList[i]['clientChatId'] == clientChatId:
                clientChatEnList[i]['serverChatId'] = serverChatId
                break
    retry_operation('client', clientChatId, msg)

async def selectServerChatId(self, cont):
    print("selectServerChatId cont:", cont)
    # 客户端选择某坐席时，发相应的坐席发送消息，添加客户列表
    cont = cont.replace("'", '"')
    selectServerChatId = json.loads(cont)
    serverChatId = selectServerChatId['serverChatId']
    clientChatId = selectServerChatId['clientChatId']
    source = selectServerChatId['source']
    idcard = selectServerChatId['idcard']
    phone = selectServerChatId['phone']
    uId = selectServerChatId['uId']
    orderNo = selectServerChatId['orderNo']
    for i in range(0, len(serverChatEnList)):
        if serverChatEnList[i]['serverChatId'] == serverChatId:
            serverChatEnList[i]["source"] = source
            serverChatEnList[i]["idcard"] = idcard
            serverChatEnList[i]["phone"] = phone
            serverChatEnList[i]["uId"] = uId
            serverChatEnList[i]["orderNo"] = orderNo
            break
    if serverChatId in serverChatDic:
        for clentChatEn in clientChatEnList:
            if clentChatEn['clientChatId'] == clientChatId:
                msg0 = "{'cmd':'clientOn','clientChatId':'" + str(
                    clentChatEn['clientChatId']) + "','clientChatName':'" + clentChatEn[
                           'clientChatName'] + "','idcard':'" + idcard + "','phone':'" + phone + "','uId':'" + uId + "','orderNo':'" + orderNo + "','source':'" + source + "'}"
                pcreateTime = str(datetime.datetime.now())
                sql = "insert into wechatTalk(projName,sender,receiver,serverChatId,serverChatName,clientChatId,content,contentType,fileUrl,role,createTime,source,idcard,phone,uId,orderNo) values('rt','client','robot','" + serverChatId + "','" + "" + "','" + clientChatId + "','" + "customerSelect" + "','" + "text" + "','" + "" + "','" + "client" + "','" + pcreateTime + "','" + source + "','" + idcard + "','" + phone + "','" + uId + "','" + orderNo + "')"
                await self.test(sql)
                retry_operation('server', serverChatId, msg0)
                break

async def sendMsg(self, type, cont):
    cont = cont.replace("'", '"')
    sendMsgInfo = json.loads(cont)
    pserverChatId = str(sendMsgInfo['serverChatId'])
    pclientChatId = str(sendMsgInfo['clientChatId'])
    pcontent = sendMsgInfo['content']
    pcontent = robot.sensitive(pcontent)
    pcontentType = sendMsgInfo['contentType']
    pfileUrl = ""
    if pcontentType == "image" or pcontentType == "file":
        pfileUrl = sendMsgInfo['fileUrl']
    prole = sendMsgInfo['role']
    pcreateTime = str(datetime.datetime.now())
    pserverChatName = ""
    for serverChatEn in serverChatEnList:
        if serverChatEn['serverChatId'] == pserverChatId:
            pserverChatName = serverChatEn['serverChatName']
            break
    if type.strip() == "client":
        # 客户端向座席发送消息
        source = sendMsgInfo['source']
        idcard = sendMsgInfo['idcard']
        phone = sendMsgInfo['phone']
        uId = sendMsgInfo['uId']
        orderNo = sendMsgInfo['orderNo']
        sql = "insert into wechatTalk(projName,sender,receiver,serverChatId,serverChatName,clientChatId,content,contentType,fileUrl,role,createTime,source,idcard,phone,uId,orderNo) values('rt','client','agent','" + pserverChatId + "','" + pserverChatName + "','" + pclientChatId + "','" + pcontent + "','" + pcontentType + "','" + pfileUrl + "','" + prole + "','" + pcreateTime + "','" + source + "','" + idcard + "','" + phone + "','" + uId + "','" + orderNo + "')"
        await self.test(sql)
        if pserverChatId in serverChatDic:
            msg1 = "{'cmd':'sendMsg','serverChatId':'" + pserverChatId + "','clientChatId':'" + pclientChatId + "','avatarUrl':'" + \
                   sendMsgInfo[
                       'avatarUrl'] + "','content':'" + pcontent + "','fileUrl':'" + pfileUrl + "','contentType':'" + pcontentType + "','role':'" + prole + "','chatState':'" + \
                   sendMsgInfo[
                       'chatState'] + "','createTime':'" + pcreateTime + "','idcard':'" + idcard + "','phone':'" + phone + "','uId':'" + uId + "','orderNo':'" + orderNo + "'}";
            retry_operation('server', pserverChatId, msg1)
            source = sendMsgInfo['source']
    elif type.strip() == "agent":
        # 座席向客户端发送消息
        for i in range(0, len(serverChatEnList)):
            if serverChatEnList[i]['serverChatId'] == pserverChatId:
                source = sendMsgInfo['source']
                idcard = sendMsgInfo['idcard']
                phone = sendMsgInfo['phone']
                uId = sendMsgInfo['uId']
                orderNo = sendMsgInfo['orderNo']
                sql = "insert into wechatTalk(projName,sender,receiver,serverChatId,serverChatName,clientChatId,content,contentType,fileUrl,role,createTime,source,idcard,phone,uId,orderNo) values('rt','agent','client','" + pserverChatId + "','" + pserverChatName + "','" + pclientChatId + "','" + pcontent + "','" + pcontentType + "','" + pfileUrl + "','" + prole + "','" + pcreateTime + "','" + source + "','" + idcard + "','" + phone + "','" + uId + "','" + orderNo + "')"
                print(sql)
                await self.test(sql)
                break
        if pclientChatId in clientChatDic:
            msg1 = "{'cmd':'sendMsg','serverChatId':'" + pserverChatId + "','clientChatId':'" + pclientChatId + "','avatarUrl':'" + \
                   sendMsgInfo[
                       'avatarUrl'] + "','content':'" + pcontent + "','fileUrl':'" + pfileUrl + "','contentType':'" + pcontentType + "','role':'" + prole + "','chatState':'" + \
                   sendMsgInfo['chatState'] + "','createTime':'" + pcreateTime + "'}";
            retry_operation('client', pclientChatId, msg1)
    elif type.strip() == "robot":
        # 客户端向机器人发送消息
        ptype = "robot"
        source = sendMsgInfo['source']
        idcard = sendMsgInfo['idcard']
        phone = sendMsgInfo['phone']
        uId = sendMsgInfo['uId']
        orderNo = sendMsgInfo['orderNo']
        if pclientChatId in clientChatDic:
            pcontent = pcontent.replace(";", ",")
            # answerContent=(robot.answer(pcontent, 'simple_pos')).strip()
            answerContent = 'noanswer'
            if answerContent == 'noanswer':
                msg1 = "{'cmd':'sendMsg','serverChatId':'" + pserverChatId + "','clientChatId':'" + pclientChatId + "','avatarUrl':'" + \
                       sendMsgInfo[
                           'avatarUrl'] + "','content':'" + answerContent + "','fileUrl':'" + pfileUrl + "','contentType':'" + "transformServer2" + "','role':'" + prole + "','chatState':'" + \
                       sendMsgInfo['chatState'] + "','createTime':'" + pcreateTime + "'}";
            else:
                msg1 = "{'cmd':'sendMsg','serverChatId':'" + pserverChatId + "','clientChatId':'" + pclientChatId + "','avatarUrl':'" + \
                       sendMsgInfo[
                           'avatarUrl'] + "','content':'" + answerContent + "','fileUrl':'" + pfileUrl + "','contentType':'" + pcontentType + "','role':'" + prole + "','chatState':'" + \
                       sendMsgInfo['chatState'] + "','createTime':'" + pcreateTime + "'}";
            pcreateTime = str(datetime.datetime.now())
            retry_operation('client', pclientChatId, msg1)
            sql = "insert into wechatTalk(projName,sender,receiver,serverChatId,serverChatName,clientChatId,content,role,createTime,source,idcard,phone,uId,orderNo) values('rt','client','robot','" + pserverChatId + "','" + pserverChatName + "','" + pclientChatId + "','" + pcontent + "','" + ptype + "','" + pcreateTime + "','" + source + "','" + idcard + "','" + phone + "','" + uId + "','" + orderNo + "')"
            await self.test(sql)
            sql = "insert into wechatTalk(projName,sender,receiver,serverChatId,serverChatName,clientChatId,content,role,createTime,source,idcard,phone,uId,orderNo) values('rt','robot','client','" + pserverChatId + "','" + pserverChatName + "','" + pclientChatId + "','" + answerContent + "','" + "client" + "','" + pcreateTime + "','" + source + "','" + idcard + "','" + phone + "','" + uId + "','" + orderNo + "')"
            await self.test(sql)

def sendBuss(self, cont):
    chatId = ""
    cont = cont.replace("'", '"')
    sendMsgInfo = json.loads(cont)
    pserverChatId = str(sendMsgInfo['serverChatId'])
    pclientChatId = str(sendMsgInfo['clientChatId'])
    pcontent = sendMsgInfo['content']
    source = sendMsgInfo['source']
    idcard = sendMsgInfo['idcard']
    phone = sendMsgInfo['phone']
    uId = sendMsgInfo['uId']
    orderNo = sendMsgInfo['orderNo']
    pfileUrl = ""
    prole = ""
    chatState = ""
    pcreateTime = str(datetime.datetime.now())
    if pcontent == "1":
        print("打款凭证反馈")
        k = -1
        for i in range(0, len(serverChatEnList)):
            if serverChatEnList[i]['status'] == '1' and serverChatEnList[i]['serverChatName'] == '7002':
                k = i
                serverChatIds = serverChatEnList[i]['serverChatId']
                break
        if k == -1:
            rcontent = "客户您好，如果您已经通过皖新租赁公户完成转账，请在此处反馈客户姓名、签约手机号、转账人姓名以及转账截图，并且签约的还款账户不要留有余额，避免重复扣款，感谢您的配合！"
            msg1 = "{'cmd':'sendMsg','serverChatId':'" + pserverChatId + "','clientChatId':'" + pclientChatId + "','avatarUrl':'" + \
                   sendMsgInfo[
                       'avatarUrl'] + "','content':'" + rcontent + "','fileUrl':'" + pfileUrl + "','contentType':'" + "text" + "','role':'" + prole + "','chatState':'" + chatState + "','createTime':'" + pcreateTime + "'}";
            retry_operation('client', pclientChatId, msg1)
            # clientChatDic.get(pclientChatId).write_message(msg1)
        else:
            if chatId in serverChatDic:
                for clentChatEn in clientChatEnList:
                    if clentChatEn['clientChatId'] == pclientChatId:
                        msg0 = "{'cmd':'clientOn','clientChatId':'" + str(
                            clentChatEn['clientChatId']) + "','clientChatName':'" + clentChatEn[
                                   'clientChatName'] + "','idcard':'" + idcard + "','phone':'" + phone + "','uId':'" + uId + "','orderNo':'" + orderNo + "','source':'" + source + "'}"
                        serverChatDic.get(chatId).write_message(msg0)
                        count2 = int(serverChatEnList[i]['count'])
                        serverChatId = str(serverChatEnList[k]['serverChatId'])
                        serverChatName = serverChatEnList[k]['serverChatName']
                        avatarUrl = serverChatEnList[k]['avatarUrl']
                        serverChatEnList[k]['count'] = count2 + 1
                        msg = "{'serverChatId':'" + serverChatId + "','serverChatName':'" + serverChatName + "','avatarUrl':'" + avatarUrl + "'}"
                        for i in range(0, len(clientChatEnList)):
                            if clientChatEnList[i]['clientChatId'] == pclientChatId:
                                clientChatEnList[i]['serverChatId'] = serverChatId
                                break
                        self.write_message(msg)
                        break
    elif pcontent == "2":
        print("业务办理")
        k = -1
        for i in range(0, len(serverChatEnList)):
            if serverChatEnList[i]['status'] == '1' and serverChatEnList[i]['serverChatName'] == '2001':
                k = i
                serverChatIds = serverChatEnList[i]['serverChatId']
                break
        if k == -1:
            msg1 = ""
            retry_operation('client', pclientChatId, msg1)
            # clientChatDic.get(pclientChatId).write_message(msg1)
        else:
            if chatId in serverChatDic:
                for clentChatEn in clientChatEnList:
                    if clentChatEn['clientChatId'] == pclientChatId:
                        msg0 = "{'cmd':'clientOn','clientChatId':'" + str(
                            clentChatEn['clientChatId']) + "','clientChatName':'" + clentChatEn[
                                   'clientChatName'] + "','idcard':'" + idcard + "','phone':'" + phone + "','uId':'" + uId + "','orderNo':'" + orderNo + "','source':'" + source + "'}"
                        retry_operation('server', chatId, msg0)
                        # serverChatDic.get(serverChatIds).write_message(msg0)
                        count2 = int(serverChatEnList[i]['count'])
                        serverChatId = str(serverChatEnList[k]['serverChatId'])
                        serverChatName = serverChatEnList[k]['serverChatName']
                        avatarUrl = serverChatEnList[k]['avatarUrl']
                        serverChatEnList[k]['count'] = count2 + 1
                        msg = "{'serverChatId':'" + serverChatId + "','serverChatName':'" + serverChatName + "','avatarUrl':'" + avatarUrl + "'}"
                        for i in range(0, len(clientChatEnList)):
                            if clientChatEnList[i]['clientChatId'] == pclientChatId:
                                clientChatEnList[i]['serverChatId'] = serverChatId
                                break
                        self.write_message(msg)
                        break
    elif pcontent == "3":
        print("修改还款卡")
        k = -1
        print(serverChatEnList)
        for i in range(0, len(serverChatEnList)):
            if serverChatEnList[i]['status'] == '1' and serverChatEnList[i]['serverChatName'] == '2001':
                k = i
                serverChatIds = serverChatEnList[i]['serverChatId']
                break
        if k == -1:
            rcontent = "客户您好，还款卡仅支持中行，农行，工商，建行，邮储五家银行卡。<br>"
            rcontent = rcontent + "改卡请留言提供以下材料：<br>"
            rcontent = rcontent + "1.您的姓名、签约手机号<br>"
            rcontent = rcontent + "2.更换新卡的卡号，所对应的银行和银行签约手机号<br>"
            rcontent = rcontent + "在线客服会根据您预留的信息电话联系您办理业务，请您注意来电信息"
            msg1 = "{'cmd':'sendMsg','serverChatId':'" + pserverChatId + "','clientChatId':'" + pclientChatId + "','avatarUrl':'" + \
                   sendMsgInfo[
                       'avatarUrl'] + "','content':'" + rcontent + "','fileUrl':'" + pfileUrl + "','contentType':'" + "text" + "','role':'" + prole + "','chatState':'" + chatState + "','createTime':'" + pcreateTime + "'}";
            retry_operation('client', pclientChatId, msg1)
            # clientChatDic.get(pclientChatId).write_message(msg1)
        else:
            if chatId in serverChatDic:
                for clentChatEn in clientChatEnList:
                    if clentChatEn['clientChatId'] == pclientChatId:
                        msg0 = "{'cmd':'clientOn','clientChatId':'" + str(
                            clentChatEn['clientChatId']) + "','clientChatName':'" + clentChatEn[
                                   'clientChatName'] + "','idcard':'" + idcard + "','phone':'" + phone + "','uId':'" + uId + "','orderNo':'" + orderNo + "','source':'" + source + "'}"
                        retry_operation('server', chatId, msg0)
                        # serverChatDic.get(serverChatIds).write_message(msg0)
                        count2 = int(serverChatEnList[i]['count'])
                        serverChatId = str(serverChatEnList[k]['serverChatId'])
                        serverChatName = serverChatEnList[k]['serverChatName']
                        avatarUrl = serverChatEnList[k]['avatarUrl']
                        serverChatEnList[k]['count'] = count2 + 1
                        msg = "{'serverChatId':'" + serverChatId + "','serverChatName':'" + serverChatName + "','avatarUrl':'" + avatarUrl + "'}"
                        for i in range(0, len(clientChatEnList)):
                            if clientChatEnList[i]['clientChatId'] == pclientChatId:
                                clientChatEnList[i]['serverChatId'] = serverChatId
                                break
                        self.write_message(msg)
                        break
    elif pcontent == "4":
        print("异议反馈")
        k = -1
        for i in range(0, len(serverChatEnList)):
            if serverChatEnList[i]['status'] == '1' and serverChatEnList[i]['serverChatName'] == '2001':
                k = i
                serverChatIds = serverChatEnList[i]['serverChatId']
                break
        if k == -1:
            msg1 = ""
            retry_operation('client', pclientChatId, msg1)
            # clientChatDic.get(pclientChatId).write_message(msg1)
        else:
            if chatId in serverChatDic:
                for clentChatEn in clientChatEnList:
                    if clentChatEn['clientChatId'] == pclientChatId:
                        msg0 = "{'cmd':'clientOn','clientChatId':'" + str(
                            clentChatEn['clientChatId']) + "','clientChatName':'" + clentChatEn[
                                   'clientChatName'] + "','idcard':'" + idcard + "','phone':'" + phone + "','uId':'" + uId + "','orderNo':'" + orderNo + "','source':'" + source + "'}"
                        retry_operation('server', chatId, msg0)
                        # serverChatDic.get(serverChatIds).write_message(msg0)
                        count2 = int(serverChatEnList[i]['count'])
                        serverChatId = str(serverChatEnList[k]['serverChatId'])
                        serverChatName = serverChatEnList[k]['serverChatName']
                        avatarUrl = serverChatEnList[k]['avatarUrl']
                        serverChatEnList[k]['count'] = count2 + 1
                        msg = "{'serverChatId':'" + serverChatId + "','serverChatName':'" + serverChatName + "','avatarUrl':'" + avatarUrl + "'}"
                        for i in range(0, len(clientChatEnList)):
                            if clientChatEnList[i]['clientChatId'] == pclientChatId:
                                clientChatEnList[i]['serverChatId'] = serverChatId
                                break
                        self.write_message(msg)
                        break

def getKnList(self, cont):
    cont = cont.replace("'", '"')
    knowledge = json.loads(cont)
    keywords = knowledge['keywords']
    cursor = db.cursor()
    sql = "SELECT content FROM knContent where keywords like '%%%s%%'" % keywords
    # sql="SELECT id,keywords,content FROM knContent"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        print(results)
        msg = ""
        for row in results:
            content = row[0]
            msg = msg + "{'content':'" + content + "','MoreKnList':'" + "" + "'" + "}@"
            print(msg)
        msg = msg[0:len(msg) - 1]
        self.write_message(msg)
    except:
        print("Error000: unable to fecth data")

def getKnList10(self, cont):
    cont = cont.replace("'", '"')
    knowledge = json.loads(cont)
    print(knowledge)
    cursor = db.cursor()
    keywords = knowledge['keywords']
    sql = "SELECT content FROM knContent where keywords like '%%%s%%'" % keywords + " limit 10"
    # sql="SELECT id,keywords,content FROM knContent"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        print(results)
        msg = ""
        for row in results:
            content = row[0]
            msg = msg + "{'content':'" + content + "','MoreKnList':'" + "" + "'" + "}@"
            print(msg)
        msg = msg[0:len(msg) - 1]
        self.write_message(msg)
    except:
        print("Error000: unable to fecth data")

async def serverQuit(self, cont):
    cont = cont.replace("'", '"')
    userSeatNoS = json.loads(cont)
    userSeatNo = userSeatNoS['userSeatNo']
    print(userSeatNo)
    for se in serverChatEnList:
        if se['serverChatName'] == userSeatNo:
            lastTime = str(datetime.datetime.now())
            sql = "update user set chatLastTime='" + lastTime + "',chatStatus='0' where userSeatNo='" + se[
                'serverChatName'] + "'"
            await self.test(sql)
            serverChatEnList.remove(se)
    print(serverChatEnList)
    # db.close()

def getTransferUserSeatList(self):
    msg = ""
    for k in range(0, len(serverChatEnList)):
        serverChatId = str(serverChatEnList[k]['serverChatId'])
        serverChatName = serverChatEnList[k]['serverChatName']
        avatarUrl = serverChatEnList[k]['avatarUrl']
        status = serverChatEnList[k]['status']
        if status == 1 or status == "1":
            msg = msg + "{'TransferUserSeatList':'1','serverChatId':'" + serverChatId + "','serverChatName':'" + serverChatName + "','avatarUrl':'" + avatarUrl + "'}@"
    print(msg)
    msg = msg[0:len(msg) - 1]
    self.write_message(msg)

async def transNewSeat(self, cont):
    cont = cont.replace("'", '"')
    transChatEn = json.loads(cont)
    print("transChatEn--")
    print(transChatEn)
    serverChatId = str(transChatEn['serverChatId'])  # 原坐席
    oldserverChatId = serverChatId
    clientChatId = str(transChatEn['clientChatId'])  # 客户
    transServerChatId = str(transChatEn['transServerChatId'])  # 转接到坐席
    serverChatName = str(transChatEn['serverChatName'])  # 转接到坐席名
    avatarUrl = str(transChatEn['avatarUrl'])
    source = str(transChatEn['source'])  # 来源
    idcard = str(transChatEn['idcard'])
    phone = str(transChatEn['phone'])
    uId = str(transChatEn['uId'])
    orderNo = str(transChatEn['orderNo'])
    # 回复给客户消息
    msg = "{'serverChatId':'" + transServerChatId + "','serverChatName':'" + serverChatName + "','avatarUrl':'" + avatarUrl + "'}"
    print("msg--:")
    print(msg)
    retry_operation('client', clientChatId, msg)
    # clientChatDic.get(clientChatId).write_message(msg)

    # 向转接坐席发送消息，添加客户列表s
    serverChatId = transServerChatId
    for i in range(0, len(serverChatEnList)):
        if serverChatEnList[i]['serverChatId'] == serverChatId:
            serverChatEnList[i]["source"] = source
            serverChatEnList[i]["idcard"] = idcard
            serverChatEnList[i]["phone"] = phone
            serverChatEnList[i]["uId"] = uId
            serverChatEnList[i]["orderNo"] = orderNo
            break
    print(clientChatEnList)
    if serverChatId in serverChatDic:
        for clentChatEn in clientChatEnList:
            if clentChatEn['clientChatId'] == clientChatId:
                print("cID" + clientChatId)
                msg0 = "{'cmd':'clientOn','clientChatId':'" + str(
                    clentChatEn['clientChatId']) + "','clientChatName':'" + clentChatEn[
                           'clientChatName'] + "','source':'" + source + "','idcard':'" + idcard + "','phone':'" + phone + "','uId':'" + "','orderNo':'" + "'}"
                pcreateTime = str(datetime.datetime.now())
                print("msg0" + msg0)
                sql = "insert into wechatTalk(projName,sender,receiver,serverChatId,serverChatName,clientChatId,content,contentType,fileUrl,role,createTime,source,idcard,phone,uId,orderNo) values('rt','client','robot','" + serverChatId + "','" + "" + "','" + clientChatId + "','" + "customerSelect" + "','" + "text" + "','" + "" + "','" + "client" + "','" + pcreateTime + "','" + source + "','" + idcard + "','" + phone + "','" + uId + "','" + orderNo + "')"
                await self.test(sql)
                retry_operation('server', serverChatId, msg0)
                # serverChatDic.get(serverChatId).write_message(msg0)
                break
                # 向转接坐席发送消息，添加客户列表e

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        content = self.get_query_argument('content')
        answer = (robot.answer(content, 'simple_pos')).strip()
        self.write("answer:" + answer)
        pass

    def post(self):
        json_data = self.request.body
        print(json_data)
        if json_data:
            data = json.loads(json_data)
            content = data['content']
            answer = (robot.answer(content, 'simple_pos')).strip()
            self.write("answer:" + answer)
        pass


class RefreshHandler(tornado.web.RequestHandler):
    def get(self):
        robot.reload()
        pass

    def post(self):
        robot.reload()
        pass


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/index', MainHandler),
            (r'/ws', ConnectHandler),
            (r'/refresh', RefreshHandler),
        ]
        tornado.web.Application.__init__(self, handlers)


if __name__ == "__main__":
    robot = FAQrobot('0000', usedVec=False)
    app = Application()
    app.listen(3416)
    tornado.ioloop.IOLoop.current().start()