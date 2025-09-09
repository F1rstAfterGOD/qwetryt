import aiohttp
import logging
from typing import Optional, Dict, Any
from config import OPUS_API_KEY, OPUS_API_URL

class OpusAPI:
    """Клиент для работы с Opus.pro API"""
    
    def __init__(self):
        self.api_key = OPUS_API_KEY
        self.base_url = OPUS_API_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def create_job(self, youtube_url: str, user_id: int, task_id: str) -> Optional[str]:
        """Создание задачи обработки видео в Opus"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "url": youtube_url,
                    "webhook_url": f"{self.base_url}/webhook/opus",
                    "metadata": {
                        "user_id": user_id,
                        "task_id": task_id
                    }
                }
                
                async with session.post(
                    f"{self.base_url}/api/v1/jobs",
                    json=payload,
                    headers=self.headers
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("job_id")
                    else:
                        error_text = await response.text()
                        logging.error(f"Opus API error: {response.status} - {error_text}")
                        return None
                        
        except Exception as e:
            logging.error(f"Ошибка при создании задачи в Opus: {e}")
            return None
    
    async def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Получение статуса задачи"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/v1/jobs/{job_id}",
                    headers=self.headers
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logging.error(f"Ошибка получения статуса: {response.status}")
                        return None
                        
        except Exception as e:
            logging.error(f"Ошибка при получении статуса: {e}")
            return None

# Глобальный экземпляр
opus_api = OpusAPI()