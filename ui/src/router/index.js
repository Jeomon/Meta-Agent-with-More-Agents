import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      redirect: '/chat',
    },
    {
      path:'/signup',
      name:'signup',
      component: ()=>import('../views/SignUp.vue')
    },
    {
      path:'/signin',
      name:'signin',
      component: ()=>import('../views/SignIn.vue')
    },
    {
      path: '/chat',
      name: 'chat',
      component: ()=>import('../views/Chat.vue')
    },
    {
      path: '/settings/',
      name: 'settings',
      component: ()=>import('../views/Settings.vue'),
      redirect: '/settings/profile',
      children:[
        {
          path:'profile',
          name:'profile',
          components:{
            content:()=>import('../views/Profile.vue')
          }
        },
        {
          path:'agents',
          name:'agents',
          components:{
            content:()=>import('../views/Agents.vue')
          }
        },
        {
          path:'tools',
          name:'tools',
          components:{
            content:()=>import('../views/Tools.vue')
          }
        },
        {
          path:'integrations',
          name:'integrations',
          components:{
            content:()=>import('../views/Integrations.vue')
          }
        },
        {
          path:'about',
          name:'about',
          components:{
            content:()=>import('../views/About.vue')
          }
        }
      ]
    }
  ]
})

export default router
