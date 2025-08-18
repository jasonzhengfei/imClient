<!-- 聊天记录 -->
<template>
  <div class="common_chat-wrapper">
    <div class="common_chat-inner">
      <!-- 聊天记录 -->
      <div v-if="chatLoaded" class="common_chat-main" :class="{ 'height-class': focusFlag }" id="common_chat_main"
        ref="common_chat_main">
        <div class="common_chat-main-content">
          <div class="inner">
            <div v-for="(item, index) in chatInfoEn.msgList" :key="index">
              <!-- 系统消息 -->
              <div v-if="item.role == 'sys'" class="item sys">
                <!-- 1)文本类型 -->
                <div v-if="item.contentType == 'text'" class="text-content">
                  <p style="color:#b0b0b0">{{ fomatDate(item.createTime) }}</p>
                  <p>{{ item.content }}</p>
                </div>
              </div>
              <!-- 客户、客服 -->
              <div v-else class="item" :class="{
                sender: item.role == oprRoleName,
                receiver: item.role != oprRoleName,
              }">
                <div class="info-wrapper" :class="item.state">
                  <!-- 头像 -->
                  <div class="avatar-wrapper">
                    <img class="kf-img" :src="item.avatarUrl" />
                  </div>
                  <!-- 1)文本类型 -->
                  <div v-if="item.contentType == 'text'" class="item-content common_chat_emoji-wrapper-global">
                    <p class="text">{{ fomatDate(item.createTime) }}</p>
                    <p class="text" v-html="getqqemojiEmoji(item.content)"></p>
                  </div>
                  <!-- 2)图片类型 -->
                  <div v-else-if="item.contentType == 'image'" class="item-content">
                    <p class="text">{{ fomatDate(item.createTime) }}</p>
                    <img class="img" :src="item.fileUrl" @click="imgViewDialog_show(item)" />
                    <!-- <img class="img" :src="item.fileUrl" /> -->
                  </div>
                  <!-- 3)文件类型 -->
                  <div v-else-if="item.contentType == 'file'" class="item-content">
                    <p class="text">{{ fomatDate(item.createTime) }}</p>
                    <div class="file">
                      <i class="file-icon iconfont fa fa-file"></i>
                      <div class="file-info">
                        <p class="file-name">
                          <!-- <span @click="downloadFile(item.fileUrl)">{{ getFileName(item.fileUrl) }} <span
                              style="margin-left:10px">下载 </span></span> -->
                        </p>
                        <div class="file-opr">
                          <div>
                            <!-- v-show="item.state=='success'"  -->
                            <!-- <a
                              class="file-download"
                              :href="item.fileUrl"
                              target="_blank"
                              :download="getFileName(item.fileUrl)"
                              >下载</a
                            > -->
                            <!-- <a class="file-download" :href="item.fileUrl" target="_blank"
                              :download="getFileName(item.fileUrl)">{{ getFileName(item.fileUrl) }}下载</a>
                          
                           -->
                            <!-- <a class="file-download" :href="item.fileUrl" @click="downloadFile" target="_blank"
                              :download="getFileName(item.fileUrl)">{{ getFileName(item.fileUrl) }}下载</a> -->

                            <!-- <a class="file-download" :href="item.fileUrl" target="_blank" :download="getFileName(item.fileUrl)">下载</a> -->
                            <el-button @click="browsePdf(item.fileUrl)"> 预览</el-button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div v-if="item.contentType == 'transformServer'"
                    class="item-content common_chat_emoji-wrapper-global">
                    <div style="
                        margin-top: 10px;
                        margin-bottom: 15px;
                        width: 250px;
                      ">
                      <div style="margin-top: 15px">
                        <span style="color: #1072b5; font-size: 16px">
                          我猜你想问
                        </span>
                      </div>
                    </div>
                    <div class="text0" v-for="item in curQuesions" :key="item.id" @click="tran(item.id)">
                      {{ item.keywords }}
                      <!-- <p v-if="item.type==1" >{{item.question}}</p>
                                                <a v-else :href="item.answer"> {{item.question}}</a> -->
                    </div>
                    <div style="margin-top: 10px">
                      <!-- <span style="padding:5px;line-height:20px;font-size:14px;background:#1072b5;color:white;margin-left:5px;" v-if="fShow" @click="showf()"> 上一页 </span>  -->
                      <span style="
                          margin-left: 5px;
                          margin-right: 5px;
                          padding: 5px;
                          line-height: 20px;
                          font-size: 14px;
                          background: #d12b1e;
                          color: white;
                        " @click="shown()">
                        换一换
                      </span>
                    </div>
                  </div>
                  <div v-if="item.contentType == 'transformServer'">
                    <div style="clear:both"> </div>
                    <div style="margin-top:15px">
                      <span style="color: #1072b5; font-size: 16px">
                        请选择办理的业务:
                      </span>
                    </div>
                    <div style="margin-top:10px">
                      <span style="
                          margin-left: 5px;
                          margin-right: 5px;
                          padding: 5px;
                          line-height: 20px;
                          font-size: 14px;
                          background: #d12b1e;
                          color: white;" @click="doBussiness(1)">
                        打款凭证反馈
                      </span>
                      <span style="
                          margin-left: 5px;
                          margin-right: 5px;
                          padding: 5px;
                          line-height: 20px;
                          font-size: 14px;
                          background: #d12b1e;
                          color: white;" @click="doBussiness(2)">
                        业务办理
                      </span>
                      <span style="
                          margin-left: 5px;
                          margin-right: 5px;
                          padding: 5px;
                          line-height: 20px;
                          font-size: 14px;
                          background: #d12b1e;
                          color: white;" @click="doBussiness(3)">
                        修改还款卡
                      </span>
                      <span style="
                          margin-left: 5px;
                          margin-right: 5px;
                          padding: 5px;
                          line-height: 20px;
                          font-size: 14px;
                          background: #d12b1e;
                          color: white;" @click="doBussiness(4)">
                        异议反馈
                      </span>
                    </div>

                  </div>
                  <div v-if="item.contentType == 'questionAnswer'"
                    class="item-content common_chat_emoji-wrapper-global">
                    <p class="text">
                      {{ item.content }}
                    </p>
                  </div>
                  <div v-if="item.contentType == 'satisfy'" class="item-content common_chat_emoji-wrapper-global">
                    <p class="text">
                      请对客服的服务进行
                      <el-button style="cursor: pointer" type="text" @click="showSatisfy()">【评价】</el-button>
                    </p>
                  </div>
                  <div v-if="item.contentType == 'questionAnswera'"
                    class="item-content common_chat_emoji-wrapper-global">
                    <p class="text">
                      <a target="_blank" :href="item.content">
                        {{ item.content }}</a>
                    </p>
                  </div>
                  <div v-if="item.contentType == 'transformServer2'"
                    class="item-content common_chat_emoji-wrapper-global">
                    <p class="text">
                      您的问题我还在学习当中，您可以转
                      <el-button id="transfBtn" :disabled="!transFlag" type="primary"
                        @click="chatCallback('transformServer')">人工客服</el-button>
                    </p>
                  </div>
                  <div v-if="item.contentType == 'questionAnswer3'"
                    class="item-content common_chat_emoji-wrapper-global">
                    <p class="text">
                      {{ item.content
                      }}<el-button id="transfBtn" :disabled="!transFlag" type="primary"
                        @click="chatCallback('transformServer')">人工客服</el-button>
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- 底部区域 -->
      <div class="common_chat-footer">
        <div>
          <!-- 表情、文件选择等操作 -->
          <!-- <div class="opr-wrapper">
            <span style="
                padding: 5px;
                line-height: 20px;
                font-size: 14px;
                background: #d12b1e;
                color: white;
              " @click="book()">
              展位预订</span>
            <span style="
                padding: 5px;
                font-size: 14px;
                background: #d12b1e;
                color: white;
              " @click="meet()">
              会议活动</span>
            <span style="
                padding: 5px;
                font-size: 14px;
                background: #d12b1e;
                color: white;
              " @click="register()">
              预登记</span>
             <span style="padding:5px;font-size:14px;;background:#FF0000;color:white" @click="ticket()"> 购票</span> 
            <span style="
                padding: 5px;
                font-size: 14px;
                background: #d12b1e;
                color: white;
              " @click="rate()">
              服务评价</span> -->

          <!-- <span  style="padding:5px;font-size:14px;;background:#1072b5;color:white" @click="test()"> 测试</span>                       
          </div> -->
          <div class="opr-wrapper" style="margin-top: 5px">
            <common-chat-emoji id="commonchatemojid" class="item" ref="qqemoji"
              @select="qqemoji_selectFace"></common-chat-emoji>
            <el-upload style="float:left" class="upload-demo"
              action="https://www.wanxinleasing.com:9005/backend2/api/file/upload" :multiple="false"
              accept="image/*|video/*" :before-upload="beforeUpload" :file-list="fileList" :on-success="uploadSucessRe">
              <i style="font-size: 30px;color:#aaa" class="iconfont fa fa-picture-o"></i>
            </el-upload>
            <el-upload style="float:left;margin-left:10px" class="upload-demo"
              action="https://www.wanxinleasing.com:9005/backend2/api/file/upload" :multiple="false"
              accept=".docx,.doc,.xls,.xlsx,.pdf,.txt,.ppt" :before-upload="beforeUpload" :file-list="fileList"
              :on-success="uploadSucessFile">
              <i style="font-size: 26px;padding-top:3px;color:#aaa" class="iconfont fa fa-file-o"></i>
            </el-upload>
            <i v-show="historyFlag == true" @click="showHistory()"
              style="font-size: 30px;margin-left:10px;color:#aaa;padding-top:1px" class="iconfont fa fa-book"></i>
            <!-- <span @click="showHistory()" style="
                padding-left: 5px;
                padding-right:5px;
                font-size: 30px;
                background: #1072b5;
                color: white;

                float:left
              ">
              历史</span> -->

            <!-- <a class="item" href="javascript:void(0)" @click="fileUpload_click('file')">
              <i class="iconfont fa fa-file-o"></i>
            </a>
             accept="image/*" 
            <form method="post" enctype="multipart/form-data">
              <input type="file" multiple accept="image/*" name="uploadFile" id="common_chat_opr_fileUpload" style="
                  display: none;
                  position: absolute;
                  left: 0;
                  top: 0;
                  width: 0%;
                  height: 0%;
                  opacity: 0;
                " />
            </form> -->


            <!-- <label for="camera">
              <div class="camera">
                <i class="iconfont fa fa-file-o"></i>
                <input id="camera" ref="camera" type="file" accept="image/*" capture="camera" style="display:none;
                                    position: absolute;
                  left: 0;
                  top: 0;
                  width: 0%;
                  height: 0%;
                  opacity: 0;
                  " @change="handleInputChange">

              </div>
            </label> -->

            <!-- <div class="uploader">
    <div class="uploader_wrapper">
      <div class="uploader_upload">
        <i class="iconfont fa fa-file-o"></i>
        <input type="file" id="fileInputId" :accept="accept" ref="fileInput" @change="handleFileUpload" />
      </div>
    </div>
  </div> -->


          </div>
          <!-- 聊天输入框 -->
          <!-- @keydown="inputContent_keydown" @mouseup="inputContent_mouseup" @mouseleave="inputContent_mouseup" -->
          <div class="input-wrapper">
            <div style="font-size:20px" maxlength="450" class="inputContent common_chat_emoji-wrapper-global"
              :class="{ 'height-class-input': focusFlag }" id="common_chat_input" contenteditable="true"
              @paste.stop="inputContent_paste" @drop="inputContent_drop" @focus="focuson" @blur="focusoff"
              ref="chatContent"></div>
          </div>


          <el-button id="btnSend" type="primary" size="small" class="send-btn" :class="chatInfoEn.state"
            style="cursor: pointer; background: #d12b1e;margin-top:5px" @click="sendText()">发送</el-button>

          <!-- <el-button type="primary" size="small" class="send-btn" :class="chatInfoEn.state" @touch="sendText()" :disabled="chatInfoEn.inputContent.length==0">发送</el-button> -->
        </div>
        <!-- 离线 -->
        <div v-show="chatInfoEn.state == 'off' || chatInfoEn.state == 'end'" class="off-wrapper">
          <span class="content">会话已经结束</span>
        </div>
      </div>
    </div>
    <!-- 图片查看dialog -->
    <el-dialog title :visible.sync="imgViewDialogVisible" class="imgView-dialog" :modal="false">
      <div class="header">
        <i class="iconfont fa fa-remove" @click="imgViewDialog_close"></i>
      </div>
      <!-- <div class="main" @mousewheel="bbimg(this)"> -->
      <div class="main">
        <img style="width:300px;" ref="image" class="img " :src="imgViewDialog_imgSrc" />
      </div>
    </el-dialog>
    <!-- 满意度dialog -->
    <el-dialog :visible.sync="rateDialogVisible" :close-on-press-escape="false" width="80%" style="height: 400px">
      <div class="imRate-wrapper">
        <div v-show="!resultVisible" class="main">
          <p class="title">请对客服的服务进行评价</p>
          <el-row>
            <el-rate v-model="dataForm.score" show-text :texts="['很差', '不好', '一般', '满意', '惊喜']">
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
    <!--预登记  -->
    <el-dialog :visible.sync="registerDialogVisible" :close-on-press-escape="false" width="98%">
      <div id="registerDiv">
        <iframe id="registerframe" :src="registerurl" frameborder="0"></iframe>
      </div>
    </el-dialog>
    <!--购票 -->
    <el-dialog :visible.sync="ticketDialogVisible" :close-on-press-escape="false" width="98%">
      <div id="ticketDiv">
        <iframe id="ticketframe" :src="ticketurl" frameborder="0"></iframe>
      </div>
    </el-dialog>
    <!--展位预订  -->
    <el-dialog :visible.sync="bookDialogVisible" :close-on-press-escape="false" width="98%" height="1000px">
      <div class="imRate-wrapper">
        <div class="main">
          <p class="title" style="align: left">感谢您对我们展会的支持</p>
          <p class="title" style="align: left">
            填写以下信息后，即有销售专员与您联系。
          </p>

          <el-form ref="formbook" :model="formbook" :rules="rules" label-width="100px">
            <el-row style="margin-top: 10px">
              <el-col :span="23">
                <el-form-item label="公司名称" prop="company">
                  <el-input v-model="formbook.company"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="23">
                <el-form-item label="联系人" prop="contacts">
                  <el-input v-model="formbook.contacts"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="23">
                <el-form-item label="职位" prop="post">
                  <el-input v-model="formbook.post"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="23">
                <el-form-item label="手机/微信" prop="mobile">
                  <el-input v-model="formbook.mobile"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="23">
                <el-form-item label="邮箱" prop="email">
                  <el-input v-model="formbook.email"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="23">
                <el-form-item label="公司产品" prop="product">
                  <el-input v-model="formbook.product"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="23">
                <el-form-item label="意向参展面积" label-width="120px" prop="area">
                  <el-input v-model="formbook.area"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="23">
                <el-form-item label="是否首次参展" label-width="120px">
                  <el-input v-model="formbook.firstFlag"></el-input>
                  <!-- <el-radio-group v-model="formbook.firstFlag">
                                    <el-radio :label=true>是</el-radio>
                                    <el-radio :label=false>否</el-radio>
                                </el-radio-group> -->
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="23">
                <el-form-item label="其他说明">
                  <el-input v-model="formbook.otherText"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>
          <el-button type="primary" class="submit-btn position-h-mid" @click="submitbook">确定</el-button>
        </div>
      </div>
    </el-dialog>
    <!-- 会议活动  -->
    <!--展位预订  -->
    <el-dialog :visible.sync="meetDialogVisible" :close-on-press-escape="false" width="98%">
      <div class="imRate-wrapper">
        <div class="main">
          <p class="title" style="align: left">感谢您对我们活动的支持</p>
          <p class="title" style="align: left">
            填写以下信息后，即有服务专员与您联系。
          </p>
          <el-form ref="formmeet" label-width="100px" :model="formmeet" :rules="meetrules">
            <el-row style="margin-top: 10px">
              <el-col :span="23">
                <el-form-item label="公司名称" prop="company">
                  <el-input v-model="formmeet.company"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="23">
                <el-form-item label="联系人" prop="contacts">
                  <el-input v-model="formmeet.contacts"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="23">
                <el-form-item label="职位" prop="post">
                  <el-input v-model="formmeet.post"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="23">
                <el-form-item label="手机/微信" prop="mobile">
                  <el-input v-model="formmeet.mobile"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="23">
                <el-form-item label="邮箱" prop="email">
                  <el-input v-model="formmeet.email"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="23">
                <el-form-item label="您所感兴趣的会议" prop="interest" label-width="150px">
                  <el-input v-model="formmeet.interest"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="23">
                <el-form-item label="参加人数" prop="peoplecount" label-width="120px">
                  <el-input v-model="formmeet.peoplecount"></el-input>
                </el-form-item>
              </el-col>
            </el-row>

            <el-row>
              <el-col :span="23">
                <el-form-item label="其他说明">
                  <el-input v-model="formmeet.otherText"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>
          <el-button type="primary" class="submit-btn position-h-mid" @click="submitmeet">确定</el-button>
        </div>
      </div>
    </el-dialog>
    <!-- 问题是否解决  -->
    <el-dialog :visible.sync="isSolveDialogVisible" :close-on-press-escape="false" width="70%" style="height: 300px">
      <span style="
          font-size: 16px;
          margin-top: 30px;
          margin-bottom: 30px;
          margin-left: 5px;
        ">问题是否解决:</span>
      <div></div>
      <el-radio style="font-size: 24px; margin-left: 30px; margin-top: 20px" v-model="isSolve" label="1">是</el-radio>
      <el-radio style="font-size: 24px" v-model="isSolve" label="2">否
      </el-radio>
      <div style="margin-top: 30px"></div>
      <el-button type="primary" class="submit-btn position-h-mid" @click="submitIsSolve">确定</el-button>
    </el-dialog>
    <!-- 历史通话信息 -->
    <el-dialog width="1000px" :visible.sync="isHistoryVisible" :close-on-press-escape="false">
      <div>
        <el-table :data="currTableData" row-key="id">
          <el-table-column label="坐席" prop="serverChatName" width="60px" />
          <el-table-column label="会话内容" prop="content" width="300px" />
          <el-table-column label="发送时间" prop="createTime" width="190px" :formatter="dateFormat" />
          <el-table-column label="会话类型" prop="contentType" width="100px" />
          <el-table-column label="发送者" prop="sender" width="100px" :formatter="typeSender" />
          <el-table-column label="接收者" prop="receiver" width="100px" :formatter="typeReceiver" />
        </el-table>
        <el-pagination class="fy" :total="total" background :page-sizes="[20, 36, 66, 96, 168, 336]"
          layout="total, sizes, prev, pager, next, jumper" @current-change="current_change"
          @size-change="handleSizeChange" />
        <!-- <div>
              <iframe ref="iframewebchat" id="webchat" :src="urlwebchat" frameborder="0" scrolling="no"></iframe>
            </div> -->
      </div>
    </el-dialog>
    <el-dialog width="1000px" :visible.sync="fileVisible" :close-on-press-escape="false">
      <div>
        <pdf ref="pdf" :src="pdfUrl">
        </pdf>
      </div>
    </el-dialog>

  </div>
