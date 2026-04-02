<template>
  <div class="upload-skill">
    <div class="upload-header">
      <h1>➕ 上传技能</h1>
      <p>分享你的 AI 技能，帮助开发者，获得收益</p>
    </div>

    <a-card>
      <a-form
        :model="formState"
        name="upload"
        @finish="handleSubmit"
        layout="vertical"
      >
        <a-row :gutter="24">
          <a-col :span="12">
            <a-form-item
              label="技能名称"
              name="name"
              :rules="[{ required: true, message: '请输入技能名称' }]"
            >
              <a-input
                v-model:value="formState.name"
                placeholder="例如：智能客服助手"
                size="large"
              />
            </a-form-item>
          </a-col>

          <a-col :span="12">
            <a-form-item
              label="技能分类"
              name="category"
              :rules="[{ required: true, message: '请选择技能分类' }]"
            >
              <a-select
                v-model:value="formState.category"
                placeholder="选择分类"
                size="large"
              >
                <a-select-option value="nlp">📝 自然语言处理</a-select-option>
                <a-select-option value="vision">👁️ 计算机视觉</a-select-option>
                <a-select-option value="data">📊 数据分析</a-select-option>
                <a-select-option value="automation">🤖 自动化</a-select-option>
                <a-select-option value="other">其他</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>

        <a-form-item
          label="技能描述"
          name="description"
          :rules="[{ required: true, message: '请输入技能描述' }]"
        >
          <a-textarea
            v-model:value="formState.description"
            placeholder="请详细描述技能的功能和使用场景"
            :rows="4"
            size="large"
          />
        </a-form-item>

        <a-row :gutter="24">
          <a-col :span="12">
            <a-form-item
              label="技能版本"
              name="version"
              :rules="[{ required: true, message: '请输入版本号' }]"
            >
              <a-input
                v-model:value="formState.version"
                placeholder="1.0.0"
                size="large"
              />
            </a-form-item>
          </a-col>

          <a-col :span="12">
            <a-form-item label="作者名称" name="author">
              <a-input
                v-model:value="formState.author"
                placeholder="你的名称或团队名"
                size="large"
              />
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="24">
          <a-col :span="12">
            <a-form-item label="是否免费" name="is_free">
              <a-radio-group v-model:value="formState.is_free">
                <a-radio :value="true">🆓 免费</a-radio>
                <a-radio :value="false">💰 付费</a-radio>
              </a-radio-group>
            </a-form-item>
          </a-col>

          <a-col :span="12" v-if="!formState.is_free">
            <a-form-item
              label="价格 (元)"
              name="price"
              :rules="[{ required: true, message: '请输入价格' }]"
            >
              <a-input-number
                v-model:value="formState.price"
                :min="0"
                :precision="2"
                style="width: 100%"
                size="large"
              />
            </a-form-item>
          </a-col>
        </a-row>

        <a-form-item label="GitHub 仓库" name="repository">
          <a-input
            v-model:value="formState.repository"
            placeholder="https://github.com/username/repo"
            size="large"
          />
        </a-form-item>

        <a-form-item label="文档链接" name="documentation">
          <a-input
            v-model:value="formState.documentation"
            placeholder="https://your-docs-url.com"
            size="large"
          />
        </a-form-item>

        <a-form-item label="标签" name="tags">
          <a-select
            v-model:value="formState.tags"
            mode="tags"
            placeholder="输入标签后按回车，例如：AI、NLP、客服"
            size="large"
          />
        </a-form-item>

        <a-form-item>
          <a-checkbox v-model:checked="formState.agree">
            我承诺此技能为原创或已获授权，符合平台规范
          </a-checkbox>
        </a-form-item>

        <a-form-item>
          <a-button
            type="primary"
            html-type="submit"
            size="large"
            :loading="loading"
            :disabled="!formState.agree"
          >
            {{ loading ? '提交中...' : '提交技能' }}
          </a-button>
        </a-form-item>
      </a-form>
    </a-card>

    <a-alert
      message="💡 收益说明"
      description="付费技能：平台抽成 20%，开发者获得 80% 收益。免费技能：提升知名度和影响力。"
      type="info"
      show-icon
      style="margin-top: 24px"
    />
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { skills } from '../api'

const router = useRouter()
const loading = ref(false)

const formState = reactive({
  name: '',
  description: '',
  category: '',
  version: '1.0.0',
  author: '',
  is_free: true,
  price: 0,
  repository: '',
  documentation: '',
  tags: [],
  agree: false
})

const handleSubmit = async () => {
  loading.value = true
  try {
    const skillData = {
      ...formState,
      price: formState.is_free ? 0 : formState.price
    }
    
    await skills.create(skillData)
    
    message.success('技能提交成功！等待审核后上架')
    router.push('/profile')
  } catch (error) {
    console.error('提交失败:', error)
    const errorMsg = error.response?.data?.detail || '提交失败，请稍后重试'
    message.error(errorMsg)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.upload-skill {
  max-width: 1000px;
  margin: 0 auto;
  padding: 24px;
}

.upload-header {
  text-align: center;
  margin-bottom: 32px;
}

.upload-header h1 {
  font-size: 32px;
  color: #333;
  margin-bottom: 8px;
}

.upload-header p {
  color: #666;
  font-size: 16px;
}
</style>
