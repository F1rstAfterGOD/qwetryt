from motor.motor_asyncio import AsyncIOMotorClient
import logging
from config.settings import MONGO_URI, MONGO_DB_NAME

class Database:
    client: AsyncIOMotorClient = None
    db = None

db = Database()

async def connect_to_mongo():
    """Подключение к MongoDB"""
    db.client = AsyncIOMotorClient(MONGO_URI)
    db.db = db.client[MONGO_DB_NAME]
    logging.info("Подключение к MongoDB установлено")

async def close_mongo_connection():
    """Закрытие подключения к MongoDB"""
    if db.client:
        db.client.close()
        logging.info("Подключение к MongoDB закрыто")