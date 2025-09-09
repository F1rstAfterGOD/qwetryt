import os
from dotenv import load_dotenv

load_dotenv()

# Bot settings
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_BASE_URL = os.getenv("WEBHOOK_BASE_URL")
WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

# API settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))

# Database settings
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "youtube_shorts_bot")

# Opus API settings
OPUS_API_KEY = os.getenv("OPUS_API_KEY")
OPUS_API_URL = os.getenv("OPUS_API_URL", "https://api.opus.pro")
OPUS_WEBHOOK_SECRET = os.getenv("OPUS_WEBHOOK_SECRET")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")