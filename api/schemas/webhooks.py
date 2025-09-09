from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class OpusWebhookRequest(BaseModel):
    """Схема для webhook от Opus Clip"""
    job_id: str
    status: str
    clips: Optional[List[Dict[str, Any]]] = None
    error_message: Optional[str] = None