</template>

<script>
import pdf from 'vue-pdf'
import moment from "moment";
import common_chat_emoji from './common_chat_emoji.vue';
import $ from 'jquery'
export default {
  components: {
    commonChatEmoji: common_chat_emoji,
    pdf,
  },
  props: {
    chatInfoEn: {
      required: true,
      type: Object,
      default: {
        inputContent: '', // 本次输入框的消息内容
        msgList: [], // 消息集合
      },
    },

    oprRoleName: {
      required: true,
      type: String,
      default: '',
    }, // 操作者名称；e.g. server:服务端、client:客服端
  },
  data() {
    return {
      pdfUrl: "",
      fileVisible: false,
      keyboardVisible: false,
      originalHeight: window.innerHeight,
      resizeTimeout: null,
      focusFlag: false,
      historyFlag: true,
      currTableData: [],
      tableData: [],
      total: 0,
      projId: '',
      currentPage: 1,
      total: 0,
      pagesize: 12,
      urlwebchat: "",
      isHistoryVisible: false,
      transFlag: true,
      fileList: [],
      accept: { type: String, default: '*' },
      test: '',
      params: {
        zoomVal: 1,
        left: 0,
        top: 0,
        currentX: 0,
        currentY: 0,
        flag: false,
      },
      pageTotal: 0,
      pageNo: 0,
      isSolveDialogVisible: false,
      isSolve: '1',
      pNo: 1,
      fShow: false,
      nShow: true,
      curQuesions: [],
      questions: [],
      meetrules: {
        company: [
          { required: true, trigger: 'blur', message: '请输入公司名称' },
        ],
        contacts: [
          { required: true, trigger: 'blur', message: '请输入联系人' },
        ],
        post: [{ required: true, trigger: 'blur', message: '请输入职位' }],
        mobile: [
          { required: true, trigger: 'blur', message: '请输入手机/微信' },
        ],
        email: [{ required: true, trigger: 'blur', message: '请输入邮箱' }],
        interest: [
          { required: true, trigger: 'blur', message: '请输入感兴趣的展会' },
        ],
        peoplecount: [
          { required: true, trigger: 'blur', message: '请输入参展人数' },
        ],
      },
      rules: {
        company: [
          { required: true, trigger: 'blur', message: '请输入公司名称' },
        ],
        contacts: [
          { required: true, trigger: 'blur', message: '请输入联系人' },
        ],
        post: [{ required: true, trigger: 'blur', message: '请输入职位' }],
        mobile: [
          { required: true, trigger: 'blur', message: '请输入手机/微信' },
        ],
        email: [{ required: true, trigger: 'blur', message: '请输入邮箱' }],
        product: [
          { required: true, trigger: 'blur', message: '请输入产品/服务' },
        ],
        area: [
          { required: true, trigger: 'blur', message: '请输入意向参展面积' },
        ],
        firstFlag: [
          { required: true, trigger: 'blur', message: '请输入是否首次参展' },
        ],
      },
      meetDialogVisible: false,
      bookDialogVisible: false,
      ticketurl: 'https://ali6.infosalons.com.cn/reg/TCT22/registercn/login',
      ticketDialogVisible: false,
      // registerurl:"https://www.tctasia.cn/guanzhong_yzzs.shtml",
      registerurl: 'https://ali6.infosalons.com.cn/reg/TCT22/registercn/login',
      rateDialogVisible: false,
      registerDialogVisible: false,
      resultVisible: false, // 满意度已提交
      dataForm: {
        score: null, // 选中的item
        remark: '',
      },
      formbook: {
        projId: '',
        company: '', //公司名称
        contacts: '', //联系人
        post: '', //职位
        mobile: '', //手机/微信
        email: '', //邮箱
        product: '', //产品/服务
        area: '', //面积
        firstFlag: '', //是否首次参展
        otherText: '', //其他
      },
      formmeet: {
        projId: '',
        company: '', //公司名称
        contacts: '', //联系人
        post: '', //职位
        mobile: '', //手机/微信
        email: '', //邮箱
        interest: '', //感兴趣的会议
        peoplecount: '', //人数
        otherText: '', //其他
      },
      chatCall: false,
      manuShow: true,
      inputContent_setTimeout: null, // 输入文字时在输入结束才修改具体内容
      selectionRange: null, // 输入框选中的区域
      shortcutMsgList: [], // 聊天区域的快捷回复列表
      imgViewDialogVisible: false, // 图片查看dialog的显示
      imgViewDialog_imgSrc: '', // 图片查看dialog的图片地址
      chatLoaded: false, // chat是否已加载完毕
    };
  },
  watch: {},
  mounted() {
    this.$nextTick(function () {
      this.$data.chatLoaded = true;
      this.init();
      this.shown();
      this.projId = 1
      var formData = { projId: this.projId };

      // pageTotal
      this.$http.post({
        url: 'https://www.wanxinleasing.com:9005/backend2/api/comProb/getPageTotal',
        // url: 'http://localhost:62031/api/comProb/getPageTotal',
        params: formData,
        //  url: 'http://180.168.223.243:19001/api/comProb/getPageTotal',
        successCallback: (rs) => {
          console.log('rss');
          console.log(rs);
          this.pageTotal = rs;
        },
      });

      // var userAgent = navigator.userAgent || navigator.vendor || window.opera;
      // console.log(userAgent,"userAgent")
      // var isAndroid= userAgent.match(/android/i);
      // console.log(isAndroid,"isAndroid")
      // if(isAndroid==true){
      //    alert("capture,camera")
      //  let up = document.getElementById('common_chat_opr_fileUpload');
      //  up.setAttribute('capture', 'camera');
      // }

      // let up = document.getElementById('common_chat_opr_fileUpload');
      // up.setAttribute('accept', 'image/*'); // 只允许选择图片文件
      // up.removeAttribute('capture'); // 移除 capture 属性以避免调用摄像头
      // console.log(up, "up")
      this.originalHeight = window.innerHeight;

    });

    this.showHistory()
  },

  methods: {
    doBussiness(val) {
      console.log(val)
      this.sendBuss(val)
    },
    browsePdf(fileUrl) {
      debugger
      fileUrl = fileUrl.replace("http://192.168.0.124:8099/", "/backend2/")
      console.log("fileUrl", fileUrl)
      this.pdfUrl = fileUrl
      this.fileVisible = true
    },
    fomatDate(date) {
      if (date == undefined || date == "") {
        return " ";
      }
      return moment(date).format("YYYY-MM-DD HH:mm:ss");
    },
    current_change: function (currentPage) {
      this.currentPage = currentPage;
      this.queryData();
    },
    handleSizeChange: function (pageSize) {
      this.pagesize = pageSize;
      this.queryData();
    },
    queryData() {
      this.currTableData = this.tableData.slice(
        (this.currentPage - 1) * this.pagesize,
        this.currentPage * this.pagesize
      );
    },
    typeSender: function (row, column) {
      var type = row.sender;
      if (type == "agent") {
        return "坐席";
      } else if (type == "client") {
        return "客户";
      } else if (type == "robot") {
        return "机器人";
      } else {
        return "";
      }
    },
    typeReceiver: function (row, column) {
      var type = row.receiver;
      console.log(type, "type");
      if (type == "agent") {
        return "坐席";
      } else if (type == "client") {
        return "客户";
      } else if (type == "robot") {
        return "机器人";
      } else {
        return "";
      }
    },
    dateFormat: function (row, column) {
      var date = row[column.property];
      if (date == undefined || date == "") {
        return " ";
      }
      return moment(date).format("YYYY-MM-DD HH:mm:ss");
    },
    formatScore00: function (row, column) {
      switch (row.score) {
        case 5:
          return "非常满意";
        case 4:
          return "满意";
        case 3:
          return "一般";
        case 2:
          return "不满意";
        case 1:
          return "非常不满意";
        default:
          return "";
      }
    },
    showHistory() {
      console.log("showHistory")
      var phoneNum = this.$parent.phone
      var formData = {
        phoneNum: "15156044550"
      };
      this.$http.post({
        url: 'https://www.wanxinleasing.com:9005/backend2/api/WebChat/getChatByPhone',
        params: formData,
        successCallback: (rs) => {
          console.log('rss');
          console.log(rs);
          var table = rs
          table.sort((a, b) => a.id - b.id);
          this.tableData = table
          this.total = rs.length
          this.queryData();

          for (var i = 0; i < this.total; i++) {
            var x = this.tableData[i]
            // console.log(x, "x")
            var data = {}
            if (x.contentType == 'image') {
              data = {
                role: x.sender,
                avatarUrl: "static/image/im_client_avatar.png",
                contentType: x.contentType,
                content: x.content,
                fileUrl: x.fileUrl,
                createTime: moment(x.createTime).format("YYYY-MM-DD HH:mm:ss")

              }
            } else if (x.contentType == 'file') {
              data = {
                role: x.sender,
                avatarUrl: "static/image/im_client_avatar.png",
                contentType: x.contentType,
                content: x.content,
                fileUrl: x.fileUrl,
                createTime: moment(x.createTime).format("YYYY-MM-DD HH:mm:ss")

              }
            }
            else {
              data = {
                role: x.sender,
                avatarUrl: "static/image/im_client_avatar.png",
                contentType: x.contentType,
                content: x.content,
                createTime: moment(x.createTime).format("YYYY-MM-DD HH:mm:ss")
              }
            }

            // console.log(data, "data")
            this.$emit('addChatMsg', data);
          }


          // this.isHistoryVisible = true;
        }
      })
      this.historyFlag = false;
      // this.urlwebchat = "http://192.168.0.39:11060/#/workorder/webchat/?phoneNo=" + phoneNum

    },
    beforeUnmount() {
      //或者beforeUnmount
      window.removeEventListener("resize", this.handleResize);
    },
    beforeUpload(file) {
      console.log("file", file)
      console.log(this.fileList, "this.fileList")
      // if (file.size / 1024 / 1024 > 5) {
      //   this.$message.error({
      //     message: `上传文件大小不能超过5M!`,
      //   });
      //   return false;
      // }
      if (file.size / 1024 / 1024 > 2) {
        return new Promise((resolve, reject) => {
          const reader = new FileReader();
          reader.readAsDataURL(file);
          reader.onload = (e) => {
            const img = new Image();
            img.src = e.target.result;
            img.onload = () => {
              const canvas = document.createElement('canvas');
              const ctx = canvas.getContext('2d');
              canvas.width = 1024; // 设置压缩后图片的宽度
              canvas.height = 768; // 根据原始图片比例计算压缩后图片的高度
              ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
              canvas.toBlob((blob) => {
                const compressedFile = new File([blob], file.name, { type: file.type, lastModified: Date.now() });
                resolve(compressedFile);
              }, file.type);
            };
          };
        })
      }

    },
    uploadSucessFile(response, file, fileList) {
      console.log(response, "uploadSucessFile response======：");
      console.log(file, "uploadSucessFile file======：");
      console.log(fileList, "uploadSucessFile fileList======：");
      var fileName = file.name
      var data = {
        contentType: 'file',
        fileName: fileName,
        fileUrl: '/backend2/upload/' + file.response.data[0],
        state: 'success',
      }
      console.log("data_", data)
      this.sendMsg(data);
    },
    uploadSucessRe(response, file, fileList) {
      console.log(response, "response======：");
      console.log(file, "file======：");
      console.log(fileList, "fileList======：");
      var fileName = file.name
      var data = {
        contentType: 'image',
        fileName: fileName,
        fileUrl: '/backend2/upload/' + file.response.data[0],
        state: 'success',
      }
      console.log("data_", data)
      this.sendMsg(data);
    },
    handleFileUpload() {
      console.log("uuu")
      const file = this.$refs.fileInput.files[0];
      console.log(file, "file")
      this.$refs.fileInput.value = '';
      const reader = new FileReader();
      reader.onload = () => {
        console.log(file);
        const fileData = {
          name: file.name,
          type: file.type,
          size: file.size,
          preview: reader.result,
          poster: '',
          lastModified: file.lastModified,
          file: file,
          isEdit: true,
          fileSuffix: file.type,
        };
        console.log(fileData);
        const fileType = this.isImageOrVideo(file.type);
        if (fileType === 'video' && file.size > 300 * 1024 * 1024) {
          return this.$toast.info('选择文件超过限制大小');
        }
        console.log(fileData, "fileData")


        let formData = new FormData();
        formData.append(
          'uploadFile',
          file
        );
        this.$http.uploadFile({
          // url: 'http://47.100.176.161/api/File/upload',
          url: 'https://www.wanxinleasing.com:9005/backend2/api/File/upload',
          params: formData,
          successCallback: (rs) => {
            console.log('rs1');
            console.log(rs);
            this.sendMsg({
              contentType: fileType,
              fileName: file.name,
              // fileUrl: 'http://47.100.176.161/upload/' + rs[0],
              fileUrl: '/backend2/upload/' + rs[0],
              state: 'success',
            });
          },
        });
      };

      if (file) {
        reader.readAsDataURL(file);
      }
    },
    deleteFile(index) {
      this.files.splice(index, 1);
    },
    isImageOrVideo(filename) {
      if (!filename) return;
      let imageExtensions = ['jpg', 'jpeg', 'png', 'gif'];
      let videoExtensions = ['mp4', 'mov', 'avi', 'mkv', 'quicktime'];
      let ext = filename.split('/')[1].split('.').pop().toLowerCase();
      if (imageExtensions.includes(ext)) {
        return 'image';
      } else if (videoExtensions.includes(ext)) {
        return 'video';
      } else {
        return 'file';
      }
    },
    downloadFile00(fileUrl) {
      console.log(fileUrl, "fileUrl")
      window.postMessage({ type: 'download', url: '/backend2/upload/' + fileUrl }, '*');
      var fileName = fileUrl;
      // var x = "http://192.168.3.220:8013/records/" + fileName;
      var x = '/backend2/upload/' + fileName;
      fetch(x)
        .then((res) => res.blob())
        .then((blob) => {
          const a = document.createElement("a");
          document.body.appendChild(a);
          a.style.display = "none";
          // 使用获取到的blob对象创建的url
          const url = window.URL.createObjectURL(blob);
          a.href = url;
          // 指定下载的文件名
          a.download = fileName;
          a.click();
          document.body.removeChild(a);
          // 移除blob对象的url
          window.URL.revokeObjectURL(url);
        });
    },

    downloadFile: function (t) {
      console.log(t, "fileUrl"),
        window.postMessage({
          type: "download",
          url: "/backend2/upload/" + t
        }, "*");
      var e = t;
      fetch("/backend2/upload/" + e).then(function (t) {
        return t.blob()
      }).then(function (t) {
        var a = document.createElement("a");
        document.body.appendChild(a),
          a.style.display = "none";
        var n = window.URL.createObjectURL(t);
        a.href = n,
          a.download = e,
          a.click(),
          document.body.removeChild(a),
          window.URL.revokeObjectURL(n)
      })
    },
    handleInputChange() {
      this.getCamera();
    },
    async getCamera() {
      const fileName = this.$refs.camera.value;
      var extend = fileName.substring(fileName.lastIndexOf('.') + 1);
      const file = this.$refs.camera.files[0];
      console.log("fileName:", fileName);
      console.log("file:", file);
      let formData = new FormData();
      formData.append(
        'uploadFile',
        file
      );
      this.$http.uploadFile({
        // url: 'http://47.100.176.161/api/File/upload',
        url: 'https://www.wanxinleasing.com:9005/backend2/api/File/upload',
        params: formData,
        successCallback: (rs) => {
          console.log('rs1');
          console.log(rs);
          this.sendMsg({
            contentType:
              ['png', 'jpg', 'jpeg', 'gif', 'bmp'].indexOf(extend) >= 0
                ? 'image'
                : 'file',
            fileName: fileName,
            // fileUrl: 'http://47.100.176.161/upload/' + rs[0],
            fileUrl: '/backend2/upload/' + rs[0],
            state: 'success',
          });
        },
      });
      // let blob = new Blob(file); // 返回的文件流数据
      // let url = window.URL.createObjectURL(blob); // 将他转化为路径
      // this.imgSrc = await this.fileToBase64(file);
    },
    fileToBase64(file) {
      return new Promise((resolve, reject) => {
        // 创建一个新的 FileReader 对象
        const reader = new FileReader();
        // 读取 File 对象
        reader.readAsDataURL(file);
        // 加载完成后
        reader.onload = function () {
          // 将读取的数据转换为 base64 编码的字符串
          const base64String = reader.result.split(",")[1];
          // 解析为 Promise 对象，并返回 base64 编码的字符串
          resolve(base64String);
        };

        // 加载失败时
        reader.onerror = function () {
          reject(new Error("Failed to load file"));
        };
      });
    },
    bbimg() {
      console.log('bbimg');
      //图片放大缩小
      let e = e || window.event;
      this.params.zoomVal += e.wheelDelta / 1200;
      if (this.params.zoomVal >= 0.2) {
        this.test = `transform:scale(${this.params.zoomVal});`;
      } else {
        this.params.zoomVal = 0.2;
        this.test = `transform:scale(${this.params.zoomVal});`;
        return false;
      }
    },
    showSatisfy() {
      this.rateDialogVisible = true;
    },
    submitIsSolve() {
      // this.$emit('submitSolve', { isSolve: this.isSolve });
      var formData = {
        clientChatId: this.$parent.clientChatEn.clientChatId,
        isSolve: this.isSolve,
      };

      this.$http.post({
        url: '/backend2/api/WebChat/addIsSolve',
        params: formData,
        successCallback: (rs) => {
          console.log('rss');
          console.log(rs);
        },
      });

      //问题是否解决提交按钮
      // var formData={isSolve:this.isSolve}
      // this.$http.post({
      //     url: 'http://180.168.223.243:19003/api/WebChat/addIsSolve',
      //     params: formData,
      //     successCallback: (rs) => {
      //       console.log("rss")
      //       console.log(rs)
      //     },
      // });
      // this.$router.go(-1);

      // location.href =
      //   'https://ali6.infosalons.com.cn/reg/TCT22/registercn/index';
      // window.opener = null;
      // window.open('about:blank', '_top').close();
      // WeixinJSBridge.call('closeWindow');
      this.$router.go(-1);
      // var userAgent = navigator.userAgent;
      // if (
      //   userAgent.indexOf('Firefox') != -1 ||
      //   userAgent.indexOf('Chrome') != -1
      // ) {
      //   undefined;
      //   //  window.open('','_self').close()
      //   window.location.href = 'about:blank';
      // } else {
      //   window.close();
      // }
      this.isSolveDialogVisible = false;
    },
    closeChat() {
      //结束会话

      // this.$router.go(-1);
      if (this.chatCall == false) {
        //没有转人工
        this.isSolveDialogVisible = true;
      } else {
        this.rateDialogVisible = true;
        //满意度
      }
    },
    showf() {
      this.curQuesions = [];
      if (this.pNo > 1) {
        this.pNo = this.pNo - 1;
        this.curQuesions = [];
        for (var i = (this.pNo - 1) * 5; i < this.pNo * 5; i++) {
          this.curQuesions.push(this.questions[i]);
        }
      }
      if (this.pNo == 1) {
        this.fShow = false;
      }
      this.nShow = true;
    },
    shown() {
      if (this.pageTotal == this.pageNo) {
        this.pageNo = 0;
      }
      var userInfoSpan = $("#userInfoSpan").html();
      console.log("userInfoSpan", userInfoSpan)
      //userInfoSpan:userName + "," + this.userType + "," + this.idcard + "," + this.phone + "," + this.uId
      var customPhone = userInfoSpan.split(',')[3];
      this.pageNo = this.pageNo + 1;
      this.projId = 1
      var isChannel = "2"; //1有承接渠道 ，2没有承接渠道
      var postData = { customPhone: "15156044550" }
      console.log("postData", postData)
      this.$http.post({
        url: 'https://www.wanxinleasing.com:9005/backend2/api/SPService/getIsChannelByCustomPhone',
        params: postData,
        successCallback: (rs) => {
          console.log('rss');
          console.log(rs);
          isChannel = rs[0][0]
          console.log(isChannel, "isChannel")
        }
      })
      var formData = { pageNo: this.pageNo, projId: this.projId, isChannel: isChannel };
      console.log(formData, "formData");
      this.$http.post({
        url: 'https://www.wanxinleasing.com:9005/backend2/api/comProb/getListByNo',
        params: formData,
        successCallback: (rs) => {
          console.log('rss');
          console.log(rs);
          this.questions = rs;
          this.curQuesions = [];
          for (var i = 0; i < this.questions.length; i++) {
            this.curQuesions.push(rs[i]);
          }
          console.log('this.curQuestions');
          console.log(this.curQuesions);
        },
      });
    },
    tran(index) {
      //userName + "," + this.userType + "," + this.idcard + "," + this.phone + "," + this.uId
      console.log($("#userInfoSpan").html(), "userInfoSpan")
      var userInfoSpan = $("#userInfoSpan").html()
      console.log("userInfoSpan:", userInfoSpan)
      console.log("tran(index)=====:", index)

      debugger
      var content = '';
      var type = '';
      var keywords = ''
      for (var i = 0; i < this.questions.length; i++) {
        if (this.questions[i].id == index) {
          content = this.questions[i].content;
          type = this.questions[i].type;
          keywords = this.questions[i].keywords;
          break;
        }
      }
      if (content == '' || content == undefined) {
        return;
      }
      var userType = userInfoSpan.split(',')[1];
      if (userType == "未注册") {
        console.log(content, "content")
        console.log(keywords, "keywords")
        if (keywords == "如何下载WX易享车APP?") {
          content = '【温馨提示】客户您好，如果您的手机是安卓系统:请通过华为应用市场搜索"易享车"进行安装。苹果手机I0S系统:请点击 https://testflight.apple.com/join/5du0Gs8 链接下载TestFlight经行下载”WX易享车"App';
        } else {
          content = "【温馨提示】客户您好，当前系统查询不到您的信息。请您使用签约手机号下载WX易享车APP，进行实名认证。确认完成后即刻解锁此项查询功能。";
        }
      }
      var formData = {
        clientChatId: this.$parent.clientChatEn.clientChatId,
        content: content,
        projId: this.projId,
      };
      this.$http.post({
        url: '/backend2/api/WebChat/addByComProb',
        //  url: 'http://180.168.223.243:19001//api/CallReport/setWebChatSatify',
        // url: 'http://localhost:62031/api/CallReport/setWebChatSatify',
        params: formData,
        successCallback: (rs) => {
          console.log('rss');
          console.log(rs);
        },
      });
      if (type == '2') {
        this.$emit('addChatMsg', {
          role: 'server',
          avatarUrl: 'static/image/im_client_avatar.png',
          contentType: 'questionAnswera',
          content: content,
        });
      } else if (type == '1') {
        this.$emit('addChatMsg', {
          role: 'server',
          avatarUrl: 'static/image/im_client_avatar.png',
          contentType: 'questionAnswer',
          content: content,
        });
      } else {
        this.$emit('addChatMsg', {
          role: 'server',
          avatarUrl: 'static/image/im_client_avatar.png',
          contentType: 'questionAnswer3',
          content: content,
        });
      }

      var self = this;
      self.goEnd();
    },

    setMan() {
      this.manuShow = true;
      this.chatCall = false;
      this.chatFlag = false;
    },
    meet() {
      this.meetDialogVisible = true;
    },
    submit() {
      var formData;
      if (
        (this.$parent.clientChatEn == null) |
        (this.$parent.clientChatEn == undefined)
      ) {
        formData = {
          clientChatId: '',
          score: this.dataForm.score,
          remark: this.dataForm.remark,
        };
      } else {
        formData = {
          clientChatId: this.$parent.clientChatEn.clientChatId,
          score: this.dataForm.score,
          remark: this.dataForm.remark,
        };
      }

      this.$http.post({
        url: '/backend2/api/CallReport/setWebChatSatify',
        //  url: 'http://180.168.223.243:19001//api/CallReport/setWebChatSatify',
        // url: 'http://localhost:62031/api/CallReport/setWebChatSatify',
        params: formData,
        successCallback: (rs) => {
          console.log('rss');
          console.log(rs);
        },
      });
      this.$emit('clientQuit');
      this.rateDialogVisible = false;
      setTimeout(() => {
        this.$router.go(-1);
      }, 2000);


    },
    submitmeet() {
      this.$refs['formmeet'].validate(async (valid) => {
        if (valid) {
          console.log(this.formmeet);
          this.formmeet.projId = this.projId;
          var formData = { MeetInfo: this.formmeet };
          this.$http.post({
            // url: 'http://180.168.223.243:19001/api/WebChat/addMeet',
            url: '/backend2/api/WebChat/addMeet',
            params: formData,
            successCallback: (rs) => {
              console.log('rss');
              console.log(rs);
            },
          });
          this.meetDialogVisible = false;
        }
      });
    },
    submitbook() {

      this.$refs['formbook'].validate(async (valid) => {
        if (valid) {
          this.formbook.projId = this.projId;
          var formData = { BoothInfo: this.formbook };
          this.$http.post({
            // url: 'http://180.168.223.243:19001/api/WebChat/addBook',
            url: '/backend2/api/WebChat/addBook',
            params: formData,
            successCallback: (rs) => {
              console.log('rss');
              console.log(rs);
            },
          });
          this.bookDialogVisible = false;
        } else {
          return false;
        }
      });
    },
    book() {
      this.bookDialogVisible = true;
    },
    register() {
      //   window.open('https://ali6.infosalons.com.cn/reg/TCT22/registercn/login','_blank')
      if (this.projId == 1) {
        //tct

        // this.registerurl =
        //   'https://ali6.infosalons.com.cn/reg/TCT22/registercn/login';
        this.registerurl = 'https://sourl.cn/3NQDNa';
        window.open(this.registerurl, '_blank')
        //this.registerDialogVisible = true;
      }
      if (this.projId == 2) {
        //pfa
        // this.registerurl = 'https://ali6.infosalons.com.cn/reg/pfa22mo/visitor/start.aspx';
        //this.registerurl='https://sourl.cn/tLbwBF'
        this.registerurl = 'https://sourl.cn/eFriRu'
        window.open(this.registerurl, '_blank')
      }
      if (this.projId == 3) {
        //dacf
        console.log("dacf")
        // this.registerurl = 'https://ali6.infosalons.com.cn/reg/dacf22/registercn/start_wx.aspx';
        this.registerurl = 'https://1163-pages.vnuexhibitions.com.cn/p/17ef9';
        window.open(this.registerurl, '_blank')
        //this.registerDialogVisible = true;
      }
      if (this.projId == 4) {
        //rt
        // this.registerurl =
        'https://ali6.infosalons.com.cn/reg/RNT22mo/registercn/start.aspx';
        this.registerurl = 'https://ali6.infosalons.com.cn/reg/rnt23/registercn/start.aspx?type=RNT-TRACE116-23';
        window.open(this.registerurl, '_blank')
        //this.registerDialogVisible = true;
      }

      if (this.projId == 5) {
        //DFCt
        console.log("dfc")
        this.registerurl = 'https://ali6.infosalons.com.cn/reg/dacf22/registercn/start_wx.aspx';
        window.open(this.registerurl, '_blank')
        //this.registerDialogVisible = true;
      }
    },
    ticket() {
      this.ticketDialogVisible = true;
    },
    rate() {
      this.rateDialogVisible = true;
    },
    setManuShow: function () {
      this.manuShow = true;
    },
    /**
     * 初始化
     * @param {Object} opts 可选对象
     */
    init: function (opts) {
      var self = this;
      // 初始化状态
      document.getElementById('common_chat_input').innerHTML = '';
      self.$refs.qqemoji.$data.faceHidden = true;

      // 在线状态
      if (this.chatInfoEn.state == 'on') {
        // 1.显示在输入框的内容
        setTimeout(function () {
          // 未断开获取焦点
          document.getElementById('common_chat_input').focus();
          self.setInputContentSelectRange();
          // 设置之前保存的输入框内容
          if (self.chatInfoEn.inputContent) {
            self.setInputDiv(self.chatInfoEn.inputContent);
          }
        }, 200);
      } else {
        document.getElementById('common_chat_input').blur();
      }

      // 2.滚动到底部
      this.$nextTick(function () {
        self.$refs.common_chat_main.scrollTop =
          self.$refs.common_chat_main.scrollHeight;
        document.getElementById('common_chat_input').focus();
      });
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
    /**
     * 发送文本
     */
    sendText: function () {
      var self = this;
      var o = self.$refs.chatContent;
      var c = o.innerHTML;
      console.log("c----------------------c", c)
      var content = c
        .replace(/<img .+?text=\"(.+?)\".+?>/g, '[$1]')
      // .replace(/<.+?>/g, '');
      console.log("content", content)
      if (content.length == '') {
        return;
      }
      content = content.replace(';', ',');

      var msgContent = content;
      document.getElementById('common_chat_input').innerHTML = '';
      self.setInputContentByDiv();
      debugger
      this.sendMsg({
        contentType: 'text',
        content: msgContent,
      });

      this.$emit('changeCurTime');
    },

    /**
     * 设置输入内容
     * 根据input输入框innerHTML转换为纯文本
     */
    setInputContentByDiv: function () {
      console.log('setInputContentByDiv');
      var self = this;
      var htmlStr = document.getElementById('common_chat_input').innerHTML;

      // 1.转换表情为纯文本：<img textanme="[笑]"/> => [笑]
      var tmpInputContent = htmlStr
        .replace(/<img .+?text=\"(.+?)\".+?>/g, '[$1]')
        .replace(/<.+?>/g, '');
      console.log('tmpInputContent');
      console.log(tmpInputContent);
      // 2.设置最长长度
      if (tmpInputContent.length > 500) {
        document.getElementById('common_chat_input').innerHTML = '';
        var value = tmpInputContent
          .substr(0, 499)
          .replace(/\[(.+?)\]/g, function (item, value) {
            return self.$refs.qqemoji.getImgByFaceName(value);
          });
        this.setInputDiv(value);
      }

      // 3.修改store
      this.chatInfoEn.inputContent = tmpInputContent;
    },

    /**
     * 设置input输入框内容
     * @param {String} vlaue 设置的值
     */
    setInputDiv: function (value) {
      console.log('setInputDiv');
      if (this.$data.selectionRange == null) {
        document.getElementById('common_chat_input').focus();
        return;
      }
      // 1.设置selectionRange
      if (window.getSelection) {
        window.getSelection().removeAllRanges();
        window.getSelection().addRange(this.$data.selectionRange);
      } else {
        this.$data.selectionRange && this.$data.selectionRange.select();
      }

      // 2.表情转换为img
      value = this.getqqemojiEmoji(value);

      // 3.聊天框中是否选中了文本，若选中文本将被替换成输入内容
      if (window.getSelection) {
        var sel, range;
        // IE9 and non-IE
        sel = window.getSelection();
        if (sel.getRangeAt && sel.rangeCount) {
          // 1)删除选中的文本(内容)
          range = sel.getRangeAt(0); // 获取鼠标选中的文本区域
          range.deleteContents(); // 删除选中的文本

          // 2)创建以输入内容为内容的DocumentFragment
          var elemnet;
          if (range.createContextualFragment) {
            elemnet = range.createContextualFragment(value);
          } else {
            // 以下代码等同createContextualFragment
            // 创建一个DocumentFragment
            elemnet = document.createDocumentFragment();

            var divEl = document.createElement('div');
            divEl.innerHTML = value;
            // divEl下的元素，依次插入到DocumentFragment
            for (let i = 0, len = divEl.children.length; i < len; i++) {
              elemnet.appendChild(divEl.firstChild);
            }
          }
          // 3)选中文本的位置替换为新输入的内容，并把光标定位到新内容后方
          var lastNode = elemnet.lastChild;
          range.insertNode(elemnet);
          range.setStartAfter(lastNode);
          sel.removeAllRanges();
          sel.addRange(range);
        }
      } else if (document.selection && document.selection.type != 'Control') {
        // IE < 9
        document.selection.createRange().pasteHTML(imgStr);
      }
      console.log('表情转换为img======:', value);

      // 4.修改inputContent
      this.setInputContentByDiv();
    },

    /**
     * 转换为QQ表情
     */
    getqqemojiEmoji: function (value) {
      // console.log('getqqemojiEmoji');
      if (value == undefined) {
        return;
      }
      var self = this;
      let rs = value.replace(/\[(.+?)\]/g, function (item, value) {
        return self.$refs.qqemoji.getImgByFaceName(value);
      });
      // console.log("getqqemojiEmoji转换为QQ表情=================:", rs);
      return rs;
    },

    /**
     * 设置input输入框的选择焦点
     */
    setInputContentSelectRange: function () {
      // console.log("setInputContentSelectRange")
      if (window.getSelection && window.getSelection().rangeCount > 0) {
        var selectRange = window.getSelection().getRangeAt(0);
        if (
          selectRange.commonAncestorContainer.nodeName == '#text' &&
          selectRange.commonAncestorContainer.parentElement &&
          selectRange.commonAncestorContainer.parentElement.id ==
          'common_chat_input'
        ) {
          // 选中了输入框内的文本
          this.$data.selectionRange = selectRange;
        } else if (
          selectRange.commonAncestorContainer.id == 'common_chat_input'
        ) {
          // 选中了输入框
          this.$data.selectionRange = selectRange;
        }
      }
    },

    /**
     * 输入框的mouseup
     */
    inputContent_mouseup: function (e) {
      //console.log("setInputContentSelectRange")
      this.setInputContentSelectRange();
    },
    focusoff() {
      console.log("focusoff")
      this.focusFlag = false
      this.keyboardVisible = false;
      window.removeEventListener('resize', this.handleResize)
    },
    focuson(e) {
      console.log("focuson")
      this.focusFlag = true
      this.keyboardVisible = true;
      window.addEventListener('resize', this.handleResize)
    },
    handleResize() {
      clearTimeout(this.resizeTimeout);
      this.resizeTimeout = setTimeout(() => {
        const currentHeight = window.innerHeight;
        if (currentHeight < this.originalHeight) {
          this.keyboardVisible = true;
        } else {
          this.keyboardVisible = false;
        }
      }, 100);
    },
    /**
     * 输入框的keydown
     */
    inputContent_keydown: function (e) {
      //console.log("setInputContentSelectRange")
      // keyup触发时，绑定的数据还没有被变更，需要进行延后访问
      this.focusFlag = true
      clearTimeout(this.$data.inputContent_setTimeout);
      this.$data.inputContent_setTimeout = setTimeout(() => {
        this.setInputContentByDiv();

        // 若按了回车，直接发送
        if (e.keyCode == 13) {
          this.sendText();
        }
        this.setInputContentSelectRange();
      }, 1);
    },

    /**
     * 输入框的粘贴
     */
    inputContent_paste: function (e) {
      var self = this;
      var isImage = false;
      if (e.clipboardData && e.clipboardData.items.length > 0) {
        // 1.上传图片
        for (var i = 0; i < e.clipboardData.items.length; i++) {
          var item = e.clipboardData.items[i];
          if (item.kind == 'file' && item.type.indexOf('image') >= 0) {
            // 粘贴板为图片类型
            var file = item.getAsFile();
            let formData = new FormData();
            formData.append('uploadFile', file);
            this.$http.uploadFile({
              // url: 'http://180.168.223.243:19001/api/File/upload',
              url: 'https://www.wanxinleasing.com:9005/backend2/api/File/upload',
              params: formData,
              successCallback: (rs) => {
                console.log('rs');
                console.log(rs[0]);
                document.getElementById('common_chat_opr_fileUpload').value =
                  '';
                this.sendMsg({
                  contentType: 'image',
                  fileName: rs[0],
                  // fileUrl: ' http://180.168.223.243:19001/upload/' + rs[0],
                  fileUrl: ' /backend2/upload/' + rs[0],
                  // fileUrl: 'http://192.168.3.220:8011'+ rs[0],

                  state: 'success',
                });
              },
            });
            isImage = true;
          }
        }

        // 2.非图片，粘贴纯文本
        if (!isImage) {
          var str = e.clipboardData.getData('text/plain');
          // 转化为纯文字
          var span = document.createElement('span');
          span.innerHTML = str;
          var txt = span.innerText;
          this.setInputDiv(
            txt
              .replace(/\n/g, '')
              .replace(/\r/g, '')
              .replace(/</g, '&lt;')
              .replace(/>/g, '&gt;')
          );
        }
      }
      e.stopPropagation();
      e.preventDefault();
    },

    /**
     * 文件上传_点击
     */
    fileUpload_click: function (fileType) {
      document.getElementById('common_chat_opr_fileUpload').onchange =
        this.fileUpload_change;
      document.getElementById('common_chat_opr_fileUpload').click();
    },

    /**
     * 文件上传_选中文件
     */
    fileUpload_change: function (e) {
      console.log("estart", e)
      console.log("document.querySelector1", document.querySelector('#common_chat_opr_fileUpload').value)
      var fileNameIndex =
        document
          .getElementById('common_chat_opr_fileUpload')
          .value.lastIndexOf('\\') + 1;
      var fileName = document
        .getElementById('common_chat_opr_fileUpload')
        .value.substr(fileNameIndex);
      var extend = fileName.substring(fileName.lastIndexOf('.') + 1);

      // if (extend == "jpg" || extend == "jpeg" || extend == "png" || extend == "bmp") {
      //   //TO DO
      // } else {
      //   alert("只能选择图片文件");
      //   return
      // }
      // // 1.判断有效
      // // 1)大小
      // console.log(document.getElementById('common_chat_opr_fileUpload').files[0].size,)
      // if (
      //   document.getElementById('common_chat_opr_fileUpload').files[0].size >=
      //   1000 * 1000 * 10
      // ) {
      //   console.log(">10mb")
      //   this.$ak.Msg.toast('文件大小不能超过10M', 'error');
      //   document.getElementById('common_chat_opr_fileUpload').value = '';
      //   //return false;
      // }
      console.log("file", document.getElementById('common_chat_opr_fileUpload').files[0])
      // 2.文件上传
      let formData = new FormData();
      formData.append(
        'uploadFile',
        document.getElementById('common_chat_opr_fileUpload').files[0]
      );
      this.$http.uploadFile({
        // url: 'http://47.100.176.161/api/File/upload',
        url: 'https://www.wanxinleasing.com:9005/backend2/api/File/upload',
        params: formData,
        successCallback: (rs) => {
          console.log('rs1');
          console.log(rs);
          document.getElementById('common_chat_opr_fileUpload').value = '';
          this.sendMsg({
            contentType:
              ['png', 'jpg', 'jpeg', 'gif', 'bmp'].indexOf(extend) >= 0
                ? 'image'
                : 'file',
            fileName: fileName,
            // fileUrl: 'http://47.100.176.161/upload/' + rs[0],
            fileUrl: '/backend2/upload/' + rs[0],
            state: 'success',
          });
          e.target.value = ""
          console.log(e, "eend")
          document.querySelector('#common_chat_opr_fileUpload').value = ''
          console.log("document.querySelector2", document.querySelector('#common_chat_opr_fileUpload').value)

        },
      });

    },
    /**
     * qqemoji选中表情
     */
    qqemoji_selectFace: function (rs) {
      console.log('qqemoji_selectFace=====：', rs);
      var imgStr = rs.imgStr;
      this.setInputDiv(imgStr);
      document.getElementById("btnSend").focus()
    },
    /**
     * 转换文件名，若文件名称超过9个字符，将进行截取处理
     * @param {String} fileName 文件名称
     */
    getFileName: function (fileName) {
      if (!fileName) {
        return;
      }
      var i = fileName.lastIndexOf('/');
      var name = fileName.substring(i + 1, fileName.lastIndexOf('.'));
      var extend = fileName.substring(fileName.lastIndexOf('.') + 1);
      if (name.length > 9) {
        name = name.substring(0, 3) + '...' + name.substring(name.length - 3);
      }
      return name + '.' + extend;
    },
    /**
     * 图片查看dialog_显示
     */
    imgViewDialog_show: function (item) {
      this.$data.imgViewDialogVisible = true;
      this.$data.imgViewDialog_imgSrc = item.fileUrl;
    },

    /**
     * 图片查看dialog_显示
     */
    imgViewDialog_close: function () {
      this.$data.imgViewDialogVisible = false;
      var self = this;
      setTimeout(function () {
        self.$data.imgViewDialog_imgSrc = '';
      }, 100);
    },

    /**
     * 输入框的拖拽
     */
    inputContent_drop: function (e) {
      var self = this;
      setTimeout(function () {
        self.setInputContentByDiv();
      }, 100);
    },
    sendBuss: function (msg) {
      var self = this;
      debugger
      if (msg == 2) {
        var d = new Date();
        var h = d.getHours();
        if (h >= 9 && h < 19) {
          // if ((h >= 0)) {
          console.log("h >= 10 && h <19")
          this.$emit('sendBuss', msg);
        } else {
          console.log("人工客服时间：工作日10:00-19:00，请见谅。")
          this.$emit('addChatMsg', {
            role: 'server',
            avatarUrl: 'static/image/im_client_avatar.png',
            contentType: 'text',
            content: '客户您好，当前并非【人工客服】工作时间，请您在工作日上午10点进行咨询办理',
          });
        }
      } else if (msg == 4) {
        var d = new Date();
        var h = d.getHours();
        // if ((h >= 9 && h <= 11) || (h>=13 && h<=23)) {
        if ((h >= 0)) {
          console.log("h >= 10 && h <19")
          this.$emit('sendBuss', msg);
        } else {
          console.log("人工客服时间：工作日10:00-19:00，请见谅。")
          this.$emit('addChatMsg', {
            role: 'server',
            avatarUrl: 'static/image/im_client_avatar.png',
            contentType: 'text',
            content: '客户您好，很抱歉给您带来不良体验，请您留言反馈您的异议问题或在工作时间咨询人工客服4008639066',
          });
        }
      } else {
        this.$emit('sendBuss', msg);
      }



    },
    /**
     * 发送消息，e.g. 文本、图片、文件
     * @param {Object} msg 消息对象
     */
    sendMsg: function (msg) {
      console.log("sendMsg====", msg)
      var self = this;
      // 1.传递
      this.$emit('sendMsg', {
        msg: msg,
        successCallbcak: function () {
          document.getElementById('common_chat_input').focus();
          self.goEnd();
        },
      });
    },

    /**
     * 传递回调
     */
    chatCallback: function (emitType, data) {
      this.chatCall = true;
      var d = new Date();
      var h = d.getHours();
      console.log("chatCallback")
      console.log(h);
      if (h >= 9 && h < 17) {
        // if ((h >= 9 && h <= 11) || (h>=13 && h<=23)) {
        // if ((h >= 0)) {
        console.log("h >= 9 && h <17")
        this.manuShow = false;
        this.$emit('chatCallback', {
          eventType: emitType,
          data: data,
        });
      } else {
        console.log("人工客服时间：工作日9:00-19:00，请见谅。")
        this.$emit('addChatMsg', {
          role: 'server',
          avatarUrl: 'static/image/im_client_avatar.png',
          contentType: 'text',
          content: '人工客服时间：工作日9:00-19:00，请见谅。',
        });
      }
      this.transFlag = false;
    },
    sendMsgAgent: function (msg) {
      this.sendMsg({
        contentType: 'text',
        content: msg,
      });
    },
    /**
     * 聊天记录滚动到底部
     */
    goEnd: function () {
      this.$nextTick(() => {
        setTimeout(() => {
          this.$refs.common_chat_main.scrollTop =
            this.$refs.common_chat_main.scrollHeight;
        }, 100);
      });
    },
  }
}


</script>
<style lang="less">
#webchat {
  width: 400px;
  height: 900px;
}

.el-table .cell {
  line-height: 12px !important
}

.zoomable-image {
  max-width: 100%;
  height: auto;
  user-select: none;
}

.el-upload-list--picture-card {
  display: none !important;
}

.el-upload-list {

  display: none !important;
}

.el-row {
  height: 60px;
}

.el-form-item {
  margin-bottom: 5px;
}

.common_chat-wrapper {
  width: 100%;
  height: 100%;
  overflow: hidden;
  position: relative;
  font-size: 12px;
  float: left;
  border: 0px;

  .common_chat-inner {
    width: 100%;
    height: 100%;

    .common_chat-main {
      position: relative;
      height: calc(~'100% - 165px');
      overflow-y: auto;
      overflow-x: hidden;

      .common_chat-main-header {
        padding-top: 14px;
        text-align: center;

        .el-button {
          padding: 0px;
          font-size: 12px;
          color: #8d8d8d;
        }
      }

      .common_chat-main-content {
        position: absolute;
        width: 100%;
        height: 100%;

        &>.inner {
          padding-bottom: 20px;

          .item {
            clear: both;
            overflow: hidden;
          }

          .sys {
            color: #b0b0b0;
            font-size: 12px;
            text-align: center;

            .text-content {
              padding-top: 20px;
            }

            .myd-content {
              .desc {
                margin-top: 18px;
              }

              .text {
                color: #3e3e3e;
                margin-top: 12px;
              }

              .remark {
                margin-top: 10px;
              }
            }
          }

          .receiver,
          .sender {
            margin-top: 18px;
            font-size: 12px;

            .avatar-wrapper {
              float: left;

              .kf-img {
                width: 40px;
                height: 40px;
              }
            }

            .info-wrapper {
              position: relative;
              text-align: left;
              font-size: 12px;

              .item-content {
                position: relative;
                max-width: 340px;
                color: #3e3e3e;
                font-size: 13px;
                border-radius: 3px;

                .phead {
                  margin-top: 10px;
                  margin-bottom: 20px;
                  color: #8d8d8d;
                  font-size: 14px;
                }

                .pquestion {
                  font-size: 14px;
                  margin-top: 5px;
                  width: 100%;
                  padding-bottom: 10px;
                  border-bottom: 1px solid rgb(212, 210, 210);
                }

                .text0 {
                  line-height: 1.2;
                  white-space: normal;
                  word-wrap: break-word;
                  word-break: break-all;
                  padding: 5px 6px;
                }

                .text {
                  line-height: 1.8;
                  white-space: normal;
                  word-wrap: break-word;
                  word-break: break-all;
                  padding: 10px 12px;
                }

                .qqemoji {
                  width: 24px;
                  height: 24px;
                }

                .img {
                  max-width: 320px;
                  max-height: 240px;
                  white-space: normal;
                  word-wrap: break-word;
                  word-break: break-all;
                  padding: 5px;
                  cursor: pointer;
                }

                .file {
                  width: 220px;
                  padding: 10px 8px;
                  margin: 3px;
                  overflow: hidden;
                  background: #fff;
                  border-radius: 5px;

                  .el-button {
                    padding: 0px;
                    font-size: 12px;
                  }

                  .file-info {
                    float: left;
                    padding: 0px 8px;

                    .file-name {
                      width: 160px;
                      display: inline-block;
                      color: #333333;
                      white-space: nowrap;
                      text-overflow: ellipsis;
                      overflow: hidden;
                      line-height: 1.3;
                    }
                  }

                  .file-opr {
                    margin-top: 8px;
                  }

                  .file-icon {
                    float: left;
                    color: #663399;
                    font-size: 40px;
                  }

                  .file-download {
                    color: #00a8d7;
                    cursor: pointer;
                    text-decoration: blink;
                  }
                }

                .preInput {
                  position: relative;
                  color: #8d8d8d;

                  img {
                    height: 15px;
                    position: relative;
                    top: 3px;
                  }
                }

                .issueList {
                  width: 250px;
                  padding: 10px;

                  .title {
                    position: relative;

                    .content {
                      position: absolute;
                      margin-top: -1px;
                      margin-left: 6px;
                    }
                  }

                  .el-collapse-item__wrap {
                    background: transparent;
                  }

                  .el-collapse {
                    border: 0px;
                    margin-top: 8px;
                    margin-bottom: -8px;

                    .el-collapse-item__header {
                      font-size: 13px;
                      background: transparent;
                      color: #d12b1e;
                      padding-left: 5px;
                    }

                    .el-collapse-item__wrap {
                      .el-collapse-item__content {
                        font-size: 12px;
                        color: #3e3e3e;
                        padding-left: 5px;
                      }
                    }
                  }
                }

                .issueExtend {
                  width: 250px;
                  padding: 10px 10px 0px;

                  .main {
                    border-top: 1px solid #eeeff0;
                    margin-top: 10px;
                    padding-top: 10px;

                    p {
                      margin-bottom: 5px;
                    }

                    .el-button {
                      font-size: 12px;
                      color: #d12b1e;
                    }
                  }
                }

                .issueResult {
                  width: 250px;

                  .main {
                    padding: 10px;
                  }

                  .footer {
                    border-top: 1px solid #eeeff0;
                    height: 30px;

                    .btn {
                      width: 60px;
                      margin: 0px 30px;
                      padding: 6px 0px;
                      display: inline-block;
                      text-align: center;
                      font-size: 10px;
                      color: #8d8d8d;
                      cursor: pointer;
                      position: relative;

                      &:first-child::after {
                        top: 4px;
                        right: -30px;
                        width: 1px;
                        height: 80%;
                        content: '';
                        position: absolute;
                        background-color: #eeeff0;
                        z-index: 0;
                      }
                    }

                    .iconfont {
                      font-size: 10px;
                      margin-right: 5px;
                    }
                  }
                }
              }
            }
          }

          .item.receiver {
            margin-left: 5px;

            .avatar-wrapper {
              margin-right: 15px;
            }

            .info-wrapper {
              .item-content {
                float: left;
                color: #000000;
                background-color: #f9fbfc;
                border: 1px solid #ccc;

                &::before {
                  position: absolute;
                  top: -1px;
                  left: -10px;
                  width: 0px;
                  height: 0px;
                  content: '';
                  border-top: 0px;
                  border-right: 10px solid #ccc;
                  border-bottom: 5px solid transparent;
                  border-left: 0px;
                }
              }
            }
          }

          .item.sender {
            margin-right: 5px;

            .avatar-wrapper {
              float: right;
              margin-left: 15px;
            }

            .info-wrapper {
              float: right;

              .item-content {
                float: right;
                background: #0095ff;
                border: 1px solid #0095ff;
                color: #ffffff;

                &::before {
                  position: absolute;
                  top: -1px;
                  right: -10px;
                  width: 0px;
                  height: 0px;
                  content: '';
                  border-top: 0px;
                  border-right: 0px;
                  border-bottom: 5px solid transparent;
                  border-left: 10px solid #0095ff;
                }
              }
            }
          }
        }
      }
    }

    .common_chat-footer {
      position: relative;
      width: 100%;
      border-top: 1px solid #ccc;

      .opr-wrapper {
        // height: 2px;
        height: 30px;
        padding: 10px;
        text-align: left;

        &>.item {
          margin-right: 12px;
          float: left;
          font-weight: normal;
          text-decoration: blink;

          &>.iconfont {
            color: #aaa;
            font-size: 20px;
          }
        }
      }

      .input-wrapper {
        position: relative;
        padding: 2px 0px 0px 2px;

        .inputContent {
          width: 99%;
          padding: 2px;
          // height: 90px;
          height: 65px;
          resize: none;
          overflow: auto;
          line-height: 1.5;
          outline: 0px solid transparent;
        }

        .shortcutPopover-wrapper {
          position: absolute;
          top: 30px;
          left: 10px;
          width: 440px;
          max-height: 80px;
          padding: 4px;
          font-size: 12px;
          overflow-y: auto;
          border: 1px solid #9b9aab;
          border-radius: 3px;
          background-color: #fff;
          cursor: pointer;

          p {
            padding: 4px;

            &.selected {
              background-color: #ded1cc;
            }

            .key {
              display: inline-block;
              width: 50px;
              white-space: nowrap;
              text-overflow: ellipsis;
              overflow: hidden;
            }

            .content {
              display: inline-block;
              width: 350px;
              margin-left: 10px;
              white-space: nowrap;
              text-overflow: ellipsis;
              overflow: hidden;
            }

            .highlight {
              color: #00a8d7;
            }
          }
        }

        .tips {
          position: absolute;
          top: 7px;
          left: 20px;
          width: auto;
          color: #8d8d8d;
        }
      }

      .send-btn {
        float: right;
        margin-right: 16px;

        &.off,
        &.end {
          background-color: #ccc;
          border-color: #ccc;
        }
      }

      .off-wrapper {
        position: absolute;
        top: 0px;
        left: 0px;
        width: 100%;
        height: 100%;
        background-color: rgba(255, 255, 255, 0.6);
        font-size: 14px;

        .content {
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
        }
      }
    }
  }
}

.imgView-dialog {
  background: #00000080;


  .el-dialog {
    max-width: 100%;
    position: relative;
    top: 150px;
    background: transparent;
    box-shadow: none;

    .el-dialog__header {
      display: none;
    }

    .el-dialog__body {
      padding: 0px;
      text-align: center;
      position: relative;

      .header {
        text-align: right;
        position: relative;
        height: 0px;

        .fa-remove {
          font-size: 32px;
          color: white;
          position: relative;
          right: -50px;
          top: -30px;
          cursor: pointer;
        }
      }

      .main {
        .img {
          max-width: 100%;
          max-height: 100%;
          height: 100%;
        }
      }
    }
  }
}

.imRate-wrapper {
  height: 1000px;

  &>.main {
    overflow: hidden;

    .title {
      text-align: center;
      font-size: 14px;
      color: #000000;
      margin-top: 15px;
    }

    .el-rate {
      margin-top: 20px;
      text-align: center;
      margin-bottom: 36px;

      .el-rate__item {
        width: 18%;

        .el-rate__icon {
          font-size: 20px;
        }
      }

      .el-rate__text {
        display: block;
        margin-top: 16px;
      }
    }

    textarea {
      width: 95%;
      margin: 10px auto 0px;
    }

    .submit-btn {
      width: 100px;
      margin: 18px 0;
    }
  }

  &>.submit-main {
    .fa {
      display: table;
      margin: 85px auto 0px;
      color: #6bcc00;
      font-size: 50px;
    }

    .title {
      margin-top: 30px;
      font-size: 20px;
      text-align: center;
      color: #000000;
    }
  }
}

#registerframe {
  height: 600px;
  width: 100%;
}

#ticketframe {
  height: 600px;
  width: 100%;
}

.camera {
  width: 65px;
  height: 40px;
  overflow: hidden;
  font-size: 16px;
  position: relative;

  .txt {
    position: absolute;
    width: 100%;
    height: 100%;
    background-color: #e8e8e8;
  }

  .height-class {
    height: calc(~'100% - 365px');
  }

  // height: calc(~'100% - 165px');
}
</style>
