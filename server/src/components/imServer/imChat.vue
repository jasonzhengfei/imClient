<!-- 聊天记录 -->
<template>
  <div>
    <div class="item im-record imRecord-wrapper">
      <header class="header">
        <div class="kf-info-wrapper" style="display: inline">
          <!-- <img class="kf-avatar" :src="storeServerChatEn.avatarUrl" /> -->
          <span style="float: left; margin-top: 14px; color: blue">
            {{ userChineseName }}</span>
          <el-radio-group @change="changeStatus" style="
              float: left;
              margin-left: 5px;
              margin-top: 8px;
              display: inline;
            " v-model="status" size="small">
            <el-radio-button label="离线"></el-radio-button>
            <el-radio-button label="在线"></el-radio-button>
          </el-radio-group>
          <!-- <span class="kf-name position-h-v-mid">{{storeServerChatEn.serverChatName}}</span> -->
        </div>
        <div class="client-info-wrapper">
          <p>
            <i class="fa fa-user on-line"></i>{{ storeCurrentChatEnlist.length }}
          </p>
        </div>
      </header>
      <main class="main">
        <div v-if="storeCurrentChatEnlist.length > 0" class="item-list">
          <div class="item" v-for="(tmpEn, index) in storeCurrentChatEnlist" :key="index" @click="selectChat(tmpEn)"
            v-bind:class="{
              active:
                selectedChatEn != null &&
                tmpEn.clientChatId == selectedChatEn.clientChatId,
            }">
            <div class="followicon-wrapper">
              <i class="iconfont icon-zhidingwujiaoxing position-h-v-mid" @click="isShow(index)">X</i>
              <i class="iconfont icon-zhidingwujiaoxing position-h-v-mid" :class="{ active: tmpEn.isFollow }"
                @click.stop="toggleFollowIcon(tmpEn)"></i>
            </div>
            <div class="info-wrapper">
              <p class="first-p">
                <span class="name">{{ tmpEn.clientChatName.split(',')[6]
                  + "_" + tmpEn.clientChatName.split(',')[7] + "(" + tmpEn.clientChatName.split(',')[5] + ")" }}</span>
                <span class="lastMsgTime">{{
                  getLastMsgTimeStr(tmpEn.lastMsgTime)
                  }}</span>
              </p>
              <p class="second-p">
                <span style="color: red;display: inline-block;height: 15px;" class="lastMsgContent"
                  v-html="tmpEn.lastMsgContent"></span>
                <el-badge class="newMsgCount" :value="tmpEn.newMsgCount" :max="99"
                  v-show="tmpEn.newMsgCount > 0"></el-badge>
              </p>
            </div>
          </div>
        </div>
        <div v-else-if="storeCurrentChatEnlist.length == 0" class="empty-wrapper">
          <div class="content">
            <i class="iconfont fa fa-commenting-o"></i>
            <p class="title">当前没有会话</p>
          </div>
        </div>
      </main>
    </div>
    <div class="item im-chat imChat-wrapper">
      <!-- 头部 -->
      <header class="imChat-header">
        <span style="padding: 8px; font-size: 14px; background: rgb(231, 32, 32); color: white; margin-top: 10px;"
          class="name">{{ storeSelectedChatEn.clientChatName.split(',')[0] }}</span>


        <span style="padding: 8px; font-size: 14px; background: rgb(231, 32, 32); color: white; margin-top: 10px;">{{
          storeSelectedChatEn.clientChatName.split(',')[1] }}</span>
        <span style="padding: 8px; font-size: 14px; background: rgb(16, 114, 181); color: white; margin-top: 10px;"
          v-show="storeSelectedChatEn.state == 'on'" class="customerdetails" @click="showDetails()">
          客户详情
        </span>
        <span class="time">{{
          getAccessTimeStr(storeSelectedChatEn.accessTime)
          }}</span>
        <!-- <span v-show="storeSelectedChatEn.state == 'on'" class="on-line">在线</span>
        <span v-show="storeSelectedChatEn.state == 'off'" class="off-line">离线</span> -->
      </header>
      <main class="imChat-main">
        <!-- 聊天框区域 -->
        <common-chat ref="common_chat" @addChatMsg="addChatMsg" :chatInfoEn="storeSelectedChatEn"
          :oprRoleName="'server'" @transNewSeat="transNewSeat" @transReSetClientChatEn="transReSetClientChatEn"
          @sendMsg="sendMsg" @transferUserSeat="transferUserSeat"></common-chat>
      </main>
    </div>
    <div class="knowledge">
      <el-tabs v-model="activeName" @tab-click="handleClick">
        <el-tab-pane label="知识库" name="first">
          <div>
            <el-form ref="knowf" :model="knowform" label-width="80px">
              <el-row :gutter="20" style="margin-top: 10px">
                <el-col :span="8">
                  <el-form-item label="关键词" style="margin-bottom: 3px">
                    <el-input style="width: 120px" v-model="knowform.keywords" />
                  </el-form-item>
                </el-col>
                <el-col :span="3">
                  <el-button type="default" style="margin-left: 120px" @click="searchkn">
                    搜索
                  </el-button>
                </el-col>
              </el-row>
              <el-row>
                <el-col :span="23">
                  <span style="
                  font-size: 12px;
                  color: grey;
                  margin-left: 20px;
                  margin-bottom: 10px;
                ">
                    例：字段1,字段2,....
                  </span>
                </el-col>
              </el-row>
            </el-form>
            <el-table :data="listk" border height="600px" style="margin-top: 8px">
              <el-table-column align="left" label="知识内容" prop="content" width="200px" show-overflow-tooltip />
              <el-table-column align="left" fixed="right" label="操作">
                <template slot-scope="scope">
                  <el-button size="mini" type="primary" @click="show(scope.row)">
                    预览
                  </el-button>
                </template>
              </el-table-column>
              <template #empty>
                <el-image :src="require('@/assets/data_empty.png')" class="vab-data-empty" />
              </template>
            </el-table>
          </div>
        </el-tab-pane>
        <el-tab-pane label="历史会话" name="third">
          <div>
            <iframe ref="iframewebchat" id="webchat" :src="urlwebchat" frameborder="0" scrolling="no"></iframe>
          </div>
        </el-tab-pane>
        <el-tab-pane label="创建工单" name="second">
          <div>
            <iframe ref="iframe" id="workorderCreate" :src="url" frameborder="0" scrolling="no"></iframe>
          </div>
        </el-tab-pane>
      </el-tabs>


    </div>
    <el-dialog :visible.sync="dialogTableVisible">
      <div style="
          margin-top: 20px;
          margin-left: 5px;
          line-height: 30px;
          padding-bottom: 20px;
        " v-html="content" />
    </el-dialog>
  </div>
