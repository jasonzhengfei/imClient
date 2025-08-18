<!-- im客户端 入口 -->
<template>
  <div class="imClient-wrapper">
    <div class="imClient-inner" :style="{ width: imClientinnerWidth }">
      <header class="imClient-header">
        <div class="name-wrapper position-v-mid">
          <span v-if="chatInfoEn.chatState == 'robot'">在线客服</span>
          <span v-else-if="chatInfoEn.chatState == 'agent'">您正在与客服{{ serverChatEn.serverChatName }}对话</span>
        </div>
        <div class="opr-wrapper position-v-mid">
          <!-- <el-tooltip content="评分" placement="bottom" effect="light">
                        <i class="fa fa-star-half-full" @click="showRateDialog()"></i>
                    </el-tooltip>
                    <el-tooltip content="留言" placement="bottom" effect="light">
                        <i class="fa fa-envelope-o" @click="showLeaveDialog()"></i>
                    </el-tooltip> -->
          <el-tooltip content="结束会话" placement="bottom" effect="light">
            <span id="userInfoSpan" style="display:none">{{ userInfo }}</span>
            <span style="display:none" @click="closeChat()"> 结束会话</span>
          </el-tooltip>
          <el-tooltip style="display:none" content="退出" placement="bottom" effect="light">
            <i style="display:none" class="fa fa-close" @click="closewin2()"></i>
          </el-tooltip>

          <!-- <span @click="closeChat()" style="float:right">X</span> -->
        </div>
        <!-- <div class="opr-wrapper position-v-mid">
                    <el-tooltip content="评分" placement="bottom" effect="light">
                        <i class="fa fa-star-half-full" @click="showRateDialog()"></i>
                    </el-tooltip>
                    <el-tooltip content="留言" placement="bottom" effect="light">
                        <i class="fa fa-envelope-o" @click="showLeaveDialog()"></i>
                    </el-tooltip>
                    <el-tooltip content="结束会话" placement="bottom" effect="light">
                        <i class="fa fa-close" @click="closeChat()"></i>
                    </el-tooltip>
                </div> -->
      </header>
      <main class="imClient-main">
        <!-- 聊天框 -->
        <div class="item imClientChat-wrapper" :style="{ width: imClientChatWrapperWidth }">
          <!-- 聊天记录 -->
          <common-chat ref="common_chat" :chatInfoEn="chatInfoEn" :oprRoleName="'client'" @submitSolve="submitSolve"
            @sendBuss="sendBuss" @sendMsg="sendMsg" @chatCallback="chatCallback" @addChatMsg="addChatMsg"
            @refreshFAQ="refreshFAQ" @changeCurTime="changeCurTime" @clientQuit="clientQuit"
            :projId="projId"></common-chat>
        </div>
        <!-- 信息区域 -->
        <!-- <div class="item imClientInfo-wrapper"> -->
        <!--  <article class="imClientInfo-notice-wrapper">
                        <header class="imClientInfo-item-header">
                            公告
                        </header>
                        <main class="imClientInfo-notice-main">
                            <p class="link">
                                </p>
                            <p class="link"></p>
                        </main>
                    </article>  -->

        <!-- <article class="imClientInfo-faq-wrapper">
                        <header class="imClientInfo-item-header">
                            常见问题
                        </header>
                        <main class="imClientInfo-faq-main">
                        <el-collapse v-model="activeNames" >
                            <el-collapse-item v-for="(item, index) in list" :title="item.keywords" :name="index" :key="index">
                                <div>{{item.content}}</div>
                            </el-collapse-item>
                        </el-collapse>
                        </main>
                    </article> -->
        <!-- </div>  -->
      </main>
    </div>
    <!-- 转接客服dialog -->
    <el-dialog title="请选择客服" :visible.sync="transferDialogVisible" :close-on-press-escape="false">
      <im-transfer ref="im_transfer" @submit="transferDialog_submit"></im-transfer>
    </el-dialog>
    <!-- 满意度dialog -->
    <el-dialog :visible.sync="rateDialogVisible" :close-on-press-escape="false" width="80%" style="height: 400px">
      <!-- <im-rate ref="im_rate"></im-rate> -->
      <div class="imRate-wrapper">
        <div v-show="!resultVisible" class="main">
          <p class="title">请对客服的进行评价</p>
          <el-row>
            <el-rate v-model="dataForm.score" show-text :texts="['非常不满意', '不满意', '一般', '满意', '非常满意']">
            </el-rate>
          </el-row>
          <el-row>
            <el-input type="textarea" :maxlength="50" :rows="4" resize="none" placeholder="备注(选填，50字符以内)"
              v-model="dataForm.remark"></el-input>
          </el-row>
          <el-button type="primary" class="submit-btn position-h-mid" @click="submit"
            :disabled="dataForm.score == null">确定</el-button>
        </div>
        <!-- 评价后的界面 -->
        <div v-show="resultVisible" class="submit-main">
          <i class="fa fa-check-circle-o"></i>
          <p class="title">评价提交成功</p>
        </div>
      </div>
    </el-dialog>
    <!-- 离线留言dialog -->
    <el-dialog :visible.sync="leaveDialogVisible" :close-on-press-escape="false">
      <im-leave ref="im_leave"></im-leave>
    </el-dialog>
    <!-- 结束会话dialog -->
    <el-dialog :visible.sync="logoutDialogVisible" :close-on-press-escape="false">
      <p class="title">结束本次会话？</p>
      <div class="footer">
        <el-button type="primary" @click="logoutDialog_cancel">取消</el-button>
        <el-button type="primary" @click="logoutDialog_submit">结束会话</el-button>
      </div>
    </el-dialog>
    <!-- 问题是否解决  -->
    <el-dialog :visible.sync="isSolveDialogVisible" :close-on-press-escape="false" width="70%" style="height: 300px">
      <span style="
          font-size: 16px;
          margin-top: 30px;
          margin-bottom: 30px;
          margin-left: 5px;
        ">问题是否解决</span>
      <el-radio style="font-size: 24px" v-model="isSolve" label="1">是</el-radio>
      <el-radio style="font-size: 24px" v-model="isSolve" label="2">否
      </el-radio>
      <div style="margin-top: 30px"></div>
      <el-button type="primary" class="submit-btn position-h-mid" @click="submitIsSolve">确定</el-button>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'
