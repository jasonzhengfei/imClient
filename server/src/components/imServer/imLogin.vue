<template>
    <div>
        <el-row :gutter="20">
            <el-col :span="8">
                <el-input v-model="userName" placeholder="请输入用户名"></el-input>
            </el-col>
            <el-col :span="4">
                <el-button type="primary" @click="login">登陆</el-button>
            </el-col>
        </el-row>
    </div>

</template>

<script>

    export default {
        data() {
            return {
                userName: ''
        }
    },
    methods:{
        login:function(){
            this.$store.imServerStore.commit("setChatName",this.userName)
            this.$router.push('/imServer')
        }
    }
    }
</script>