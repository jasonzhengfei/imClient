import Vue from 'vue'
import Router from 'vue-router'
import imServer from '@/components/imServer/imServer'
import imLogin from '@/components/imServer/imLogin'

Vue.use(Router)

export default new Router({
    routes: [
        { path: '/', redirect: 'imServer' },
        { path: '/imServer', name: 'imServer', component: imServer },
        {path:'/imLogin',name:'imLogin',component:imLogin}

    ]
})