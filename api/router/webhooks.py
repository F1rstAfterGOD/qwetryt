from fastapi import APIRouter, HTTPException
from db.models import Task
from api.schemas.webhooks import OpusWebhookRequest
import logging

router = APIRouter(tags=["webhooks"])

@router.post("/opus")
async def opus_webhook(webhook_data: OpusWebhookRequest):
    """Обработка webhook от Opus Clip"""
    try:
        # Находим задачу по job_id
        task = await Task.get_by_opus_job_id(webhook_data.job_id)
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Обновляем статус задачи
        if webhook_data.status == "completed" and webhook_data.clips:
            await Task.add_clips(str(task["_id"]), webhook_data.clips)
        else:
            await Task.update_status(str(task["_id"]), webhook_data.status)
        
        logging.info(f"Webhook processed for job_id: {webhook_data.job_id}")
        return {"status": "success"}
        
    except Exception as e:
        logging.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")