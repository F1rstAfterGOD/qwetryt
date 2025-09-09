import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aiohttp import web
import json

from db.models import connect_to_mongo, close_mongo_connection
from api.webhooks import opus_webhook
from utils.logger import setup_logging

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

if __name__ == '__main__':
    import asyncio
    
    async def main():
        app = await init_app()
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, 'localhost', 8000)
        await site.start()
        print("🚀 API сервер запущен на http://localhost:8000")
        
        try:
            await asyncio.Future()  # run forever
        except KeyboardInterrupt:
            pass
        finally:
            await runner.cleanup()
    
    asyncio.run(main())