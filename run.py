import asyncio
from multiprocessing import Process
from aiohttp import web
from utils.logger import setup_logging

def run_bot():
    """Запуск Telegram бота с webhook"""
    from bot.main import main
    asyncio.run(main())

def run_api():
    """Запуск aiohttp сервера для webhook"""
    async def start_api():
        from api.main import init_app
        app = await init_app()
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', 8000)
        await site.start()
        print("API сервер запущен на порту 8000")
        
        # Ждем бесконечно
        try:
            await asyncio.Future()  # run forever
        except asyncio.CancelledError:
            pass
        finally:
            await runner.cleanup()
    
    asyncio.run(start_api())

if __name__ == "__main__":
    setup_logging()
    
    # Запуск API в отдельном процессе
    api_process = Process(target=run_api)
    api_process.start()
    
    # Запуск бота в основном процессе
    try:
        run_bot()
    except KeyboardInterrupt:
        print("Получен сигнал остановки")
    finally:
        api_process.terminate()
        api_process.join()
        print("Приложение остановлено")