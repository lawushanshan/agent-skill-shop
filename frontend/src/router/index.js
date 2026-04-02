/**
 * Vue Router 配置
 */
import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import SkillsHome from '../views/SkillsHome.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: SkillsHome
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/skills/:id',
    name: 'SkillDetail',
    component: () => import('../views/SkillDetail.vue')
  },
  {
    path: '/upload',
    name: 'UploadSkill',
    component: () => import('../views/UploadSkill.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/Profile.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫 - 检查登录状态
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
