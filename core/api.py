from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.models import connect_to_mongo, close_mongo_connection
from core.logger import setup_logging
from api.router.webhooks import router as webhooks_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    setup_logging()
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()

def create_app() -> FastAPI:
    app = FastAPI(
        title="YouTube Shorts Bot API",
        version="1.0.0",
        lifespan=lifespan
    )
    
    # Include routers
    app.include_router(webhooks_router, prefix="/webhooks")
    
    @app.get("/health")
    async def health():
        return {"status": "ok"}
    
    return app