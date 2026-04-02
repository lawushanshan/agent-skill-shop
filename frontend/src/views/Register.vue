<template>
  <div class="register-container">
    <div class="register-box">
      <div class="register-header">
        <h1>🛒 注册账号</h1>
        <p>加入 Agent Skill Shop，开启技能变现之旅</p>
      </div>

      <a-form
        :model="formState"
        name="register"
        @finish="handleRegister"
        layout="vertical"
      >
        <a-form-item
          name="username"
          :rules="[
            { required: true, message: '请输入用户名' },
            { min: 3, message: '用户名至少 3 个字符' }
          ]"
        >
          <a-input
            v-model:value="formState.username"
            placeholder="用户名"
            size="large"
          >
            <template #prefix>👤</template>
          </a-input>
        </a-form-item>

        <a-form-item
          name="email"
          :rules="[
            { required: true, message: '请输入邮箱' },
            { type: 'email', message: '请输入有效的邮箱地址' }
          ]"
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
          :rules="[
            { required: true, message: '请输入密码' },
            { min: 6, message: '密码至少 6 个字符' }
          ]"
        >
          <a-input-password
            v-model:value="formState.password"
            placeholder="密码"
            size="large"
          >
            <template #prefix>🔒</template>
          </a-input-password>
        </a-form-item>

        <a-form-item
          name="confirmPassword"
          :rules="[
            { required: true, message: '请确认密码' },
            { validator: validateConfirmPassword }
          ]"
        >
          <a-input-password
            v-model:value="formState.confirmPassword"
            placeholder="确认密码"
            size="large"
          >
            <template #prefix>🔒</template>
          </a-input-password>
        </a-form-item>

        <a-form-item>
          <a-checkbox v-model:checked="formState.isDeveloper">
            我是开发者（我要上传技能）
          </a-checkbox>
        </a-form-item>

        <a-form-item>
          <a-button
            type="primary"
            html-type="submit"
            size="large"
            :loading="loading"
            block
          >
            {{ loading ? '注册中...' : '立即注册' }}
          </a-button>
        </a-form-item>

        <div class="register-footer">
          <span>已有账号？</span>
          <router-link to="/login">立即登录</router-link>
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
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  isDeveloper: false
})

const validateConfirmPassword = async (rule, value) => {
  if (value && value !== formState.password) {
    throw new Error('两次输入的密码不一致')
  }
}

const handleRegister = async () => {
  loading.value = true
  try {
    await auth.register(
      formState.username,
      formState.email,
      formState.password,
      formState.isDeveloper
    )
    
    message.success('注册成功！请登录')
    
    // 跳转到登录页
    router.push('/login')
  } catch (error) {
    console.error('注册失败:', error)
    const errorMsg = error.response?.data?.detail || '注册失败，请稍后重试'
    message.error(errorMsg)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.register-box {
  background: white;
  border-radius: 16px;
  padding: 48px;
  width: 100%;
  max-width: 420px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.register-header {
  text-align: center;
  margin-bottom: 32px;
}

.register-header h1 {
  font-size: 28px;
  color: #333;
  margin-bottom: 8px;
}

.register-header p {
  color: #666;
  font-size: 14px;
}

.register-footer {
  text-align: center;
  color: #666;
  font-size: 14px;
  margin-top: 16px;
}

.register-footer a {
  color: #667eea;
  text-decoration: none;
  margin-left: 8px;
  font-weight: 500;
}

.register-footer a:hover {
  text-decoration: underline;
}
</style>
