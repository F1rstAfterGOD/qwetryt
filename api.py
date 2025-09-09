import uvicorn
from core.api import create_app
from config import API_HOST, API_PORT

if __name__ == '__main__':
    app = create_app()
    uvicorn.run(
        app,
        host=API_HOST,
        port=API_PORT,
        log_level="info"
    )