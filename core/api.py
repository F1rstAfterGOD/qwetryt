from aiohttp import web
from db.models import connect_to_mongo, close_mongo_connection
from api.router.webhooks import opus_webhook
from core.logger import setup_logging

async def init_app():
    setup_logging()
    app = web.Application()
    
    # Webhook endpoint
    app.router.add_post('/webhooks/opus', opus_webhook)
    
    # Health check
    async def health(request):
        return web.json_response({"status": "ok"})
    
    app.router.add_get('/health', health)
    
    # Startup/cleanup
    async def startup(app):
        await connect_to_mongo()
    
    async def cleanup(app):
        await close_mongo_connection()
    
    app.on_startup.append(startup)
    app.on_cleanup.append(cleanup)
    
    return app