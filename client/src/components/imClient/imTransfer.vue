<!-- 转接 -->
<template>
    <div class="imTransfer-wrapper">
        <main class="main">
            <el-radio-group v-model="selectedServerChatId" class="item-group">
                <div class="item" v-for="(item, index) in kfList" :key="index">
                    <el-radio-button :label="item.serverChatId">{{item.serverChatName}}</el-radio-button>
                </div>
            </el-radio-group>
        </main>
        <footer class="footer">
            <el-button type="primary" :disabled="selectedServerChatId == ''" @click="submit">开始咨询</el-button>
        </footer>
    </div>
</template>

<script>
import $ from 'jquery'
var ws = null
export default {

    data() {
        return {
            kfList: [], // 转人工队列集合
            selectedServerChatId: '' // 选中的serverChatId
        };
    },
    computed: {},
    watch: {},
    methods: {
        /**
         * init
         */
        init: function() {
            // this.$http.get({
            //     url: 'getIMServerList',
            //     successCallback: (res) => {
            //         console.log("res")
            //         console.log(res)
            //         this.$data.kfList = res;
            //     }
            // });



            // var jsonStr = '{"avatarUrl":"/static/image/im_server_avatar.png","serverChatId":"111","serverChatName":"aaa"}';
            // var jsonObj = $.parseJSON(jsonStr);
            // var a = new Array(2);
            // a[0] = jsonObj;
            // jsonStr = '{"avatarUrl":"/static/image/im_server_avatar.png","serverChatId":"222","serverChatName":"bbb"}';
            // jsonObj = $.parseJSON(jsonStr);
            // a[1] = jsonObj;



            // this.$data.kfList = a;

            ws.send("cmd@getServerChatEnList;type@client;cont@cont")
            //this.$data.selectedServerChatId = '';
        },

        /**
         * 队列dialog_提交
         */
        submit: function() {
            this.$emit('submit', {
                serverChatId: this.selectedServerChatId
            });
        },

        websocket() {
            ws.onopen = () => {

                ws.send("cmd@getServerChatEnList;type@client;cont@cont")

            }
            ws.onmessage = (evt) => {
                console.log("evtttt")
                console.log(evt.data)
                var data=evt.data;

                var serverChatEnList=data.split('@')
                this.kfList=[]
                console.log(serverChatEnList)
                var c='';
                for(var i=0;i<serverChatEnList.length;i++){
                    c=serverChatEnList[i]
                    c=c.replace(/'/g, '"')
                    console.log(c)
                    this.kfList.push(JSON.parse(c))
                    break;

                }
                this.selectedServerChatId=serverChatEnList[i].serverChatId
                 this.$emit('submit', {
                serverChatId: this.selectedServerChatId
            });
            }
            ws.onclose = function () {
                console.log('connection closed')
            }
      },
   
    },
    mounted() {
        // ws = new WebSocket('ws://47.116.135.132:7788')
        // ws=new WebSocket('ws://192.168.2.108:5679/ws')
        // ws=new WebSocket('ws://192.168.3.230:5679/ws')
        ws=new WebSocket('ws://192.168.0.38:9001/ws')
        this.websocket()}
};
</script>

<style lang="less">
    .imTransfer-wrapper {
        .main {
            height: 200px;
            border-bottom: 1px solid #ebeff3;
            .item {
                float: left;
                text-align: center;
                padding: 30px 21px 0px;
                .el-radio-button__inner {
                    display: inline-block;
                    width: 121px;
                    font-size: 14px;
                    color: #3e3e3e;
                    white-space: nowrap;
                    text-overflow: ellipsis;
                    border-radius: 5px;
                    overflow: hidden;
                }
                .el-radio-button.is-active {
                    .el-radio-button__inner {
                        color: #00a8d7;
                        background-color: #fff;
                    }
                }
            }
        }
        .footer {
            text-align: center;
            padding: 14px 0px;
        }
    }
</style>
