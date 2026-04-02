<template>
  <div class="skills-home">
    <!-- Hero 区域 -->
    <div class="hero-section">
      <div class="hero-content">
        <h1>🚀 发现强大的 AI 技能</h1>
        <p>探索、购买、部署 AI 智能体技能，让你的应用更智能</p>
        <div class="search-box">
          <a-input-search
            v-model:value="searchQuery"
            placeholder="搜索技能..."
            size="large"
            @search="handleSearch"
          />
        </div>
        <div class="filter-tags">
          <a-tag
            :color="filter === 'all' ? 'blue' : ''"
            @click="filter = 'all'"
            style="cursor: pointer"
          >
            全部
          </a-tag>
          <a-tag
            :color="filter === 'free' ? 'green' : ''"
            @click="filter = 'free'"
            style="cursor: pointer"
          >
            🆓 免费
          </a-tag>
          <a-tag
            :color="filter === 'paid' ? 'orange' : ''"
            @click="filter = 'paid'"
            style="cursor: pointer"
          >
            💰 付费
          </a-tag>
        </div>
      </div>
    </div>

    <!-- 技能列表 -->
    <div class="skills-list">
      <div class="skills-header">
        <h2>热门技能</h2>
        <a-select
          v-model:value="sortBy"
          style="width: 150px"
          @change="loadSkills"
        >
          <a-select-option value="popular">最受欢迎</a-select-option>
          <a-select-option value="newest">最新发布</a-select-option>
          <a-select-option value="rating">评分最高</a-select-option>
        </a-select>
      </div>

      <a-row :gutter="[24, 24]">
        <a-col
          v-for="skill in skills"
          :key="skill.id"
          :xs="24"
          :sm="12"
          :md="8"
          :lg="6"
        >
          <a-card
            hoverable
            class="skill-card"
            @click="goToSkill(skill.id)"
          >
            <template #cover>
              <div class="skill-cover">
                <span class="skill-icon">🤖</span>
                <a-tag
                  v-if="skill.is_free"
                  color="green"
                  class="free-tag"
                >
                  免费
                </a-tag>
                <a-tag
                  v-else
                  color="orange"
                  class="price-tag"
                >
                  ¥{{ skill.price }}
                </a-tag>
              </div>
            </template>
            <template #title>
              <div class="skill-title">{{ skill.name }}</div>
            </template>
            <a-card-meta>
              <template #description>
                <p class="skill-desc">{{ skill.description }}</p>
                <div class="skill-meta">
                  <span>📥 {{ skill.download_count }}</span>
                  <span>⭐ {{ skill.rating.toFixed(1) }}</span>
                </div>
              </template>
            </a-card-meta>
          </a-card>
        </a-col>
      </a-row>

      <!-- 空状态 -->
      <a-empty
        v-if="skills.length === 0 && !loading"
        description="暂无技能"
      />

      <!-- 加载状态 -->
      <div v-if="loading" class="loading">
        <a-spin size="large" tip="加载中..." />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { skills as skillsApi } from '../api'

const router = useRouter()

const skills = ref([])
const loading = ref(false)
const searchQuery = ref('')
const filter = ref('all')
const sortBy = ref('popular')

const loadSkills = async () => {
  loading.value = true
  try {
    const params = {
      skip: 0,
      limit: 20
    }
    
    if (filter.value === 'free') {
      params.is_free = true
    } else if (filter.value === 'paid') {
      params.is_free = false
    }
    
    if (searchQuery.value) {
      params.search = searchQuery.value
    }
    
    const response = await skillsApi.list(params)
    skills.value = response.items || []
  } catch (error) {
    console.error('加载技能失败:', error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  loadSkills()
}

const goToSkill = (skillId) => {
  router.push(`/skills/${skillId}`)
}

onMounted(() => {
  loadSkills()
})
</script>

<style scoped>
.skills-home {
  min-height: 100vh;
  background: #f5f5f5;
}

.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 80px 24px;
  text-align: center;
  color: white;
}

.hero-content h1 {
  font-size: 48px;
  margin-bottom: 16px;
  font-weight: 700;
}

.hero-content p {
  font-size: 18px;
  margin-bottom: 32px;
  opacity: 0.9;
}

.search-box {
  max-width: 600px;
  margin: 0 auto 24px;
}

.filter-tags {
  display: flex;
  justify-content: center;
  gap: 12px;
}

.skills-list {
  max-width: 1400px;
  margin: 0 auto;
  padding: 48px 24px;
}

.skills-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.skills-header h2 {
  font-size: 28px;
  color: #333;
}

.skill-card {
  cursor: pointer;
  transition: transform 0.3s;
  height: 100%;
}

.skill-card:hover {
  transform: translateY(-8px);
}

.skill-cover {
  height: 200px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.skill-icon {
  font-size: 80px;
}

.free-tag,
.price-tag {
  position: absolute;
  top: 16px;
  right: 16px;
  font-weight: 600;
}

.skill-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.skill-desc {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.skill-meta {
  display: flex;
  justify-content: space-between;
  margin-top: 12px;
  color: #999;
  font-size: 13px;
}

.loading {
  text-align: center;
  padding: 60px 0;
}
</style>
