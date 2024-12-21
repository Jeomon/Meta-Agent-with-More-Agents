import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
    },
    {
      path: '/test',
      name: 'test',
      component: ()=>import('../views/Test.vue')
    },
    {
      path:'/signup',
      name:'signup',
      component: ()=>import('../views/SignUp.vue')
    },
    {
      path: '/signin',
      name: 'signin',
      component: ()=>import('../views/SignIn.vue'),
      beforeEnter: (to, from, next) => {
        console.log(to,from);
        if (store.state.isAuthenticated) {
          next({ name: 'home' });
        } else {
          next();
        }
      }
    },
    {
      path: '/signout',
      name: 'signout',
      beforeEnter: (to, from, next) => {
        if (store.state.isAuthenticated) {
          sessionStorage.removeItem('auth_token');
          next({ name: 'home' });
        } else {
          next();
        }
      },
      meta: { requiresAuth: true }
    },
    {
      path: '/chat',
      name: 'chat',
      component: ()=>import('../views/Chat.vue'),
      meta: { requiresAuth: true },
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
      ],
      meta: { requiresAuth: true },
    }
  ]
})

router.beforeEach((to, from, next) => {
  // Check if the route requires authentication
  const isAuthenticated = store.state.isAuthenticated;
  if (to.matched.some((record) => record.meta.requiresAuth)&&!isAuthenticated) {
    const path=encodeURIComponent(window.location.pathname)
    // Redirect to login if not authenticated
    next({ name: 'signin',query:{redirect:path} });
  } else {
    // Proceed to the route if no auth is required
    next();
  }
});

export default router
