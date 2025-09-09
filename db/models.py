from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from datetime import datetime
from typing import Optional, List, Dict, Any
from bson import ObjectId
from config import MONGO_URI, MONGO_DB_NAME

# Глобальные переменные для подключения
client: Optional[AsyncIOMotorClient] = None
db: Optional[AsyncIOMotorDatabase] = None

async def connect_to_mongo():
    """Подключение к MongoDB"""
    global client, db
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[MONGO_DB_NAME]
    print("Connected to MongoDB")

async def close_mongo_connection():
    """Закрытие подключения к MongoDB"""
    global client
    if client:
        client.close()
        print("Disconnected from MongoDB")

class User:
    collection_name = "users"
    
    @classmethod
    async def create(cls, user_id: int, username: str = None, first_name: str = None):
        """Создание пользователя"""
        user_data = {
            "user_id": user_id,
            "username": username,
            "first_name": first_name,
            "created_at": datetime.utcnow(),
            "is_active": True
        }
        result = await db[cls.collection_name].insert_one(user_data)
        return str(result.inserted_id)
    
    @classmethod
    async def get_by_user_id(cls, user_id: int):
        """Получение пользователя по user_id"""
        return await db[cls.collection_name].find_one({"user_id": user_id})

class Task:
    collection_name = "tasks"
    
    @classmethod
    async def create(cls, user_id: int, youtube_url: str, opus_job_id: str = None):
        """Создание задачи"""
        task_data = {
            "user_id": user_id,
            "youtube_url": youtube_url,
            "opus_job_id": opus_job_id,
            "status": "pending",
            "clips": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        result = await db[cls.collection_name].insert_one(task_data)
        return str(result.inserted_id)
    
    @classmethod
    async def update_status(cls, task_id: str, status: str):
        """Обновление статуса задачи"""
        await db[cls.collection_name].update_one(
            {"_id": ObjectId(task_id)},
            {"$set": {"status": status, "updated_at": datetime.utcnow()}}
        )
    
    @classmethod
    async def add_clips(cls, task_id: str, clips: List[Dict[str, Any]]):
        """Добавление клипов к задаче"""
        await db[cls.collection_name].update_one(
            {"_id": ObjectId(task_id)},
            {
                "$set": {
                    "clips": clips,
                    "status": "completed",
                    "updated_at": datetime.utcnow()
                }
            }
        )
    
    @classmethod
    async def get_by_opus_job_id(cls, opus_job_id: str):
        """Получение задачи по opus_job_id"""
        return await db[cls.collection_name].find_one({"opus_job_id": opus_job_id})

__all__ = ['Task', 'User', 'connect_to_mongo', 'close_mongo_connection']