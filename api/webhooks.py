import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aiohttp import web
import hmac
import hashlib
import json
import logging
from typing import Dict, Any

from db.models import Task
from config import OPUS_WEBHOOK_SECRET, BOT_TOKEN
from aiogram import Bot
from utils.logger import log_webhook_received, log_task_completed, log_task_failed

bot = Bot(token=BOT_TOKEN)

def verify_signature(payload: bytes, signature: str) -> bool:
    """Проверка подписи webhook согласно ТЗ: HMAC-SHA256(body, OPUS_WEBHOOK_SECRET)"""
    if not OPUS_WEBHOOK_SECRET or not signature:
        return False
    expected = hmac.new(
        OPUS_WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature.replace("sha256=", ""))

async def opus_webhook(request: web.Request):
    """Webhook для получения результатов от opus.pro согласно ТЗ"""
    payload = await request.body()
    signature = request.headers.get("X-Opus-Signature", "")
    
    if not verify_signature(payload, signature):
        return web.json_response({"error": "Invalid signature"}, status=403)
    
    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        return web.json_response({"error": "Invalid JSON"}, status=400)
    job_id = data.get("job_id")
    status = data.get("status")
    clips = data.get("clips", [])
    meta = data.get("meta", {})
    error = data.get("error")
    
    # Валидация обязательных полей
    if not job_id or not status:
        return web.json_response({"error": "Missing required fields: job_id or status"}, status=400)
    
    # Поиск задачи по job_id или meta.task_id
    try:
        task = await Task.find_by_opus_job_id(job_id)
        if not task and meta.get("task_id"):
            task = await Task.find_by_task_id(meta["task_id"])
    except Exception as e:
        logging.error(f"Ошибка поиска задачи: {e}")
        return web.json_response({"error": "Database error"}, status=500)
    
    if not task:
        return web.json_response({"error": "Task not found"}, status=404)
    
    # Логирование получения webhook
    log_webhook_received(job_id, status)
    
    # Подсчет клипов согласно ТЗ (оптимизировано)
    clips_total = 0
    shorts_ok = 0
    for clip in clips:
        clips_total += 1
        if clip.get("duration", 0) <= 60 and clip.get("h", 0) > clip.get("w", 0):
            shorts_ok += 1
    
    if status == "finished":
        try:
            await Task.update_status(str(task["_id"]), "completed", clips_total, shorts_ok)
        except Exception as e:
            logging.error(f"Ошибка обновления статуса задачи: {e}")
            return web.json_response({"error": "Database error"}, status=500)
        
        # Текст уведомления согласно ТЗ
        original_title = task.get("source_url", "YouTube видео")
        message_text = (
            f"✅ Нарезка готова!\n"
            f"Клипов: {clips_total}\n"
            f"Подходят под Shorts (≤60 c): {shorts_ok}\n"
            f"Исходник: {original_title}"
        )
        
        try:
            await bot.send_message(task["tg_user_id"], message_text)
        except Exception as e:
            logging.error(f"Ошибка отправки сообщения: {e}")
        log_task_completed(task["tg_user_id"], clips_total, shorts_ok)
        
    elif status == "failed":
        try:
            await Task.update_status(str(task["_id"]), "failed")
        except Exception as e:
            logging.error(f"Ошибка обновления статуса задачи: {e}")
            return web.json_response({"error": "Database error"}, status=500)
        
        # Текст ошибки согласно ТЗ
        reason = error or "Неизвестная ошибка"
        message_text = (
            f"❌ Нарезка не удалась.\n"
            f"Причина: {reason}\n"
            f"Попробуй позже или измени исходник/ВЗ."
        )
        
        try:
            await bot.send_message(task["tg_user_id"], message_text)
        except Exception as e:
            logging.error(f"Ошибка отправки сообщения: {e}")
        log_task_failed(task["tg_user_id"], reason)
    
    return web.json_response({"status": "ok"})