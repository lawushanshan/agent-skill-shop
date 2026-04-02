<template>
  <a-config-provider :theme="themeConfig">
    <div class="app-container">
      <!-- 顶部导航 -->
      <header class="app-header" v-if="!isAuthPage">
        <div class="logo">
          <span class="logo-icon">🛒</span>
          <span class="logo-text">Agent Skill Shop</span>
        </div>
        <div class="nav-menu">
          <a-menu mode="horizontal" :selected-keys="[currentRoute]">
            <a-menu-item key="home" @click="$router.push('/')">
              🏠 首页
            </a-menu-item>
            <a-menu-item key="skills" @click="$router.push('/')">
              🤖 技能市场
            </a-menu-item>
            <a-menu-item 
              v-if="isDeveloper" 
              key="upload" 
              @click="$router.push('/upload')"
            >
              ➕ 上传技能
            </a-menu-item>
          </a-menu>
        </div>
        <div class="header-actions">
          <template v-if="isLoggedIn">
            <a-dropdown>
              <a class="user-dropdown" @click.prevent>
                <a-avatar :size="32">
                  <template #icon>👤</template>
                </a-avatar>
                <span class="username">{{ user?.username }}</span>
              </a>
              <template #overlay>
                <a-menu>
                  <a-menu-item @click="$router.push('/profile')">
                    👤 个人中心
                  </a-menu-item>
                  <a-menu-item @click="$router.push('/upload')" v-if="isDeveloper">
                    ➕ 我的技能
                  </a-menu-item>
                  <a-menu-divider />
                  <a-menu-item @click="handleLogout">
                    🚪 退出登录
                  </a-menu-item>
                </a-menu>
              </template>
            </a-dropdown>
          </template>
          <template v-else>
            <a-button type="primary" @click="$router.push('/login')">
              登录
            </a-button>
            <a-button @click="$router.push('/register')" style="margin-left: 8px">
              注册
            </a-button>
          </template>
        </div>
      </header>

      <!-- 主内容区 -->
      <main class="main-content">
        <router-view />
      </main>

      <!-- 页脚 -->
      <footer class="app-footer" v-if="!isAuthPage">
        <div class="footer-content">
          <p>© 2026 Titan Lab. All rights reserved.</p>
          <p>用 AI 解锁人类潜能的边界</p>
        </div>
      </footer>
    </div>
  </a-config-provider>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { message } from 'ant-design-vue'

const router = useRouter()
const route = useRoute()

const user = ref(null)
const themeConfig = ref({
  algorithm: [],
  token: {
    colorPrimary: '#667eea',
    borderRadius: 8
  }
})

const currentRoute = computed(() => {
  const name = route.name
  if (name === 'Home' || name === 'SkillsHome') return 'home'
  if (name === 'SkillDetail') return 'skills'
  if (name === 'UploadSkill') return 'upload'
  return name?.toLowerCase() || ''
})

const isAuthPage = computed(() => {
  return route.name === 'Login' || route.name === 'Register'
})

const isLoggedIn = computed(() => {
  return !!localStorage.getItem('token')
})

const isDeveloper = computed(() => {
  if (!user.value) {
    const userStr = localStorage.getItem('user')
    if (userStr) {
      user.value = JSON.parse(userStr)
    }
  }
  return user.value?.is_developer || false
})

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  user.value = null
  message.success('已退出登录')
  router.push('/')
}

const loadUser = () => {
  const userStr = localStorage.getItem('user')
  if (userStr) {
    user.value = JSON.parse(userStr)
  }
}

onMounted(() => {
  loadUser()
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  height: 64px;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 20px;
  font-weight: 700;
  color: #667eea;
  cursor: pointer;
}

.logo-icon {
  font-size: 28px;
}

.nav-menu {
  flex: 1;
  display: flex;
  justify-content: center;
}

.nav-menu .ant-menu {
  background: transparent;
  border: none;
}

.header-actions {
  display: flex;
  align-items: center;
}

.user-dropdown {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #333;
  text-decoration: none;
  cursor: pointer;
}

.username {
  font-size: 14px;
}

.main-content {
  flex: 1;
}

.app-footer {
  background: #1a1a2e;
  color: white;
  padding: 48px 24px;
  text-align: center;
}

.footer-content p {
  margin: 8px 0;
  opacity: 0.8;
}
</style>