</template>

<script>
import commonChat from '@/components/common/common_chat.vue';
var ws = null;
import axios from 'axios';
export default {
  components: {
    commonChat: commonChat,
  },
  data() {
    return {
      changeStatusFlag: false,
      lockReconnect: false,
      timeoutnum: null,
      url: "",
      urlwebchat: "",
      activeName: "first",
      userSeatNo: '',
      port: '',
      idx: '',
      knowform: {
        keywords: '',
      },
      source: "",
      phone: '',
      uId: "",
      orderNo: "",
      idCard: "",
      userChineseName: '',
      dialogTableVisible: false,
      content: '',
      listk: [],
      status: '在线',
      herBertTimer: null,
      // storeSelectedChatEn:{
      //     clientChatName:'',
      //     accessTime:'',
      //     state:'on'
      // }
    };
  },
  computed: {
    storeSelectedChatEn() {
      return this.$store.imServerStore.getters.selectedChatEn;
    },
    storeHaveNewMsgDelegate() {
      return this.$store.imServerStore.getters.haveNewMsgDelegate;
    },
    storeServerChatEn() {
      return this.$store.imServerStore.getters.serverChatEn;
    },

    selectedChatEn() {
      return this.$store.imServerStore.getters.selectedChatEn;
    },
    // 当前会话列表
    storeCurrentChatEnlist() {
      return this.$store.imServerStore.getters.currentChatEnlist;
    },
  },

  watch: {

    storeSelectedChatEn(value) {
      this.$refs.common_chat.goEnd();
    },
    storeHaveNewMsgDelegate(value) {
      this.$refs.common_chat.goEnd();
    },
  },
  methods: {
    handleClick() {
      console.log("this.storeSelectedChatEn", this.storeSelectedChatEn)
      if (this.activeName == "second") {
        this.url = "http://192.168.0.39:11060/#/workorder/create/?" + "userSeatNo=" + this.userSeatNo;
      }
      if (this.activeName == "third") {
        var phoneNum = this.storeSelectedChatEn.clientChatName.split(',')[3]
        this.urlwebchat = "http://192.168.0.39:11060/#/workorder/webchat/?phoneNo=" + phoneNum
        //  this.urlwebchat="http://localhost:8081/#/workorder/webchat?phoneNo=15156044550"
      }
    },
    showDetails() {
      console.log(this.storeSelectedChatEn)
      var phoneNum = this.storeSelectedChatEn.clientChatName.split(',')[3]
      var agentNum = this.userSeatNo
      const url = 'http://192.168.0.39:11060/#/popup/?phoneNum=' + phoneNum + '&agentNum=' + agentNum + '&callId=undefined&IVR=undefined';
      window.open(url, '_blank');
    },
    beforeunloadHandler() {
      this._beforeUnload_time = new Date().getTime();
    },
    unloadHandler(e) {
      this._gap_time = new Date().getTime() - this._beforeUnload_time;
      debugger
      var params = { userSeatNo: this.userSeatNo };
      this.$http.post({
        url: '/backend2/Api/UserManagement/changeChatStatus',
        params: params,
        successCallback: (rs) => {
          console.log('rr22s');
          console.log(rs);
        },
      });
    },
    async isShow(index) {
      console.log(index, "index")
      console.log(this.storeCurrentChatEnlist[index])
      var data = this.storeCurrentChatEnlist[index]
      var clientChatName = data.clientChatName.split(',')[6]
      console.log("clientChatName", clientChatName)
      console.log(clientChatName.indexOf('留言'), "ii")
      if (clientChatName.indexOf('留言') > -1) {
        var clientChatId = data.clientChatId
        console.log("clientChatId", clientChatId)
        var url = '/backend2/api/car_customerService/updateRemarkByClientChatId';
        var param = { clientChatId: clientChatId }
        var x = await axios.post(url, param)
      }
      var serverChatEn = this.$store.imServerStore.getters.serverChatEn;
      var msg =
        "cmd@agentDoClose;type@agent;cont@{'serverChatId':'" +
        serverChatEn.serverChatId +
        "','serverChatName':'" +
        serverChatEn.serverChatName +
        "','clientChatId':'" +
        data.clientChatId +
        "','avatarUrl':'" +
        data.avatarUrl +
        "','content':'" +
        "agentDoClose" +
        "','contentType':'" +
        "text" +
        "'}";
      console.log(msg, "msg")
      ws.send(
        msg
      );
      this.storeCurrentChatEnlist.splice(index, 1);
    },
    show(row) {
      console.log(row);
      console.log(row.content);
      this.content = row.content;
      this.dialogTableVisible = true;
    },
    searchkn() {
      // var msg="cmd@getKnList;type@text;cont@{'keywords':'"+ this.knowform.keywords+"'}"
      // ws.send(msg)
      var params = { keywords: this.knowform.keywords };
      this.$http.post({
        url: '/backend2/Api/kmManagement/getKnContentByKey',
        params: params,
        successCallback: (rs) => {
          console.log('rrs');
          console.log(rs);
          this.listk = rs;
        },
      });
    },
    changeStatus() {
      console.log(this.status);
      if (this.status == '在线') {
        var serverChatEn = this.$store.imServerStore.getters.serverChatEn;
        var msg = "cmd@setStatus;type@agent;cont@{'status':'1','serverChatId':'" +
          serverChatEn.serverChatId +
          "','serverChatName':'" +
          serverChatEn.serverChatName +
          "','avatarUrl':'" +
          serverChatEn.avatarUrl +
          "'}"
        console.log(msg, "msg")
        console.log("ws", ws)
        ws.send(
          msg
        );
      } else {
        var serverChatEn = this.$store.imServerStore.getters.serverChatEn;
        var msg = "cmd@setStatus;type@agent;cont@{'status':'0','serverChatId':'" +
          serverChatEn.serverChatId +
          "','serverChatName':'" +
          serverChatEn.serverChatName +
          "','avatarUrl':'" +
          serverChatEn.avatarUrl +
          "'}"
        console.log(msg, "msg")
        ws.send(
          msg
        );
      }
    },
    /**
     * 选中当前列表的chat
     * @param {Object} en call实体类
     */
    selectChat: function (en) {
      console.log('en');
      console.log(en);
      this.port = en.port;
      this.$store.imServerStore.dispatch('selectChat', {
        clientChatId: en.clientChatId,
      });
      this.source = en.clientChatName.split(',')[5]
      this.phone = en.clientChatName.split(',')[3]
      this.idCard = en.clientChatName.split(',')[2]
      this.uId = en.clientChatName.split(',')[4]
      this.orderNo = en.clientChatName.split(',')[8]
      var clientChatId = en.clientChatId
      this.urlwebchat = ""
      console.log("storeSelectedChatEn:::", this.storeSelectedChatEn)
      this.$emit('selectedChat', {}); // 事件上传

    },

    /**
     * 设置关注
     */
    toggleFollowIcon: function (en) {
      // en.isFollow = !en.isFollow;
      // // 排序
      // this.$store.imServerStore.commit('sortCurrentChatEnlist', {});
    },

    /**
     * 获取背景class
     * @param {string} clientChatName 姓名
     */
    getBgClass: function (clientChatName) {
      // var rs = clientChatName.charCodeAt(0) % 5;
      // return 'bg' + rs;
    },

    /**
     * 返回chat对象的最后一次消息时间
     * @param {String|Date} sValue 传入的时间字符串
     */
    getLastMsgTimeStr: function (sValue) {
      // if (sValue == null) {
      //     return '';
      // }
      // var rs = this.$ak.Utils.getDateTimeStr(sValue, 'H:i:s');
      // return rs;
    },
    /**
     * 发送消息
     * @param {Object} rs 回调对象
     */
    transferUserSeat: function () {
      // var o = {"avatarUrl":"/static/image/im_server_avatar.png","serverChatId":"111","serverChatName":"aaa"}
      // var a = new Array(2);
      // a[0] =o;
      // o = {"avatarUrl":"/static/image/im_server_avatar.png","serverChatId":"222","serverChatName":"bbb"}
      // a[1] = o;
      // this.$store.imServerStore.commit('setTransferUserSeatList', a);

      var msg = "cmd@getTransferUserSeatList;type@agent;cont@{'herbert':'1'}";
      console.log(msg);
      ws.send(msg);

      // var msg=this.storeServerChatEn.serverChatId +
      //     "','clientChatId':'" +
      //     this.storeSelectedChatEn.clientChatId 
      // console.log("transferUserSeat"+msg);
    },
    transNewSeat: function (msg) {
      console.log("transNewSeatmsg", msg)
      var msg = msg.msg
      var serverChatId = msg.serverChatId
      var clientChatId = this.storeSelectedChatEn.clientChatId
      var transServerChatId = msg.transServerChatId
      var serverChatName = msg.serverChatName
      var avatarUrl = msg.avatarUrl
      var source = msg.source//关注
      var idcard = msg.idcard
      var phone = msg.phone
      var uId = msg.uId
      var orderNo = msg.orderNo
      console.log("关注:source", source)
      var msg = "cmd@transNewSeat;type@agent;cont@{'avatarUrl':'" + avatarUrl + "','serverChatName':'" + serverChatName + "','serverChatId':'" + serverChatId + "','clientChatId':'" + clientChatId + "','transServerChatId':'" + transServerChatId + "','source':'" + source + "','idcard':'" + idcard + "','phone':'" + phone + "','uId':'" + uId + "','orderNo':'" + orderNo + "'}"
      console.log("msg::", msg)
      ws.send(msg);
    },
    transReSetClientChatEn(clientChatEn) {
      clientChatEn.clientChatId = "00000000"
      console.log("transReSetClientChatEn", clientChatEn)
      this.$store.imServerStore.commit('setClientChatEn', clientChatEn);
    },
    addChatMsg: function (rs) {

      console.log("addChatMsg--", rs)
      console.log("this.storeSelectedChatEn.clientChatId", this.storeSelectedChatEn.clientChatId)

      var msg = rs
      this.$store.imServerStore.dispatch('addChatMsg', {
        clientChatId: this.storeSelectedChatEn.clientChatId,
        msg: msg,
      });
    },
    sendMsg: function (rs) {
      console.log("storeSelectedChatEn", this.storeSelectedChatEn)
      if (this.storeSelectedChatEn.clientChatName == "" || this.storeSelectedChatEn.clientChatName == undefined) {
        return;
      }
      var msg = rs.msg;
      msg.role = 'server';
      msg.avatarUrl = this.storeServerChatEn.avatarUrl;
      // 1.socket发送消息
      this.$store.imServerStore.dispatch('sendMsg', {
        clientChatId: this.storeSelectedChatEn.clientChatId,
        msg: msg,
      });

      // 2.附加到此chat对象的msg集合里
      this.$store.imServerStore.dispatch('addChatMsg', {
        clientChatId: this.storeSelectedChatEn.clientChatId,
        msg: msg,
        successCallback: function () {
          rs.successCallbcak && rs.successCallbcak();
        },
      });
      //3.向客户端发送消息
      var avatarUrl = msg.avatarUrl;
      var content = msg.content;
      var contentType = msg.contentType;
      var createTime = msg.createTime;
      var fileUrl = msg.fileUrl;
      var role = 'client';
      var chatState = 'client';
      var msg0 = '';

      if (content == '' || content == undefined) {
      } else {
        if (content.indexOf('&gt;') >= 0) {
          content = content.replace('&gt;', '');
        }
        if (content.indexOf('@') > 0) {
          content = content.replace('@', '~');
        }
      }

      //ws.send('avatarUrl:' + avatarUrl + ',content:' + content + ',contentType:' +contentType + ',createTime:' +createTime + ',role:' + role + ",chatState:" + chatState + ',cmd:msg')
      if (contentType == 'image' || contentType == 'file') {
        msg0 =
          "cmd@sendMsg;type@agent;cont@{'serverChatId':'" +
          this.storeServerChatEn.serverChatId +
          "','clientChatId':'" +
          this.storeSelectedChatEn.clientChatId +
          "','avatarUrl':'" +
          avatarUrl +
          "','content':'" +
          content +
          "','fileUrl':'" +
          fileUrl +
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
          "','uId':'" +
          this.uId +
          "','orderNo':'" +
          this.orderNo +
          "','phone':'" +
          this.phone +
          "','idcard':'" +
          this.idCard +
          "'}";
      } else {
        msg0 =
          "cmd@sendMsg;type@agent;cont@{'serverChatId':'" +
          this.storeServerChatEn.serverChatId +
          "','clientChatId':'" +
          this.storeSelectedChatEn.clientChatId +
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
          "','uId':'" +
          this.uId +
          "','orderNo':'" +
          this.orderNo +
          "','phone':'" +
          this.phone +
          "','idcard':'" +
          this.idCard +
          "'}";
      }
      var port = this.storeSelectedChatEn.port;
      console.log(port);
      console.log("msg0", msg0)
      ws.send(msg0);
      // if (port == '19002') {
      //   ws.send(msg0);
      // }

    },
    goEnd: function () {
      this.$refs.common_chat.goEnd();
    },
    /**
     * 获取chat的访问时间
     * @param {Date} accessTime 问时间
     */
    getAccessTimeStr: function (accessTime) {
      // return this.$ak.Utils.getDateTimeStr(accessTime, 'Y-m-d H:i:s');
    },
    herBert() {
      this.herBertTimer = setInterval(() => {
        // console.log(ws,"ws")
        var that = this
        if (ws.readyState == 1) {
          var msg = "cmd@herbert;type@client;cont@{'herbert':'1'}";
          // console.log(msg);
          ws.send(msg);
        } else {
          that.reconnect();
        }


      }, 4000);
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
        that.changeStatusFlag = true
      }, 5000);
    },
    websocketonopen() {
      var serverChatEn = this.$store.imServerStore.getters.serverChatEn;
      console.log(serverChatEn);
      ws.send(
        "cmd@login;type@agent;cont@{'status':'1','serverChatId':'" +
        serverChatEn.serverChatId +
        "','serverChatName':'" +
        serverChatEn.serverChatName +
        "','avatarUrl':'" +
        serverChatEn.avatarUrl +
        "','count':'0" +
        "'}"
      );
      if (this.changeStatusFlag == true) {
        this.changeStatus()
        this.changeStatusFlag = false;
      }
      this.herBert();
    },


    websocketonmessage(evt) {
      var c = evt.data;
      console.log('cccc');
      console.log(c);
      if (c.indexOf('TransferUserSeatList') > 0) {
        var a = c.split('@');
        var listk = [];
        for (var i = 0; i < a.length; i++) {
          var c = a[i];
          c = c.replace(/'/g, '"');
          var o = JSON.parse(c);
          listk.push(o);
        }
        this.$store.imServerStore.commit('setTransferUserSeatList', listk);
      } else {
        if (c.indexOf('MoreKnList') > 0) {
          var a = c.split('@');
          console.log(a);
          this.listk = [];
          for (var i = 0; i < a.length; i++) {
            var c = a[i];
            c = c.replace(/'/g, '"');
            var o = JSON.parse(c);
            this.listk.push(o);
          }
        } else {
          c = c.replace(/'/g, '"');
          var o = JSON.parse(c);
          if (c.indexOf('clientOn') > 0) {
            var clientChatEn = {
              clientChatId: o.clientChatId,
              clientChatName: o.clientChatName,
              avatarUrl: '',
              port: '19001',
              projName: 'tct',
              idcard: o.idcard,
              phone: o.phone,
              source: o.source,
              uId: o.uId,
              orderNo: o.orderNo
            };
            this.phone = o.phone
            console.log("clientChatEn", clientChatEn)
            this.$store.imServerStore.commit('setClientChatEn', clientChatEn);
            this.$store.imServerStore.dispatch('CLIENT_ON');
          } else {
            // chatState: "client"
            //收到客户发来的消息
            var content = o.content;
            if (content == '' || content == undefined) {
            } else {
              if (content.indexOf('#http://') > 0) {
                console.log('#http://>0');
                var a = content.indexOf('#http://');
                var b = content.lastIndexOf('#');
                var content1 = content.substr(0, a);
                var content2 = content.substr(a + 1, b - a - 1);
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
                var content2 = content.substr(a + 1, b - a - 1);
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

            if (o.content == "customerSelect") {

            } else {
              var msg = {
                avatarUrl: o.avatarUrl,
                // content:'(ICI)'+ o.content,
                content: o.content,
                contentType: o.contentType,
                fileUrl: o.fileUrl,
                role: o.role,
                createTime: o.createTime,
              };
              console.log("oooo:", o)
              this.$store.imServerStore.dispatch('addChatMsg', {
                clientChatId: o.clientChatId,
                msg: msg,
                successCallback: function () {
                  //  rs.successCallbcak && rs.successCallbcak();
                },
              });
            }

          }
        }
      }


    },
    websocketclose() {
      console.log(ws, "ws")
      var that = this
      that.reconnect();
      console.log('connection 19001 closed');
    },
    websocket() {
      // ws = new WebSocket('ws://192.1680.126:19001/ws');
      ws = new WebSocket('ws://192.168.0.38:9001/ws/tct');
      ws.onopen = this.websocketonopen;
      ws.onmessage = this.websocketonmessage;
      ws.onclose = this.websocketclose;
    },

  },
  async mounted() {
    window.addEventListener('beforeunload', (e) => this.beforeunloadHandler(e));
    window.addEventListener('unload', (e) => this.unloadHandler(e));
    var url = window.location.href;
    console.log('url');
    console.log(url);
    var dz_url = url;
    if (url.indexOf('#') > 0) {
      dz_url = url.split('#')[0];
    }
    console.log("dz_ur" + dz_url);
    //var cs = dz_url.split('?')[1]; //获取?之后的参数字符串
    var cs = url.split('?')[1]; //获取?之后的参数字符串
    console.log("cs" + cs);
    var cs_arr = cs.split('&'); //参数字符串分割为数组
    console.log("cs_arr" + cs_arr);
    var cs = {};
    for (var i = 0; i < cs_arr.length; i++) {
      //遍历数组，拿到json对象
      cs[cs_arr[i].split('=')[0]] = cs_arr[i].split('=')[1];
    }
    console.log(cs);
    console.log(cs.userSeatNo);
    this.userSeatNo = cs.userSeatNo;
    this.$store.imServerStore.commit('setChatName', cs.userSeatNo);
    this.$store.imServerStore.dispatch('SERVER_ON');
    this.websocket();
    var param = { userSeatNo: cs.userSeatNo };
    var url = '/backend2/api/car_customerService/getLeavIngMsg';

    var xx = await axios.post(url, param)
    console.log("xx", xx)
    var xdata = xx.data
    var rs = xdata.data
    if (rs.length > 0) {
      for (var i = 0; i < rs.length; i++) {
        var phone = rs[i].phone
        console.log("phone", phone)
        var formData = { customPhone: phone };
        var url0 = '/backend2/api/car_customerService/getCar_CustomerByCustomPhone'
        var x = await axios.post(url0, formData)
        var ydata = x.data
        var rsa = ydata.data
        console.log("rsa", rsa)
        console.log("rs", rs)
        console.log("i", i)
        var source = rs[i].source
        console.log("source", source)
        var uId = rs[i].uId

        console.log("uId", uId)
        var idcard = rs[i].idCard
        console.log("idcard", idcard)
        var orderNo = ""
        var userType = "未注册"
        //有手机号就是你注册的用户，有身份证号就是指你实名的用户。
        if (idcard != '') {
          userType = "已认证"
        } else if (phone != '') {
          userType = "已注册"
        }
        var userName = "游客";
        var dealName = "游客";
        var lastName = "游客";
        console.log('rssgetCar_CustomerByCustomPhone');
        console.log(rsa);
        if (rsa.length > 0) {
          console.log("rs[0" + rsa[0])
          userName = rsa[0].customName
          dealName = rsa[0].dealName
          orderNo = rsa[0].orderNo
          lastName = userName
          console.log(userName, "userName")
          console.log(dealName, "dealName")
        }
        var clientChatId = rs[i].clientChatId
        console.log("clientChatId", clientChatId)
        var x = userName + "," + userType + "," + idcard + "," + phone + "," + uId + "," + source + "," + "留言_" + dealName + "," + lastName + "," + orderNo
        console.log("x", x)
        var o = { clientChatId: clientChatId, clientChatName: x, idcard: idcard, phone: phone, source: source, uId: uId, orderNo: orderNo }
        var clientChatEn = {
          clientChatId: o.clientChatId,
          clientChatName: o.clientChatName,
          avatarUrl: '',
          port: '19001',
          projName: 'tct',
          idcard: o.idcard,
          phone: o.phone,
          source: o.source,
          uId: o.uId,
          orderNo: orderNo
        };
        console.log("clientChatEn", clientChatEn)
        this.$store.imServerStore.commit('setClientChatEn', clientChatEn);
        this.$store.imServerStore.dispatch('CLIENT_ON');
      }
    }
    // return

    // this.$http.post({
    //   url: '/backend2/api/car_customerService/getLeavIngMsg',
    //   params: param,
    //   successCallback: (rs) => {
    //     console.log(rs);
    //     if (rs.length > 0) {
    //       for (var i = 0; i < rs.length; i++) {
    //         var phone = rs[i].phone
    //         console.log("phone", phone)
    //         var formData = { customPhone: phone };
    //         var ret = axios.post({
    //           url: '/backend2/api/car_customerService/getCar_CustomerByCustomPhone',
    //           params: formData,
    //           successCallback: (rsa) => { }
    //         })
    //         this.$http.post({
    //           url: '/backend2/api/car_customerService/getCar_CustomerByCustomPhone',
    //           params: formData,
    //           successCallback: (rsa) => {

    //             console.log("rsa", rsa)
    //             console.log("rs", rs)
    //             console.log("i", i)
    //             var source = rs[i].source
    //             console.log("source", source)
    //             var uId = rs[i].uId
    //             console.log("uId", uId)
    //             var idcard = rs[i].idcard
    //             console.log("idcard", idcard)
    //             var userType = "未注册"
    //             //有手机号就是你注册的用户，有身份证号就是指你实名的用户。
    //             if (idcard != '') {
    //               userType = "已认证"
    //             } else if (phone != '') {
    //               userType = "已注册"
    //             }
    //             var userName = "游客";
    //             var dealName = "游客";
    //             var lastName = "游客";
    //             console.log('rssgetCar_CustomerByCustomPhone');
    //             console.log(rsa);
    //             if (rsa.length > 0) {
    //               console.log("rs[0" + rsa[0])
    //               userName = rsa[0].customName
    //               dealName = rsa[0].dealName
    //               lastName = userName
    //               console.log(userName, "userName")
    //               console.log(dealName, "dealName")
    //             }
    //             var clientChatId = rs[i].clientChatId
    //             console.log("clientChatId", clientChatId)
    //             var x = userName + "," + userType + "," + idcard + "," + phone + "," + uId + "," + source + "," + "留言_" + dealName + "," + lastName
    //             console.log("x", x)
    //             var o = { clientChatId: clientChatId, clientChatName: x, idcard: idcard, phone: phone, source: source, uId: uId }
    //             var clientChatEn = {
    //               clientChatId: o.clientChatId,
    //               clientChatName: o.clientChatName,
    //               avatarUrl: '',
    //               port: '19001',
    //               projName: 'tct',
    //               idcard: o.idcard,
    //               phone: o.phone,
    //               source: o.source,
    //               uId: o.uId
    //             };
    //             console.log("clientChatEn", clientChatEn)
    //             this.$store.imServerStore.commit('setClientChatEn', clientChatEn);
    //             this.$store.imServerStore.dispatch('CLIENT_ON');
    //           },
    //         });


    //       }

    //     }

    //   },
    // });




  },
  destroyed() {
    window.removeEventListener('beforeunload', (e) =>
      this.beforeunloadHandler(e)
    );
    window.removeEventListener('unload', (e) => this.unloadHandler(e));
  },
};
</script>
<style lang="less">
@import '../../common/css/base.less';

.imServer-wrapper {
  #common-wrapper();
}

.el-input__inner {
  width: 200px !important
}

.knowledge {
  // width: 310px;
  width: 550px;
  float: right;

}

.imServer-wrapper {
  width: 100%;
  height: 100%;
  position: absolute;
  overflow: hidden;

  .imServer-main {
    height: 100%;
    max-width: 100%;
    position: relative;

    &>.item {
      float: left;
      border-right: 1px solid #e6e6e6;
      height: 100%;
    }

    &>.im-record {
      // width: 280px;
      width: 220px;
    }

    &>.im-chat {
      // width: calc(~'99% - 580px');
      width: calc(~'99% - 760px');
    }
  }
}

.imChat-wrapper {
  .imChat-header {
    display: flex;
    align-items: center;
    // width: 100%;
    height: 50px;
    padding-left: 10px;
    border-bottom: 1px solid #e6e6e6;
    font-size: 16px;

    span {
      margin-right: 20px;
    }

    .on-line {
      color: #70ed3a;
    }

    .off-line {
      color: #bbbbbb;
    }
  }

  .imChat-main {
    height: calc(~'100% - 150px');
  }
}

.imRecord-wrapper {
  width: 100%;
  height: 550px;
  overflow: hidden;
  border: 0px;

  &>.header {
    display: flex;
    align-items: center;
    height: 50px;
    border-bottom: 1px solid #e6e6e6;

    .kf-info-wrapper {
      position: relative;
      // width: 200px;
      height: 50px;
      padding: 0 20px;

      .kf-avatar {
        width: 50px;
        height: 50px;
      }

      .kf-name {
        font-size: 16px;
      }
    }

    .client-info-wrapper {
      p:first-child {
        margin-bottom: 5px;
      }

      .fa {
        margin-right: 10px;
      }
    }
  }

  &>.main {
    height: calc(~'100% - 50px');
    position: relative;

    .item-list {
      height: calc(~'100% - 46px');
      overflow-y: auto;

      .item {
        position: relative;
        height: 63px;
        padding: 0px;
        border-bottom: 1px solid #e6e6e6;
        cursor: pointer;

        &.active,
        &:hover {
          background-color: #0095ff;

          .info-wrapper .first-p .name,
          .info-wrapper .second-p .lastMsgContent,
          .info-wrapper .first-p .lastMsgTime {
            color: #0a0a0a;
          }

          .iconfont {
            display: initial !important;
          }
        }

        .followicon-wrapper {
          position: relative;
          float: left;
          width: 25px;
          height: 100%;

          .iconfont {
            // display: none;
            font-size: 12px;
            color: #0c0c0c;

            &.active {
              display: initial;
              color: #f9ce1d;
            }
          }
        }

        .platicon-wrapper {
          position: relative;
          float: left;
          width: 50px;
          height: 100%;

          .header-img {
            padding: 10px;
            font-size: 16px;
            color: #000;
            border-radius: 50%;

            &.bg0 {
              background-color: #ef7777;
            }

            &.bg1 {
              background-color: #00bcd4;
            }

            &.bg2 {
              background-color: #009688;
            }

            &.bg3 {
              background-color: #ffc107;
            }

            &.bg4 {
              background-color: #ff5722;
            }
          }
        }

        .info-wrapper {
          position: relative;
          float: left;
          width: 185px;
          padding-top: 5px;
          padding-left: 5px;

          .first-p {
            clear: both;
            padding-top: 11px;

            .name {
              display: inline-block;
              float: left;
              width: 180px;
              font-size: 14px;
              color: #3e3e3e;
              white-space: nowrap;
              text-overflow: ellipsis;
              overflow: hidden;
              text-align: left;
              font-weight: bolder;
            }

            .lastMsgTime {
              float: right;
              font-size: 12px;
              color: #8d8d8d;
            }
          }

          .second-p {
            clear: both;
            padding-top: 5px;
            line-height: 1.2;

            .lastMsgContent {
              display: inline-block;
              width: 150px;
              margin-top: 3px;
              font-size: 12px;
              color: #8d8d8d;
              white-space: nowrap;
              text-overflow: ellipsis;
              text-align: left;
              overflow: hidden;
            }

            .newMsgCount {
              position: relative;
              top: -15px;
              float: right;

              .el-badge__content {
                border: 1px solid #ffffff00;
              }
            }
          }
        }
      }
    }

    .empty-wrapper {
      font-size: 16px;
      color: #3e3e3e;
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);

      .content {
        width: 170px;
        height: 200px;
        margin: 0px auto;
        text-align: center;
        color: #867c7c;

        .iconfont {
          font-size: 90px;
        }

        .title {
          margin-top: 25px;
        }
      }
    }
  }


}

#workorderCreate {
  width: 600px;
  height: 1200px;


}

#webchat {
  width: 600px;
  height: 1200px;
}
</style>
