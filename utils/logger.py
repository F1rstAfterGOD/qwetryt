import logging
import sys
from datetime import datetime
from config import LOG_LEVEL

def setup_logging():
    """Настройка логирования"""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('logs/bot.log', encoding='utf-8')
        ]
    )

def log_user_request(user_id: int, url: str):
    """Логирование запроса пользователя"""
    logging.info(f"User {user_id} requested processing: {url}")

def log_webhook_received(data: dict):
    """Логирование получения webhook"""
    logging.info(f"Webhook received: {data}")