<template>
  <div class="profile">
    <div class="profile-header">
      <a-avatar :size="80">
        <template #icon>👤</template>
      </a-avatar>
      <div class="profile-info">
        <h1>{{ user?.username }}</h1>
        <p>{{ user?.email }}</p>
        <a-tag v-if="user?.is_developer" color="blue">开发者</a-tag>
        <a-tag v-else color="green">用户</a-tag>
      </div>
    </div>

    <a-row :gutter="24">
      <a-col :span="12">
        <a-card title="我的技能" class="mb-24">
          <template #extra>
            <a @click="$router.push('/upload')">上传新技能</a>
          </template>
          
          <a-empty v-if="mySkills.length === 0" description="暂无技能" />
          
          <a-list
            v-else
            :data-source="mySkills"
            split
          >
            <template #renderItem="{ item }">
              <a-list-item>
                <a-list-item-meta>
                  <template #title>
                    <a @click="$router.push(`/skills/${item.id}`)">
                      {{ item.name }}
                    </a>
                  </template>
                  <template #description>
                    <a-tag v-if="item.is_free" color="green">免费</a-tag>
                    <a-tag v-else color="orange">¥{{ item.price }}</a-tag>
                    <span>📥 {{ item.download_count }} 次下载</span>
                  </template>
                </a-list-item-meta>
              </a-list-item>
            </template>
          </a-list>
        </a-card>
      </a-col>

      <a-col :span="12">
        <a-card title="我的订单" class="mb-24">
          <a-empty v-if="orders.length === 0" description="暂无订单" />
          
          <a-list
            v-else
            :data-source="orders"
            split
          >
            <template #renderItem="{ item }">
              <a-list-item>
                <a-list-item-meta>
                  <template #title>
                    {{ item.order_no }}
                  </template>
                  <template #description>
                    <a-tag :color="getStatusColor(item.status)">
                      {{ getStatusText(item.status) }}
                    </a-tag>
                    <span>¥{{ item.amount }}</span>
                  </template>
                </a-list-item-meta>
              </a-list-item>
            </template>
          </a-list>
        </a-card>

        <a-card title="账户信息">
          <a-descriptions :column="1" size="small">
            <a-descriptions-item label="用户 ID">
              {{ user?.id }}
            </a-descriptions-item>
            <a-descriptions-item label="注册时间">
              {{ user?.created_at ? new Date(user.created_at).toLocaleDateString() : '-' }}
            </a-descriptions-item>
            <a-descriptions-item label="角色">
              {{ user?.role || '普通用户' }}
            </a-descriptions-item>
          </a-descriptions>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { message } from 'ant-design-vue'
import { skills, orders } from '../api'

const user = ref(null)
const mySkills = ref([])
const ordersList = ref([])

const getStatusColor = (status) => {
  const colors = {
    pending: 'orange',
    paid: 'blue',
    completed: 'green',
    refunded: 'red'
  }
  return colors[status] || 'default'
}

const getStatusText = (status) => {
  const texts = {
    pending: '待支付',
    paid: '已支付',
    completed: '已完成',
    refunded: '已退款'
  }
  return texts[status] || status
}

const loadData = async () => {
  try {
    // 加载用户信息
    const userStr = localStorage.getItem('user')
    if (userStr) {
      user.value = JSON.parse(userStr)
      
      // 加载用户的技能
      if (user.value.is_developer) {
        const skillsResponse = await skills.list({ limit: 100 })
        mySkills.value = (skillsResponse.items || []).filter(
          s => s.developer_id === user.value.id
        )
      }
    }
    
    // 加载订单
    const ordersResponse = await orders.list()
    ordersList.value = ordersResponse.items || []
  } catch (error) {
    console.error('加载数据失败:', error)
    message.error('加载数据失败')
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.profile {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-bottom: 32px;
  padding: 32px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  color: white;
}

.profile-info h1 {
  font-size: 28px;
  margin-bottom: 8px;
}

.profile-info p {
  opacity: 0.9;
  margin-bottom: 12px;
}

.mb-24 {
  margin-bottom: 24px;
}
</style>
