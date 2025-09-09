import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from config import BOT_TOKEN, WEBHOOK_BASE_URL, WEBHOOK_PATH, WEBHOOK_SECRET
from db.models import connect_to_mongo, close_mongo_connection
from core.logger import setup_logging
from bot.handlers import router

bot = Bot(token=BOT_TOKEN)

async def on_startup(bot: Bot):
    """Настройка webhook при запуске"""
    webhook_url = f"{WEBHOOK_BASE_URL}{WEBHOOK_PATH}"
    await bot.set_webhook(webhook_url, secret_token=WEBHOOK_SECRET)
    logging.info(f"Webhook установлен: {webhook_url}")

async def on_shutdown(bot: Bot):
    """Очистка при остановке"""
    await bot.delete_webhook()
    logging.info("Webhook удален")

async def run_bot():
    setup_logging()
    
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    try:
        await connect_to_mongo()
        
        # Запуск в режиме webhook
        app = web.Application()
        
        webhook_requests_handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot,
            secret_token=WEBHOOK_SECRET
        )
        webhook_requests_handler.register(app, path=WEBHOOK_PATH)
        
        setup_application(app, dp, bot=bot)
        
        web.run_app(app, host="0.0.0.0", port=8080)
        
    finally:
        await close_mongo_connection()
        await bot.session.close()