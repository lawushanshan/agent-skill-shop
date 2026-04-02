<template>
  <div class="skills-container">
    <h1>技能市场</h1>
    <p>浏览和发现 AI 智能体技能</p>
    
    <a-empty description="技能列表页面开发中..." style="margin-top: 100px" />
    
    <div style="text-align: center; margin-top: 32px">
      <a-button type="primary" @click="$router.push('/')">返回首页</a-button>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.skills-container {
  padding: 40px 20px;
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
}

.skills-container h1 {
  font-size: 32px;
  margin-bottom: 16px;
  color: #333;
}

.skills-container p {
  color: #666;
  font-size: 16px;
}
</style>
