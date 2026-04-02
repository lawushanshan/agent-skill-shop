"""
ACC 对接服务 - 技能部署到 ACC 平台
"""
import httpx
import os
from typing import Optional, Dict
from datetime import datetime

# ACC 配置
ACC_BASE_URL = os.getenv("ACC_BASE_URL", "http://localhost:8082")

class ACCService:
    """ACC 平台对接服务"""
    
    def __init__(self):
        self.base_url = ACC_BASE_URL
        self.timeout = 30.0
    
    async def deploy_skill_to_acc(self, skill_data: Dict) -> Optional[Dict]:
        """
        部署技能到 ACC 平台
        
        Args:
            skill_data: 技能数据字典，包含 name, description, category 等
        
        Returns:
            部署结果：{"agent_id": "...", "status": "success", "url": "..."}
            失败返回 None
        """
        try:
            # 构建 ACC Agent 数据
            agent_data = {
                "name": f"Skill: {skill_data['name']}",
                "description": skill_data.get('description', ''),
                "team": "skill",  # 技能团队
                "config": {
                    "skill_id": skill_data['id'],
                    "category": skill_data.get('category', 'general'),
                    "version": skill_data.get('version', '1.0.0'),
                    "author": skill_data.get('author', 'Unknown'),
                }
            }
            
            # 调用 ACC API 创建 Agent
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/agents",
                    json=agent_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return {
                        "agent_id": result.get('id'),
                        "status": "success",
                        "url": f"{self.base_url}/agents/{result.get('id')}",
                        "deployed_at": datetime.utcnow().isoformat()
                    }
                else:
                    print(f"ACC 部署失败：{response.status_code} - {response.text}")
                    return None
                    
        except Exception as e:
            print(f"ACC 部署异常：{e}")
            return None
    
    async def get_agent_status(self, agent_id: str) -> Optional[Dict]:
        """
        获取 ACC Agent 状态
        
        Args:
            agent_id: ACC Agent ID
        
        Returns:
            Agent 状态信息
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/api/agents/{agent_id}"
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return None
                    
        except Exception as e:
            print(f"获取 Agent 状态异常：{e}")
            return None
    
    async def undeploy_skill(self, agent_id: str) -> bool:
        """
        从 ACC 移除 Agent
        
        Args:
            agent_id: ACC Agent ID
        
        Returns:
            是否成功
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.delete(
                    f"{self.base_url}/api/agents/{agent_id}"
                )
                
                return response.status_code == 200
                    
        except Exception as e:
            print(f"移除 Agent 异常：{e}")
            return False


# 全局 ACC 服务实例
acc_service = ACCService()
