/**
 * API 客户端 - Axios 配置
 */
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8087',  // 运维调整端口
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器 - 添加 JWT Token
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 处理错误
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // Token 过期，清除并跳转登录
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// ============ 认证 API ============
export const auth = {
  // 用户登录
  login: async (email, password) => {
    const response = await api.post('/api/auth/login', { email, password })
    return response.data
  },
  
  // 用户注册
  register: async (username, email, password, isDeveloper = false) => {
    const response = await api.post('/api/auth/register', {
      username,
      email,
      password,
      is_developer: isDeveloper
    })
    return response.data
  },
  
  // 获取当前用户
  getCurrentUser: async () => {
    const response = await api.get('/api/auth/me')
    return response.data
  }
}

// ============ 技能 API ============
export const skills = {
  // 获取技能列表
  list: async (params = {}) => {
    const response = await api.get('/api/skills', { params })
    return response.data
  },
  
  // 获取技能详情
  getById: async (id) => {
    const response = await api.get(`/api/skills/${id}`)
    return response.data
  },
  
  // 创建技能
  create: async (skillData) => {
    const response = await api.post('/api/skills', skillData)
    return response.data
  },
  
  // 更新技能
  update: async (id, skillData) => {
    const response = await api.put(`/api/skills/${id}`, skillData)
    return response.data
  },
  
  // 删除技能
  delete: async (id) => {
    const response = await api.delete(`/api/skills/${id}`)
    return response.data
  }
}

// ============ 订单 API ============
export const orders = {
  // 获取订单列表
  list: async (params = {}) => {
    const response = await api.get('/api/orders', { params })
    return response.data
  },
  
  // 创建订单
  create: async (skillId) => {
    const response = await api.post('/api/orders', { skill_id: skillId })
    return response.data
  },
  
  // 获取订单详情
  getById: async (id) => {
    const response = await api.get(`/api/orders/${id}`)
    return response.data
  }
}

// ============ 评价 API ============
export const reviews = {
  // 创建评价
  create: async (skillId, content, rating) => {
    const response = await api.post(`/api/skills/${skillId}/reviews`, {
      content,
      rating
    })
    return response.data
  }
}

export default api
