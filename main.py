"""
CSE ASPIRANT – NEXTGEN MUSIC BOT
Central Startup & Service Orchestration Module
"""
import asyncio
import signal
import sys
from core.config import config, validate_config
from core.logger import logger
from core.constants import APP_NAME, APP_VERSION
from core.context import state
from database.connection import db_manager
from bot.client import bot_client
from api.server import create_app

class ApplicationOrchestrator:
    def __init__(self):
        self.app = create_app()
        self.loop = asyncio.get_event_loop()
        self._shutdown_event = asyncio.Event()

    async def startup(self):
        validate_config(config)
        logger.info(f"==================================================")
        logger.info(f"   STARTING {APP_NAME} (v{APP_VERSION})")
        logger.info(f"==================================================")
        
        # 1. Connect Databases & Cache
        await db_manager.connect()

        # 2. Start Bot Client
        await bot_client.start()

        state.is_ready = True
        logger.info(f"{APP_NAME} is fully operational and listening.")

    async def shutdown(self):
        logger.info(f"Gracefully shutting down {APP_NAME}...")
        await bot_client.stop()
        await db_manager.disconnect()
        self._shutdown_event.set()
        logger.info(f"{APP_NAME} shutdown complete.")

    def run_api_and_services(self):
        import uvicorn
        logger.info(f"Binding NextGen API on {config.services.api_host}:{config.services.api_port}")
        uvicorn.run(
            self.app,
            host=config.services.api_host,
            port=config.services.api_port,
            log_level="info"
        )

    def start(self):
        try:
            self.loop.run_until_complete(self.startup())
            logger.info("Application loop running. Press Ctrl+C to terminate.")
            # If running standalone with API in same thread or separate worker
            self.run_api_and_services()
        except (KeyboardInterrupt, SystemExit):
            logger.info("Termination signal received.")
        finally:
            self.loop.run_until_complete(self.shutdown())

orchestrator = ApplicationOrchestrator()

if __name__ == "__main__":
    orchestrator.start()

