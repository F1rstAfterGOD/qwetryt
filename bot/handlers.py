import re
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from db.models import Task
from services.opus_api import opus_api
from utils.logger import log_user_request

router = Router()

def is_youtube_url(url: str) -> bool:
    """Проверка, является ли URL ссылкой на YouTube"""
    youtube_patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=[\w-]+',
        r'(?:https?://)?(?:www\.)?youtu\.be/[\w-]+',
        r'(?:https?://)?(?:www\.)?youtube\.com/shorts/[\w-]+'
    ]
    return any(re.match(pattern, url) for pattern in youtube_patterns)

@router.message(Command("start"))
async def start_handler(message: Message):
    """Обработчик команды /start"""
    welcome_text = (
        "👋 Привет! Я бот для нарезки YouTube видео на Shorts.\n\n"
        "Просто отправь мне ссылку на YouTube видео, и я создам из него короткие клипы!\n\n"
        "Поддерживаемые форматы:\n"
        "• youtube.com/watch?v=...\n"
        "• youtu.be/...\n"
        "• youtube.com/shorts/..."
    )
    await message.answer(welcome_text)

@router.message(F.text)
async def url_handler(message: Message):
    """Обработчик URL от пользователя"""
    url = message.text.strip()
    user_id = message.from_user.id
    
    if not is_youtube_url(url):
        await message.answer(
            "❌ Это не похоже на ссылку YouTube.\n"
            "Отправь корректную ссылку на видео."
        )
        return
    
    log_user_request(user_id, url)
    
    # Отправляем сообщение о начале обработки
    processing_msg = await message.answer("⏳ Отправляю видео на обработку...")
    
    try:
        # Создаем задачу в БД
        task_id = await Task.create(user_id, url, "")
        
        # Отправляем запрос в Opus API
        opus_job_id = await opus_api.create_job(url, user_id, task_id)
        
        if not opus_job_id:
            await processing_msg.edit_text("❌ Не удалось создать задачу. Попробуй позже.")
            return
        
        # Обновляем задачу с opus_job_id
        await Task.update_status(task_id, "processing")
        
        await processing_msg.edit_text(
            "✅ Видео принято в обработку!\n"
            "Я уведомлю тебя, когда нарезка будет готова."
        )
        
    except Exception as e:
        await processing_msg.edit_text(
            "❌ Произошла ошибка при обработке.\n"
            "Попробуй позже или проверь ссылку."
        )