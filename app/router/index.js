import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path:'/',
    name:'home',
    component: () => import('../views/Home.vue'),
  },
  {
    path: '/dashboard/',
    name: 'dashboard',
    component: () => import('../views/Dashboard.vue'),
    redirect: '/dashboard/profile',
    children:[
      {
        path:'profile',
        name:'profile',
        component: ()=> import('../views/Profile.vue')
      },
      {
        path:'agents',
        name:'agents',
        component: ()=> import('../views/agents/Agents.vue'),
      },
      {
        path:'tools',
        name:'tools',
        component: ()=> import('../views/tools/Tools.vue')
      },
      {
        path:'integrations',
        name:'integrations',
        component: ()=> import('../views/Integrations.vue')
      },
      {
        path:'about',
        name:'about',
        component: ()=> import('../views/About.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
