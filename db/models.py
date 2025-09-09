from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from typing import Optional, Dict, Any
from bson import ObjectId
import logging

from config import MONGO_URI, MONGO_DB_NAME

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

class Task:
    collection_name = "tasks"
    
    @classmethod
    async def create(cls, tg_user_id: int, source_url: str, opus_job_id: str) -> str:
        """Создание новой задачи"""
        task_data = {
            "tg_user_id": tg_user_id,
            "source_url": source_url,
            "opus_job_id": opus_job_id,
            "status": "processing",
            "created_at": datetime.utcnow(),
            "clips_total": 0,
            "shorts_ok": 0
        }
        result = await db.db[cls.collection_name].insert_one(task_data)
        return str(result.inserted_id)
    
    @classmethod
    async def find_by_opus_job_id(cls, opus_job_id: str) -> Optional[Dict[str, Any]]:
        """Поиск задачи по opus_job_id"""
        return await db.db[cls.collection_name].find_one({"opus_job_id": opus_job_id})
    
    @classmethod
    async def find_by_task_id(cls, task_id: str) -> Optional[Dict[str, Any]]:
        """Поиск задачи по _id"""
        try:
            return await db.db[cls.collection_name].find_one({"_id": ObjectId(task_id)})
        except:
            return None
    
    @classmethod
    async def update_status(cls, task_id: str, status: str, clips_total: int = 0, shorts_ok: int = 0):
        """Обновление статуса задачи"""
        update_data = {
            "status": status,
            "updated_at": datetime.utcnow()
        }
        if clips_total > 0:
            update_data["clips_total"] = clips_total
        if shorts_ok > 0:
            update_data["shorts_ok"] = shorts_ok
            
        await db.db[cls.collection_name].update_one(
            {"_id": ObjectId(task_id)},
            {"$set": update_data}
        )