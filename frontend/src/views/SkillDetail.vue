<template>
  <div class="skill-detail">
    <div class="skill-header">
      <div class="skill-icon">🤖</div>
      <div class="skill-info">
        <h1>{{ skill?.name }}</h1>
        <div class="skill-meta">
          <a-tag v-if="skill?.is_free" color="green">🆓 免费</a-tag>
          <a-tag v-else color="orange">💰 ¥{{ skill?.price }}</a-tag>
          <a-tag color="blue">{{ skill?.category }}</a-tag>
          <span>📥 {{ skill?.download_count }} 次下载</span>
          <span>⭐ {{ skill?.rating?.toFixed(1) }} 分</span>
        </div>
      </div>
    </div>

    <a-row :gutter="24">
      <a-col :span="16">
        <a-card title="技能介绍" class="mb-24">
          <p>{{ skill?.description }}</p>
        </a-card>

        <a-card title="技能信息" class="mb-24">
          <a-descriptions bordered :column="1">
            <a-descriptions-item label="版本">
              {{ skill?.version }}
            </a-descriptions-item>
            <a-descriptions-item label="作者">
              {{ skill?.author }}
            </a-descriptions-item>
            <a-descriptions-item label="更新时间">
              {{ skill?.updated_at ? new Date(skill.updated_at).toLocaleDateString() : '-' }}
            </a-descriptions-item>
            <a-descriptions-item label="GitHub" v-if="skill?.repository">
              <a :href="skill.repository" target="_blank">查看源码</a>
            </a-descriptions-item>
            <a-descriptions-item label="文档" v-if="skill?.documentation">
              <a :href="skill.documentation" target="_blank">查看文档</a>
            </a-descriptions-item>
          </a-descriptions>
        </a-card>

        <a-card title="用户评价" v-if="skill?.review_count > 0">
          <a-comment>
            <template #content>
              <p>暂无评价，快来成为第一个评价的用户吧！</p>
            </template>
          </a-comment>
        </a-card>
      </a-col>

      <a-col :span="8">
        <a-card class="action-card">
          <template #title>
            <div class="action-header">
              <span v-if="skill?.is_free">免费领取</span>
              <span v-else>¥{{ skill?.price }}</span>
            </div>
          </template>
          
          <a-button
            type="primary"
            size="large"
            block
            :loading="loading"
            @click="handleAction"
          >
            {{ skill?.is_free ? '免费领取' : '立即购买' }}
          </a-button>

          <a-button
            size="large"
            block
            style="margin-top: 12px"
            v-if="isLoggedIn"
            @click="handleDeploy"
          >
            🚀 部署到 ACC
          </a-button>

          <a-divider />

          <div class="platform-fee" v-if="!skill?.is_free">
            <p>💡 说明：</p>
            <ul>
              <li>平台抽成：20%</li>
              <li>开发者收益：80%</li>
            </ul>
          </div>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { message } from 'ant-design-vue'
import { skills, orders } from '../api'

const router = useRouter()
const route = useRoute()

const skill = ref(null)
const loading = ref(false)

const isLoggedIn = computed(() => {
  return !!localStorage.getItem('token')
})

const loadSkill = async () => {
  loading.value = true
  try {
    const data = await skills.getById(route.params.id)
    skill.value = data
  } catch (error) {
    console.error('加载技能失败:', error)
    message.error('技能不存在')
    router.push('/')
  } finally {
    loading.value = false
  }
}

const handleAction = async () => {
  if (!isLoggedIn.value) {
    message.warning('请先登录')
    router.push('/login')
    return
  }

  loading.value = true
  try {
    const order = await orders.create(skill.value.id)
    
    if (skill.value.is_free) {
      message.success('领取成功！')
    } else {
      message.success('订单创建成功！待支付功能开发中...')
    }
  } catch (error) {
    console.error('操作失败:', error)
    message.error('操作失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

const handleDeploy = async () => {
  message.info('ACC 对接功能开发中...')
  // TODO: 调用 ACC 部署 API
}

onMounted(() => {
  loadSkill()
})
</script>

<style scoped>
.skill-detail {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

.skill-header {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-bottom: 32px;
  padding: 32px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  color: white;
}

.skill-icon {
  font-size: 80px;
}

.skill-info h1 {
  font-size: 32px;
  margin-bottom: 16px;
}

.skill-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.skill-meta span {
  opacity: 0.9;
}

.mb-24 {
  margin-bottom: 24px;
}

.action-card {
  position: sticky;
  top: 88px;
}

.action-header {
  font-size: 24px;
  font-weight: 700;
  color: #667eea;
}

.platform-fee {
  font-size: 14px;
  color: #666;
}

.platform-fee ul {
  margin-top: 8px;
  padding-left: 20px;
}

.platform-fee li {
  margin: 4px 0;
}
</style>
