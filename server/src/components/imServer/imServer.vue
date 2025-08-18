<!-- im服务端入口 -->
<template>
  <div class="imServer-wrapper">
    <!-- <im-record ref="im_record" @select="setChatStatus" class="item im-record" ></im-record> -->
    <im-chat ref="im_chat" class="imServer-main"></im-chat>
  </div>
</template>

<script >
import imRecord from './imRecord.vue';
import imChat from './imChat.vue';

export default {
  components: {
    imRecord: imRecord,
    imChat: imChat,
  },
  data() {
    return {
      socket: null,
    };
  },
  
  computed: {
    storeSelectedChatEn() {
      return this.$store.imServerStore.getters.selectedChatEn;
    },
  },
  watch: {},
  methods: {
    setChatStatus: function (m) {
      console.log('mm');
      console.log(m);
    },
    /**
     * 选中了会话
     */
    selectedChat: function () {},
  },
  mounted() {

    //this.$store.imServerStore.commit("setChatName",this.$route.query.ChatName)
  },

  destroyed() {
    // this.$store.imServerStore.dispatch('SERVER_OFF');
  },
};
</script>

<style lang="less">
@import '../../common/css/base.less';


.imServer-wrapper {
  #common-wrapper();
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
    & > .item {
      float: left;
      border-right: 1px solid #e6e6e6;
      height: 100%;
    }
    & > .im-record {
      width: 220px;
    }
    & > .im-chat {
      width: calc(~'99% - 280px');
    }
  }
}
</style>
