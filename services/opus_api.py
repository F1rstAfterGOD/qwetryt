import aiohttp
import json
from typing import Optional
from config import OPUS_API_KEY, OPUS_API_URL
from utils.logger import log_opus_request

class OpusAPI:
    def __init__(self):
        self.api_key = OPUS_API_KEY
        self.base_url = OPUS_API_URL
        self.webhook_url = "http://localhost:8000/webhook/opus"
    
    async def create_job(self, youtube_url: str, user_id: int, task_id: str) -> Optional[str]:
        """Создание задачи в Opus.pro API"""
        if not self.api_key:
            raise ValueError("OPUS_API_KEY не настроен")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "url": youtube_url,
            "webhook_url": self.webhook_url,
            "meta": {
                "task_id": task_id,
                "user_id": user_id
            }
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/jobs",
                headers=headers,
                json=payload
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    job_id = data.get("job_id")
                    log_opus_request(user_id, youtube_url, job_id)
                    return job_id
                else:
                    error_text = await response.text()
                    raise Exception(f"Opus API error: {response.status} - {error_text}")

opus_api = OpusAPI()