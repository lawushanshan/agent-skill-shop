<template>
  <div class="home-container">
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="hero-content">
        <h1>🛒 Agent Skill Shop</h1>
        <p class="hero-subtitle">发现、购买、部署 AI 智能体技能</p>
        <p class="hero-description">
          平台抽成仅 20%，支持免费技能分享，一键部署到 ACC 平台
        </p>
        <div class="hero-actions">
          <a-button type="primary" size="large" @click="$router.push('/skills')">
            浏览技能
          </a-button>
          <a-button size="large" @click="$router.push('/upload')" v-if="isLoggedIn">
            上传技能
          </a-button>
        </div>
      </div>
    </div>

    <!-- 技能列表 -->
    <div class="skills-section">
      <div class="section-header">
        <h2>热门技能</h2>
        <div class="filter-controls">
          <a-radio-group v-model:value="filterType" @change="loadSkills">
            <a-radio-button value="all">全部</a-radio-button>
            <a-radio-button value="free">免费</a-radio-button>
            <a-radio-button value="paid">付费</a-radio-button>
          </a-radio-group>
          <a-input-search
            v-model:value="searchQuery"
            placeholder="搜索技能..."
            style="width: 250px; margin-left: 16px"
            @search="loadSkills"
          />
        </div>
      </div>

      <div class="skills-grid" v-if="skills.length > 0">
        <div
          v-for="skill in skills"
          :key="skill.id"
          class="skill-card"
          @click="viewSkill(skill.id)"
        >
          <div class="skill-header">
            <span class="skill-icon">🚀</span>
            <a-tag v-if="skill.is_free" color="green">免费</a-tag>
            <a-tag v-else color="blue">¥{{ skill.price }}</a-tag>
          </div>
          <h3 class="skill-title">{{ skill.name }}</h3>
          <p class="skill-desc">{{ skill.description }}</p>
          <div class="skill-footer">
            <span class="skill-category">{{ skill.category }}</span>
            <span class="skill-stats">
              ⬇️ {{ skill.download_count }} | ⭐ {{ skill.rating.toFixed(1) }}
            </span>
          </div>
        </div>
      </div>

      <a-empty v-else description="暂无技能" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()
const skills = ref([])
const loading = ref(false)
const filterType = ref('all')
const searchQuery = ref('')
const isLoggedIn = ref(!!localStorage.getItem('token'))

const loadSkills = async () => {
  loading.value = true
  try {
    const params = {}
    if (filterType.value === 'free') {
      params.is_free = true
    } else if (filterType.value === 'paid') {
      params.is_free = false
    }
    if (searchQuery.value) {
      params.search = searchQuery.value
    }
    
    const response = await api.skills.list(params)
    skills.value = response.data.items
  } catch (error) {
    console.error('加载技能失败:', error)
  } finally {
    loading.value = false
  }
}

const viewSkill = (id) => {
  router.push(`/skills/${id}`)
}

onMounted(() => {
  loadSkills()
})
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background: #f5f7fa;
}

.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 80px 20px;
  text-align: center;
}

.hero-content h1 {
  font-size: 48px;
  margin-bottom: 16px;
}

.hero-subtitle {
  font-size: 24px;
  margin-bottom: 12px;
  opacity: 0.9;
}

.hero-description {
  font-size: 16px;
  margin-bottom: 32px;
  opacity: 0.8;
}

.hero-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.skills-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  flex-wrap: wrap;
  gap: 16px;
}

.section-header h2 {
  font-size: 28px;
  color: #333;
}

.filter-controls {
  display: flex;
  align-items: center;
  gap: 16px;
}

.skills-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}

.skill-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.skill-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.skill-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.skill-icon {
  font-size: 32px;
}

.skill-title {
  font-size: 20px;
  color: #333;
  margin-bottom: 12px;
}

.skill-desc {
  color: #666;
  font-size: 14px;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.skill-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
  color: #999;
}

.skill-category {
  background: #f0f2f5;
  padding: 4px 12px;
  border-radius: 12px;
}

.skill-stats {
  display: flex;
  gap: 12px;
}
</style>
