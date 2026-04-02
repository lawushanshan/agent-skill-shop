<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <h1>🛒 Agent Skill Shop</h1>
        <p>AI 智能体技能商店平台</p>
      </div>

      <a-form
        :model="formState"
        name="login"
        @finish="handleLogin"
        layout="vertical"
      >
        <a-form-item
          name="email"
          :rules="[{ required: true, message: '请输入邮箱', type: 'email' }]"
        >
          <a-input
            v-model:value="formState.email"
            placeholder="邮箱"
            size="large"
          >
            <template #prefix>📧</template>
          </a-input>
        </a-form-item>

        <a-form-item
          name="password"
          :rules="[{ required: true, message: '请输入密码' }]"
        >
          <a-input-password
            v-model:value="formState.password"
            placeholder="密码"
            size="large"
          >
            <template #prefix>🔒</template>
          </a-input-password>
        </a-form-item>

        <a-form-item>
          <a-button
            type="primary"
            html-type="submit"
            size="large"
            :loading="loading"
            block
          >
            {{ loading ? '登录中...' : '登录' }}
          </a-button>
        </a-form-item>

        <div class="login-footer">
          <span>还没有账号？</span>
          <router-link to="/register">立即注册</router-link>
        </div>
      </a-form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { auth } from '../api'

const router = useRouter()
const loading = ref(false)

const formState = reactive({
  email: '',
  password: ''
})

const handleLogin = async () => {
  loading.value = true
  try {
    const response = await auth.login(formState.email, formState.password)
    
    // 保存 token 和用户信息
    localStorage.setItem('token', response.access_token)
    localStorage.setItem('user', JSON.stringify(response.user))
    
    message.success('登录成功！')
    
    // 跳转到首页
    router.push('/')
  } catch (error) {
    console.error('登录失败:', error)
    message.error(error.response?.data?.detail || '登录失败，请检查邮箱和密码')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-box {
  background: white;
  border-radius: 16px;
  padding: 48px;
  width: 100%;
  max-width: 420px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-header h1 {
  font-size: 28px;
  color: #333;
  margin-bottom: 8px;
}

.login-header p {
  color: #666;
  font-size: 14px;
}

.login-footer {
  text-align: center;
  color: #666;
  font-size: 14px;
  margin-top: 16px;
}

.login-footer a {
  color: #667eea;
  text-decoration: none;
  margin-left: 8px;
  font-weight: 500;
}

.login-footer a:hover {
  text-decoration: underline;
}
</style>
