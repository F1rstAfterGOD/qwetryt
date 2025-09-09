import logging
import os
from datetime import datetime

def setup_logging():
    """Настройка логирования"""
    # Создаем папку logs если её нет
    os.makedirs('logs', exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/bot.log'),
            logging.StreamHandler()
        ]
    )

def log_webhook_received(job_id: str, status: str):
    """Логирование получения webhook"""
    logging.info(f"Webhook получен: job_id={job_id}, status={status}")

def log_task_completed(user_id: int, clips_total: int, shorts_ok: int):
    """Логирование завершения задачи"""
    logging.info(f"Задача завершена: user_id={user_id}, clips={clips_total}, shorts={shorts_ok}")

def log_task_failed(user_id: int, reason: str):
    """Логирование ошибки задачи"""
    logging.error(f"Задача провалена: user_id={user_id}, reason={reason}")

def log_opus_request(user_id: int, url: str, job_id: str):
    """Логирование запроса к Opus API"""
    logging.info(f"Запрос к Opus: user_id={user_id}, url={url}, job_id={job_id}")

def log_user_request(user_id: int, url: str):
    """Логирование пользовательского запроса"""
    logging.info(f"Пользователь {user_id} отправил URL: {url}")