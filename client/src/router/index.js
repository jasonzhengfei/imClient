import Vue from 'vue'
import Router from 'vue-router'

import imClient from '@/components/imClient/imClient'


Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/', redirect: 'imClient',
          
        },

        {
            path: '/imClient', name: 'imClient', component: imClient,
           
        },


    ]
})