import $ from 'jquery'
var ws = null;
var us = 'tct';
const CryptoJS = require("crypto-js");
import commonChat from '@/components/common/common_chat.vue';
import imRate from './imRate.vue';
import imLeave from './imLeave.vue';
import imTransfer from './imTransfer.vue';
var ws = null;
export default {
  components: {
    commonChat: commonChat,
    imRate: imRate,
    imLeave: imLeave,
    imTransfer: imTransfer,
  },
  data() {
    return {
      userInfo: "",
      userType: "",
      source: "",
      idcard: "",
      phone: "",
      orderNo: "",
      uId: "",
      projId: '',
      converEnd: false,
      chatFlag: false, //转人工
      isSolve: '1',
      isSolveDialogVisible: false,
      firtFlag: true,
      timer: '',
      currTime: '',
      openTimer: null,
      rateDialogVisible: false,
      resultVisible: false, // 满意度已提交
      dataForm: {
        score: null, // 选中的item
        remark: '',
      },
      activeNames: ['1'],
      list: [
        // {keywords:'11',content:'1111'},
        // {keywords:'22',content:'2222'},
        // {keywords:'33',content:'3333'},
      ],
      chatInfoEn: {
        chatState: 'robot', // chat状态；robot 机器人、agent 客服
        inputContent: '', // 输入框内容
        msgList: [], // 消息列表
        state: 'on', // 连接状态;on ：在线；off：离线
        lastMsgShowTime: null, // 最后一个消息的显示时间
      }, // 会话信息，包括聊天记录、状态
      clientChatEn: {
        clientChatId: '',
        clientChatName: '',
        avatarUrl: 'static/image/im_client_avatar.png',
      }, // 当前账号的信息
      serverChatEn: {
        serverChatId: '',
        serverChatName: '',
        avatarUrl: '',
        source: '',
      }, // 服务端chat信息
      robotEn: {
        robotName: '小旺',
        avatarUrl: 'static/image/im_robot_avatar.png',
      }, // 机器人信息
      faqList: [
        { title: '今天周几', content: '今天周一' },
        { title: '今天周几', content: '今天周二' },
        { title: '今天周几', content: '今天周三' },
        { title: '今天周几', content: '今天周四' },
        { title: '今天周几', content: '今天周五' },
      ],
      msgFlag: false,
      time: '',
      faqSelected: '-1',
      inputContent_setTimeout: null, // 输入文字时在输入结束才修改具体内容
      selectionRange: null, // 输入框选中的区域
      shortcutMsgList: [], // 聊天区域的快捷回复列表
      logoutDialogVisible: false, // 结束会话显示
      transferDialogVisible: false, // 转接人工dialog
      rateDialogVisible: false, // 评价dialog
      leaveDialogVisible: false, // 留言dialog
      imClientChatWrapperWidth: '550px',
      imClientinnerWidth: '850px',
      //
      lockReconnect: false, //是否真正建立连接
      timeout: 28 * 1000, //30秒一次心跳
      timeoutObj: null, //心跳心跳倒计时
      serverTimeoutObj: null, //心跳倒计时
      timeoutnum: null, //断开 重连倒计时
      herBertTimer: null,
      sendIntervalTimer: '', //发送计时器
      sendCurTime: '', //发送当前时间
      backFlag: false,
    };
  },

  computed: {},
  watch: {},
  methods: {
    refreshFAQ() {
      var msg = "cmd@refreshFAQ;type@client;cont@{'refreshFAQ'}";
      ws.send(msg);
    },
    submitIsSolve() {
      var formData = {
        isSolve: this.isSolve,
        clientChatId: this.$data.clientChatEn.clientChatId,
      };
      this.$http.post({
        // url: 'http://180.168.223.243:19001/api/WebChat/addIsSolve',
        url: '/backend2/api/WebChat/addIsSolve',
        params: formData,
        successCallback: (rs) => {
          console.log('rss');
          console.log(rs);
        },
      });

      this.isSolveDialogVisible = false;
    },
    submitSolve: function (rs) {
      var formData = {
        isSolve: rs.isSolve,
        clientChatEn: this.$data.clientChatEn.clientChatId,
      };
      this.$http.post({
        // url: 'http://180.168.223.243:19001/api/WebChat/addIsSolve',
        //  url: 'http://192.168.3.20:9099/api/WebChat/addIsSolve',
        url: '/backend2/api/WebChat/addIsSolve',
        params: formData,
        successCallback: (rs) => {
          console.log('rss');
          console.log(rs);
        },
      });

      this.$router.go(-1);
    },
    msgInterval() {

      var that = this;

      this.timer = setInterval(() => {
        var d = that.getNow();
        var t = that.timeDifference(that.currTime, d);
        if (t >= 300 && that.msgFlag == true) {
          if (that.chatFlag == false) {
            if (that.firtFlag == true) {
              that.addChatMsg({
                role: 'sys',
                contentType: 'text',
                content:
                  '您好，由于您超出5分钟没有回复，会话结束，请您退出后重新进入在线客服。',
              });
              that.clientQuit();
              that.rateDialogVisible = false;
              that.isSolveDialogVisible = false;
              that.firtFlag = false;
            }
          } else {
            if (that.firtFlag == true) {
              //转人工，提示满意度评价
              that.rateDialogVisible = false;
              that.firtFlag = false;
              that.addChatMsg({
                role: 'sys',
                contentType: 'text',
                content: '您好，由于您超出5分钟没有回复，会话结束了，请您退出后重新进入在线客服。',
              });
              that.clientQuit();
            }
          }
          that.converEnd = true;
        }
      }, 1000);
    },
    sendInterval() {
      var that = this;
      that.sendIntervalTimer = setInterval(() => {
        if (that.backFlag == true) {
        } else {
          var d = that.getNow();
          var t = that.timeDifference(that.sendCurTime, d);
          if (t > 60) {
            console.log('>60');
            that.addChatMsg({
              role: 'sys',
              contentType: 'text',
              content: '很抱歉，客服正在加急处理您的消息中，请稍后...',
            });
            that.sendCurTime = that.getNow();
          } else {
            console.log(t, 't');
          }
        }
      }, 1000);
    },
    changeCurTime() {
      this.timer = null;
      this.msgFlag = false;
      clearInterval(this.timer);
      if (this.chatFlag == true) {
        this.backFlag = false;
        this.sendIntervalTimer = null;
        clearInterval(this.sendIntervalTimer);
        this.sendCurTime = this.getNow();
        this.sendInterval();
      }
    },
    getNow() {
      var d = new Date();
      var s = '';
      var h = d.getHours();
      if (h < 10) {
        s = '0' + h;
      } else {
        s = h;
      }
      var m = d.getMinutes();
      if (m < 10) {
        s = s + ':0' + m;
      } else {
        s = s + ':' + m;
      }
      var ss = d.getSeconds();
      // s=s+":00";
      s = s + ':' + ss;
      return s;
    },
    timeDifference: function (startTime, endTime) {
      var start1 = startTime.split(':');
      var startAll = parseInt(start1[1] * 60) + parseInt(start1[2]);
      var end1 = endTime.split(':');
      var endAll = parseInt(end1[1] * 60) + parseInt(end1[2]);
      return endAll - startAll;
    },
    submit() {
      console.log(this.dataForm);
      var formData;
      if (
        (this.$data.clientChatEn == null) |
        (this.$data.clientChatEn == undefined)
      ) {
        formData = {
          clientChatId: '',
          score: this.dataForm.score,
          remark: this.dataForm.remark,
        };
      } else {
        formData = {
          clientChatId: this.$data.clientChatEn.clientChatId,
          score: this.dataForm.score,
          remark: this.dataForm.remark,
        };
      }
      this.$http.post({
        url: '/backend2/api/CallReport/setWebChatSatify',
        params: formData,
        successCallback: (rs) => {
          console.log('rss');
          console.log(rs);
        },
      });
      this.clientQuit();
      this.rateDialogVisible = false;
    },
    /**
     * 注册账号信息
     */
    regClientChatEn: function (userName) {
      console.log("regClientChatEn", userName)
      if (userName == '' || userName == undefined) {
        this.$data.clientChatEn.clientChatId = Number.parseInt(
          Date.now() + Math.random()
        );
      }
      else {
        this.$data.clientChatEn.clientChatId = userName.split(',')[3] + userName.split(',')[5]
      }
      // 名称格式：姓+6位数字
      if (userName == '' || userName == undefined) {
        userName = "张"
        // switch (this.$data.clientChatEn.clientChatId % 5) {
        //   case 0:
        //     userName = '张';
        //     break;
        //   case 1:
        //     userName = '李';
        //     break;
        //   case 2:
        //     userName = '王';
        //     break;
        //   case 3:
        //     userName = '赵';
        //     break;
        //   case 4:
        //     userName = '孙';
        //     break;
        // }
      }

      // var tmpId = this.$data.clientChatEn.clientChatId.toString();
      // userName += tmpId.substr(tmpId.length - 6, 6);
      this.$data.clientChatEn.clientChatName = userName;
      console.log("this.$data.clientChatEn", this.$data.clientChatEn)
      // 模拟消息
      this.addChatMsg({
        role: 'robot',
        avatarUrl: this.$data.robotEn.avatarUrl,
        contentType: 'transformServer',
      });
    },

    /**
     * 注册socket
     * @param {String} serverChatId 服务端chatId
     */
    regSocket: function (serverChatId, serverChatName) {
      //cmd@login;type@agent;cont@{clientChatId:11,clientChatName:22,avatarUrl:33}
      this.serverChatEn.serverChatId = serverChatId;
      var msg =
        "cmd@selectServerChatId;type@client;cont@{'serverChatId':'" +
        serverChatId +
        "','clientChatId':'" +
        this.clientChatEn.clientChatId +
        "','source':'" + this.source +
        "','idcard':'" + this.idcard +
        "','phone':'" + this.phone +
        "','uId':'" + this.uId +
        "','orderNo':'" + this.orderNo +
        "'}";
      ws.send(msg);
      this.addChatMsg({
        role: 'sys',
        contentType: 'text',
        content: '人工客服 ' + serverChatName + ' 正在为你服务',
      });
      $("#transfBtn").addClass('is-disabled');
    },

    /**
     * 结束会话
     */
    closeChat: function () {
      this.clientQuit();

      if (this.firtFlag == true) {
        this.$refs.common_chat.closeChat();
      }
    },
    closewin2: function () {
      var createTime = Date.now();
      var msg =
        "cmd@sendMsg;type@client;cont@{'serverChatId':'" +
        this.serverChatEn.serverChatId +
        "','clientChatId':'" +
        this.clientChatEn.clientChatId +
        "','avatarUrl':'" +
        'static/image/im_client_avatar.png' +
        "','content':'" +
        '客户已结束会话' +
        "','contentType':'" +
        'text' +
        "','role':'" +
        'agent' +
        "','chatState':'" +
        'agent' +
        "','createTime':'" +
        createTime +
        "','source':'" +
        this.source +
        "','idcard':'" +
        this.idcard +
        "','phone':'" +
        this.phone +
        "','uId':'" +
        this.uId +
        "','orderNo':'" +
        this.orderNo +
        "'}";
      ws.send(msg);
      ws = null;
      this.$router.go(-1);
    },
    closewin: function () {
      this.clientQuit();
      this.$router.go(-1);
    },
    /**
     * 添加chat对象的msg
     * @param {Object} msg 消息对象；eg：{role:'sys',content:'含有新的消息'}
     * @param {String} msg.role 消息所有者身份；eg：'sys'系统消息；
     * @param {String} msg.contentType 消息类型；text:文本(默认)；image:图片
     * @param {String} msg.content 消息内容
     * @param {Function} successCallback 添加消息后的回调
     */
    addChatMsg: function (msg, successCallback) {
      if (this.converEnd == true) {
        return false;
      }
      // 1.设定默认值
      msg.role = msg.role == undefined ? 'sys' : msg.role;
      msg.contentType = msg.contentType == undefined ? 'text' : msg.contentType;
      msg.createTime =
        msg.createTime == undefined ? new Date() : msg.createTime;


      var msgList = this.$data.chatInfoEn.msgList
        ? this.$data.chatInfoEn.msgList
        : [];

      // 2.插入消息
      // 1)插入日期
      // 实际场景中，在消息上方是否显示时间是由后台传递给前台的消息中附加上的，可参考 微信Web版
      // 此处进行手动设置，5分钟之内的消息，只显示一次消息
      msg.createTime = new Date(msg.createTime);
      if (
        this.$data.chatInfoEn.lastMsgShowTime == null ||
        msg.createTime.getTime() -
        this.$data.chatInfoEn.lastMsgShowTime.getTime() >
        1000 * 60 * 5
      ) {
        msgList.push({
          role: 'sys',
          contentType: 'text',
          content: this.$ak.Utils.getDateTimeStr(msg.createTime, 'Y-m-d H:i:s'),
        });
        this.$data.chatInfoEn.lastMsgShowTime = msg.createTime;
      }

      // 2)插入消息
      msgList.push(msg);

      // 3.设置chat对象相关属性
      this.$data.chatInfoEn.msgList = msgList;
      this.$refs.common_chat.goEnd();
      var s = this.getNow();
      this.currTime = s;
      // this.stopTime()
      // this.setTime()
      // 4.回调
      successCallback && successCallback();
    },
    sendBuss: function (rs) {
      console.log("sendBuss", rs)
      var content = rs
      var contentType = "text"
      var createTime = this.getNow();
      var msg0 =
        "cmd@sendBuss;type@client;cont@{'serverChatId':'" +
        this.serverChatEn.serverChatId +
        "','clientChatId':'" +
        this.clientChatEn.clientChatId +
        "','avatarUrl':'" +
        'static/image/im_client_avatar.png' +
        "','content':'" +
        content +
        "','contentType':'" +
        contentType +
        "','createTime':'" +
        createTime +
        "','source':'" +
        this.source +
        "','idcard':'" +
        this.idcard +
        "','phone':'" +
        this.phone +
        "','uId':'" +
        this.uId +
        "','orderNo':'" +
        this.orderNo +
        "'}";
      console.log("msg0", msg0)
      console.log("ws", ws)
      ws.send(msg0);
    },

    /**
     * 发送消息
     * @param {Object} rs 回调对象
     */
    sendMsg: function (rs) {
      console.log('rrrr');
      console.log(this.converEnd);
      if (this.converEnd == true) {
        return false;
      }
      var s = this.getNow();
      this.currTime = s;
      var msg = rs.msg;
      console.log(rs, "sendMsg_rs")
      msg.role = 'client';
      msg.avatarUrl = this.$data.clientChatEn.avatarUrl;
      if (this.$data.chatInfoEn.chatState == 'robot') {
        var avatarUrl = msg.avatarUrl;
        var content = msg.content;
        if (content == '' || content == undefined) {
        } else {
          if (content.indexOf('@') > 0) {
            content = content.replace('@', '~');
          }
        }

        var contentType = msg.contentType;
        var createTime = Date.now();
        var role = msg.role;
        var fileUrl = msg.fileUrl;
        var chatState = 'robot';
        var msg0;
        if (contentType == 'image' || contentType == 'file') {
          msg0 =
            "cmd@sendMsg;type@client;cont@{'serverChatId':'" +
            this.serverChatEn.serverChatId +
            "','clientChatId':'" +
            this.clientChatEn.clientChatId +
            "','avatarUrl':'" +
            avatarUrl +
            "','fileUrl':'" +
            fileUrl +
            "','content':'" +
            content +
            "','contentType':'" +
            contentType +
            "','role':'" +
            role +
            "','chatState':'" +
            chatState +
            "','createTime':'" +
            createTime +
            "','source':'" +
            this.source +
            "','idcard':'" +
            this.idcard +
            "','phone':'" +
            this.phone +
            "','uId':'" +
            this.uId +
            "','orderNo':'" +
            this.orderNo +
            "'}";
          console.log("if_" + msg0)
        } else {
          debugger
          msg0 =
            "cmd@sendMsg;type@robot;cont@{'serverChatId':'" +
            this.serverChatEn.serverChatId +
            "','clientChatId':'" +
            this.clientChatEn.clientChatId +
            "','avatarUrl':'" +
            avatarUrl +
            "','content':'" +
            content +
            "','contentType':'" +
            contentType +
            "','role':'" +
            role +
            "','chatState':'" +
            chatState +
            "','createTime':'" +
            createTime +
            "','source':'" +
            this.source +
            "','idcard':'" +
            this.idcard +
            "','phone':'" +
            this.phone +
            "','uId':'" +
            this.uId +
            "','orderNo':'" +
            this.orderNo +
            "'}";
          console.log("else")
        }
        console.log("a:", msg0)
        ws.send(msg0);
        // 机器人发送接口
      } else if (this.$data.chatInfoEn.chatState == 'agent') {
        var avatarUrl = msg.avatarUrl;
        var content = msg.content;
        if (content == '' || content == undefined) {
        } else {
          if (content.indexOf('@') > 0) {
            content = content.replace('@', '~');
          }
        }

        var fileUrl = msg.fileUrl;
        var contentType = msg.contentType;
        var createTime = msg.createTime;
        var role = 'agent';
        var chatState = 'agent';
        //ws.send('avatarUrl:' + avatarUrl + ',content:' + content + ',contentType:' +contentType + ',createTime:' +createTime + ',role:' + role + ",chatState:" + chatState + ',cmd:msg')
        var msg0 = '';
        if (contentType == 'image' || contentType == 'file') {
          msg0 =
            "cmd@sendMsg;type@client;cont@{'serverChatId':'" +
            this.serverChatEn.serverChatId +
            "','clientChatId':'" +
            this.clientChatEn.clientChatId +
            "','avatarUrl':'" +
            avatarUrl +
            "','fileUrl':'" +
            fileUrl +
            "','content':'" +
            content +
            "','contentType':'" +
            contentType +
            "','role':'" +
            role +
            "','chatState':'" +
            chatState +
            "','createTime':'" +
            createTime +
            "','source':'" +
            this.source +
            "','idcard':'" +
            this.idcard +
            "','phone':'" +
            this.phone +
            "','uId':'" +
            this.uId +
            "','orderNo':'" +
            this.orderNo +
            "'}";
          console.log('msg000');
          console.log(msg0);
        } else {
          msg0 =
            "cmd@sendMsg;type@client;cont@{'serverChatId':'" +
            this.serverChatEn.serverChatId +
            "','clientChatId':'" +
            this.clientChatEn.clientChatId +
            "','avatarUrl':'" +
            avatarUrl +
            "','content':'" +
            content +
            "','contentType':'" +
            contentType +
            "','role':'" +
            role +
            "','chatState':'" +
            chatState +
            "','createTime':'" +
            createTime +
            "','source':'" +
            this.source +
            "','idcard':'" +
            this.idcard +
            "','phone':'" +
            this.phone +
            "','uId':'" +
            this.uId +
            "','orderNo':'" +
            this.orderNo +
            "'}";
        }
        //  if (ws.readyState == 1) {
        //     //如果连接正常
        //     ws.send('heartCheck');
        //   } else {
        //     //否则重连
        //     self.reconnect();
        //   }
        console.log(msg0)
        ws.send(msg0);
      }
      // 2.添加到消息集合
      var self = this;
      this.addChatMsg(msg, function () {
        self.goEnd();
      });
    },

    /**
     * 显示转接客服Dialog
     */
    transferDialog_show: function () {
      this.chatInfoEn.chatState = 'agent';
      this.regSocket('1632322309243');
    },

    /**
     * 转接客服dialog_提交
     */
    transferDialog_submit: function (rs) {
      console.log(rs);
      this.transferDialogVisible = false;
      this.chatInfoEn.chatState = 'agent';
      this.regSocket(rs.serverChatId);
      console.log(rs.serverChatId);
    },

    /**
     * 注销dialog_提交
     */
    logoutDialog_submit: function () {
      this.$data.logoutDialogVisible = false;
      this.addChatMsg({
        role: 'sys',
        content: '本次会话已结束',
      });
    },

    /**
     * 注销dialog_取消
     */
    logoutDialog_cancel: function () {
      this.$data.logoutDialogVisible = false;
    },

    /**
     * 聊天记录滚动到底部
     */
    goEnd: function () {
      this.$refs.common_chat.goEnd();
    },
    clientQuit: function () {
      var createTime = Date.now();
      var msg =
        "cmd@sendMsg;type@client;cont@{'serverChatId':'" +
        this.serverChatEn.serverChatId +
        "','clientChatId':'" +
        this.clientChatEn.clientChatId +
        "','avatarUrl':'" +
        'static/image/im_client_avatar.png' +
        "','content':'" +
        '客户已结束会话' +
        "','contentType':'" +
        'text' +
        "','role':'" +
        'agent' +
        "','chatState':'" +
        'agent' +
        "','createTime':'" +
        createTime +
        "','source':'" +
        this.source +
        "','idcard':'" +
        this.idcard +
        "','phone':'" +
        this.phone +
        "','uId':'" +
        this.uId +
        "','orderNo':'" +
        this.orderNo +
        "'}";
      console.log(msg);
      ws.send(msg);
    },
    /**
     * chat回调
     */
    chatCallback: function (rs) {
      this.chatFlag = true; //转人工
      if (rs.eventType == 'transformServer') {
        var msg =
          "cmd@getServerChatEnList;type@client;cont@{'clientChatId':'" +
          this.clientChatEn.clientChatId +
          "'}";
        console.log("getServerChatEnList", msg)
        ws.send(msg);
        // this.transferDialog_show();
      }
    },
    /**
     * 显示评分dialog
     */
    showRateDialog: function () {
      this.firtFlag = false;
      this.rateDialogVisible = true;
      // this.$data.rateDialogVisible = true;
      // this.$nextTick(() => {
      //     this.$refs.im_rate.init();
      // });
    },
    /**
     * 显示留言dialog
     */
    showLeaveDialog: function () {
      this.$data.leaveDialogVisible = true;
      this.$nextTick(() => {
        this.$refs.im_leave.init();
      });
    },
    start() {
      //开启心跳
      var self = this;
      self.timeoutObj && clearTimeout(self.timeoutObj);
      self.serverTimeoutObj && clearTimeout(self.serverTimeoutObj);
      self.timeoutObj = setTimeout(function () {
        console.log('ws22');
        console.log(ws);
        //这里发送一个心跳，后端收到后，返回一个心跳消息，
        if (ws.readyState == 1) {
          //如果连接正常
          ws.send('heartCheck');
        } else {
          //否则重连
          self.reconnect();
        }
        self.serverTimeoutObj = setTimeout(function () {
          //超时关闭
          ws.close();
        }, self.timeout);
      }, self.timeout);
    },
    reset() {
      //重置心跳
      var that = this;
      //清除时间
      clearTimeout(that.timeoutObj);
      clearTimeout(that.serverTimeoutObj);
      //重启心跳
      that.start();
    },
    herBert() {
      this.herBertTimer = setInterval(() => {
        var that = this
        // console.log("herbert")
        // console.log("ws", ws)
        if (ws.readyState == 1) {
          var msg = "cmd@herbert;type@client;cont@{'herbert':'1'}";
          // console.log(msg);
          ws.send(msg);
        }
        else {
          console.log("that.reconnect")
          that.reconnect()
        }
      }, 6000);
    },
    reconnect() {
      //重新连接
      console.log('reconnect');
      var that = this;
      if (that.lockReconnect) {
        return;
      }
      console.log('1');
      that.lockReconnect = true;
      //没连接上会一直重连，设置延迟避免请求过多
      that.timeoutnum && clearTimeout(that.timeoutnum);
      that.timeoutnum = setTimeout(function () {
        //新连接
        that.websocket();
        that.lockReconnect = false;
      }, 5000);
    },
    websocketonopen() {
      console.log("open clientChatEn:", this.clientChatEn)

      // ws.send("login_this.clientChatEn.clientChatName_"+this.clientChatEn.clientChatName)
      if (this.clientChatEn.clientChatName == null || this.clientChatEn.clientChatName == '') {
        this.openTimer = setInterval(() => {
          var that = this
          if (that.clientChatEn.clientChatName == null || that.clientChatEn.clientChatName == '') {

          }
          else {
            var msg0 = "cmd@login;type@client;cont@{'clientChatId':'" +
              that.clientChatEn.clientChatId +
              "','clientChatName':'" +
              that.clientChatEn.clientChatName +
              "','avatarUrl':'" +
              that.clientChatEn.avatarUrl +
              "','serverChatId':'01" +
              "'}"
            ws.send(msg0);
            clearInterval(that.openTimer)
            that.openTimer = null;
          }
        }, 500)
      } else {
        var msg0 = "cmd@login;type@client;cont@{'clientChatId':'" +
          this.clientChatEn.clientChatId +
          "','clientChatName':'" +
          this.clientChatEn.clientChatName +
          "','avatarUrl':'" +
          this.clientChatEn.avatarUrl +
          "','serverChatId':'0" +
          "'}"
        console.log("msg0", msg0)
        ws.send(
          msg0
        );
        var msg = "cmd@getKnListtt;type@text;cont@{'keywords':'" + '' + "'}";
        ws.send(msg);
      }
      console.log('open');
      console.log(ws);
      this.herBert();
    },
    websocketonerror() {
      console.log('websocketonerror');
    },
    websocketclose() {
      console.log('connection closed');
      // this.reconnect();
    },
    websocketonmessage(evt) {
      var c = evt.data;
      console.log('c----------------------------------------------------', c);
      debugger
      if (c.indexOf('MoreKnList') > 0) {
        var a = c.split('@');
        console.log(a);
        this.list = [];
        for (var i = 0; i < a.length; i++) {
          var c = a[i];
          c = c.replace(/'/g, '"');
          var o = JSON.parse(c);
          this.list.push(o);
        }
      } else {
        console.log('ccc');
        console.log(c);
        if (c == undefined || c == '') {
          // alert('坐席全忙,请稍候');
          this.addChatMsg({
            role: 'sys',
            contentType: 'text',
            content: '坐席全忙,请稍候',
          });
          console.log(" transfBtn", $("#transfBtn"))
          $("#transfBtn").attr("disabled", false)
          $("#transfBtn").removeAttr("disabled");
          $("#transfBtn").removeClass('is-disabled');
          this.chatFlag = false;
          this.$refs.common_chat.setMan();
          return;
        }
        c = c.replace(/'/g, '"');
        var o = JSON.parse(c);
        console.log(o);
        var s = this.getNow();
        this.currTime = s;
        var _this = this;
        if (o.cmd == 'undefined' || o.cmd == '') {
        } else {
          if (o.cmd == 'sendMsg') {
            if (o.content == 'noanswer') {
            } else {
              _this.msgFlag = true;
              console.log('11');
              _this.msgInterval();
              this.sendIntervalTimer = null;
              this.backFlag = true;
              clearInterval(this.sendIntervalTimer);
            }
            console.log(o.content);
            var content = o.content;
            if (content == '' || content == undefined) {
            } else {
              var role = o.role
              if (role == "sys") {
                this.addChatMsg({
                  role: 'sys',
                  contentType: 'text',
                  content: content,
                });
                return;
              }

              if (content.indexOf('#http://') > 0) {
                console.log('#http://>0');
                var a = content.indexOf('#http://');
                var b = content.lastIndexOf('#');
                var content1 = content.substr(0, a);
                var content2 = content.substr(a + 1, b - a + 1);
                var content3 = content.substr(b + 1);
                o.content =
                  content1 +
                  "<a target='_blank' href='" +
                  content2 +
                  "'>" +
                  content2 +
                  '</a>' +
                  content3;
                console.log(o.content);
              } else if (content.indexOf('#https://') > 0) {
                var a = content.indexOf('#https://');
                var b = content.lastIndexOf('#');
                var content1 = content.substr(0, a);
                var content2 = content.substr(a + 1, b - a + 1);
                var content3 = content.substr(b + 1);
                o.content =
                  content1 +
                  "<a target='_blank' href='" +
                  content2 +
                  "'>" +
                  content2 +
                  '</a>' +
                  content3;
              } else {
                if (content.indexOf('http://') >= 0) {
                  console.log('>0');
                  o.content =
                    "<a target='_blank' href='" +
                    content +
                    "'>" +
                    content +
                    '</a>';
                  console.log(o.content);
                }
                if (content.indexOf('https://') >= 0) {
                  console.log('>0');
                  o.content =
                    "<a target='_blank' href='" +
                    content +
                    "'>" +
                    content +
                    '</a>';
                  console.log(o.content);
                }
              }

              if (content.indexOf('~') > 0) {
                o.content = content.replace('~', '@');
              }
            }
            console.log("oooooo", o)
            if (o.contentType == "image" || o.contentType == "file") {
              var fileUrl0 = o.fileUrl

              fileUrl0 = fileUrl0.replace("https://www.wanxinleasing.com:9005/", "/bairecords/")
              o.fileUrl = fileUrl0;
              console.log("fileUrl0", fileUrl0)
            }
            var avatarUrl = o.avatarUrl
            avatarUrl = "static/image/im_client_avatar.png"
            this.addChatMsg({
              role: 'server',
              avatarUrl: avatarUrl,
              contentType: o.contentType,
              content: o.content,
              fileUrl: o.fileUrl,
            });
          } else {
            this.chatInfoEn.chatState = 'agent';
            // this.regSocket(o.serverChatId)
            if (o.serverChatName == 'allbusy') {
              var qTotal = o.qTotal;
              this.addChatMsg({
                role: 'sys',
                contentType: 'text',
                content: '您好，目前还有' + qTotal + '在等待',
              });
            } else {
              // console.log("kkkkk")
              // console.log(o)
              this.regSocket(o.serverChatId, o.serverChatName);
            }
          }
        }
      }

      // this.reset();
    },
    websocket() {
      // ws = new WebSocket('ws://192.168.0.38:9001/ws/tct');
      console.log("websocket")
      ws = new WebSocket('wss://www.wanxinleasing.com:9005/ws/tct');
      console.log("ws:", ws)
      this.projId = 1;
      ws.onopen = this.websocketonopen;
      //连接错误
      ws.onerror = this.websocketonerror;
      //接收信息
      ws.onmessage = this.websocketonmessage;
      //连接关闭
      ws.onclose = this.websocketclose;
    },
  },
  created() { },
  beforeDestroy() {
    var createTime = Date.now();
    var msg =
      "cmd@sendMsg;type@client;cont@{'serverChatId':'" +
      this.serverChatEn.serverChatId +
      "','clientChatId':'" +
      this.clientChatEn.clientChatId +
      "','avatarUrl':'" +
      'static/image/im_client_avatar.png' +
      "','content':'" +
      '客户已结束会话' +
      "','contentType':'" +
      'text' +
      "','role':'" +
      'agent' +
      "','chatState':'" +
      'agent' +
      "','createTime':'" +
      createTime +
      "','source':'" +
      this.source +
      "','idcard':'" +
      this.idcard +
      "','phone':'" +
      this.phone +
      "','uId':'" +
      this.uId +
      "','orderNo':'" +
      this.orderNo +
      "'}";
    ws.send(msg);
    ws = null;

    console.log("beforeDestroy")
    if (this.timer) {
      clearInterval(this.timer); // 在Vue实例销毁前，清除我们的定时器
    }
    this.clientQuit();

    if (this.firtFlag == true) {
      this.$refs.common_chat.closeChat();
    }
  },
  async mounted() {
    var url = window.location.href;
    var cs = ""
    var i = url.indexOf('?')
    if (i > 0) {
      cs = url.substring(i + 1)
    }
    var encryptedData = decodeURIComponent(cs)
    const key = CryptoJS.enc.Utf8.parse('wanxinrzzly_2024');
    let bytes = CryptoJS.AES.decrypt(encryptedData, key, {
      mode: CryptoJS.mode.ECB, // 使用ECB模式，不使用IV
      padding: CryptoJS.pad.Pkcs7
    });
    let decryptedData = bytes.toString(CryptoJS.enc.Utf8);
    var rs = decryptedData;
    var arr = rs.split('&')
    this.source = arr[0].split('=')[1]
    this.idcard = arr[1].split('=')[1]
    this.phone = arr[2].split('=')[1]
    this.uId = arr[3].split('=')[1]
    if (this.source == "''") {
      this.source = ""
    }
    if (this.idcard == "''") {
      this.idcard = ""
    }
    if (this.phone == "''") {
      this.phone = ""
    }
    if (this.uId == "''") {
      this.uId = ""
    }

    this.userType = "未注册"
    //有手机号就是你注册的用户，有身份证号就是指你实名的用户。
    if (this.idcard != '') {
      this.userType = "已认证"
    } else if (this.phone != '') {
      this.userType = "已注册"
    }
    this.imClientChatWrapperWidth = '100%';
    this.imClientinnerWidth = '95%';
    var d = new Date();
    var s = '';
    var h = d.getHours();
    if (h < 10) {
      s = '0' + h;
    } else {
      s = h;
    }
    var m = d.getMinutes();
    if (m < 10) {
      s = s + ':0' + m;
    } else {
      s = s + ':' + m;
    }
    s = s + ':00';
    this.currTime = s;
    var userName = "游客";
    var x = userName + "," + this.userType + "," + this.idcard + "," + this.phone + "," + this.uId + "," + this.source
    this.userInfo = x
    var dealName = "游客";
    var formData = { customPhone: this.phone };
    console.log(formData);
    var lastName = this.phone;
    this.orderNo = ""
    this.$http.post({
      url: 'https://www.wanxinleasing.com:9005/backend2/api/car_customerService/getCar_CustomerByCustomPhone',
      params: formData,
      successCallback: (rs) => {
        console.log('rssgetCar_CustomerByCustomPhone');
        console.log(rs);
        if (rs.length > 0) {
          userName = rs[0].customName
          dealName = rs[0].dealName
          lastName = userName
          this.orderNo = rs[0].orderNo
        }
        x = userName + "," + this.userType + "," + this.idcard + "," + this.phone + "," + this.uId + "," + this.source + "," + dealName + "," + lastName + "," + this.orderNo
        // console.log(x, "xxxxxx")
        this.userInfo = x
        this.regClientChatEn(x); //添加客户信息
      },
    });
    var that = this
    that.websocket();
    console.log("get")

    const ip = localStorage.getItem('Ip')
    console.log("ip:", ip)
    // var pc = new RTCPeerConnection({ iceServers: [] });
    // pc.createDataChannel('');
    // pc.createOffer().then(function (sdp) {
    //   pc.setLocalDescription(sdp);
    // }).catch(function (reason) {
    //   console.log('Failed to create session description: ' + reason.toString());
    // });
    // pc.onicecandidate = function (event) {
    //   if (event.candidate) {
    //     console.log('ICE Candidate: ' + event.candidate.candidate);
    //     // The IP address can be extracted from the candidate string
    //   }
    // };

  },
};
</script>

<style lang="less">
@import '../../common/css/base.less';

.imClient-wrapper {
  #common-wrapper();
}

.imClient-inner {
  width: 850px;
  // width: 95%;
  height: 100%;
  margin: 10px auto 0px;
  overflow: hidden;
  box-shadow: 0 1px 5px 2px #ccc;

  .imClient-header {
    position: relative;
    height: 35px;
    box-sizing: border-box;
    // background: #1072b5;
    background: #d12b1e;
    font-size: 13px;
    color: #ffffff;

    .name-wrapper {
      margin-left: 20px;
    }

    .logo {
      height: 45px;
      width: auto;
    }

    .opr-wrapper {
      right: 20px;
      font-size: 16px;
      cursor: pointer;

      .fa {
        margin-left: 10px;
      }
    }
  }

  .imClient-main {
    max-width: 100%;
    height: 600px;
    position: relative;

    &>.item {
      float: left;
      height: 100%;
      border-top-width: 0px;
      border-right-width: 0px;
      box-sizing: border-box;

      &:last-child {
        border-right-width: 1px;
      }
    }

    &>.imClientChat-wrapper {
      width: 550px;
      // width: 100%;
      border-right: 1px solid #ccc;
    }

    &>.imClientInfo-wrapper {
      width: 300px;
    }
  }
}

// 信息区域
.imClientInfo-wrapper {
  width: 100%;
  height: 100%;
  background: #ffffff;

  .imClientInfo-notice-wrapper,
  .imClientInfo-faq-wrapper {
    .imClientInfo-item-header {
      font-weight: bolder;
      font-size: 16px;
      color: #1072b5;
      padding: 10px 15px 0;
    }
  }

  .imClientInfo-notice-wrapper {
    .imClientInfo-notice-main {
      padding: 0 15px;

      &>.link {
        margin: 10px 0;
        font-size: 12px;
        color: #000000;
      }
    }
  }

  .imClientInfo-faq-wrapper {
    height: 380px;
    border-top: 1px solid #ccc;

    .imClientInfo-faq-main {
      height: 100%;
      overflow-y: auto;
      overflow-x: hidden;

      .el-collapse {
        border: 0px;

        .el-collapse-item__header {
          position: relative;
          padding: 0px 15px;
          font-size: 12px;
          background: transparent;
          color: #000000;

          &.is-active {
            color: #f7455d;
          }

          .el-collapse-item__arrow {
            position: absolute;
            left: 267px;
          }
        }

        .el-collapse-item__wrap {
          background: transparent;

          .el-collapse-item__content {
            font-size: 12px;
            color: #959699;
            padding: 0px 15px 10px;
          }
        }
      }
    }
  }
}

// element-UI
.el-dialog {
  width: 500px;
  height: 750px;
  background: #fdfbfb;
  color: #000000;
}

.height-class {
  height: 300px !important;
  //  height: calc(~'100% - 365px');
}

.height-class-input {
  height: 200px !important;
}
</style>
