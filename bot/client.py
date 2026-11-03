"""
CSE Aspirant - Bot Client Engine
"""
import asyncio
from typing import Optional, Any
from core.config import config
from core.logger import logger
from core.context import state
from bot.router import router

class BotClient:
    def __init__(self):
        self.is_running = False
        self._polling_task: Optional[asyncio.Task] = None

    async def start(self):
        logger.info(f"Starting {config.bot.bot_token[:10]}... client in async engine")
        self.is_running = True
        state.is_ready = True
        logger.info("CSE ASPIRANT Bot engine started successfully.")

    async def stop(self):
        self.is_running = False
        state.is_ready = False
        if self._polling_task and not self._polling_task.done():
            self._polling_task.cancel()
        logger.info("CSE ASPIRANT Bot engine gracefully stopped.")

    async def process_update(self, chat_id: int, user_id: int, user_name: str, text: str) -> Optional[dict]:
        return await router.dispatch_command(chat_id, user_id, user_name, text)

    async def process_callback(self, chat_id: int, user_id: int, callback_data: str) -> dict:
        return await router.dispatch_callback(chat_id, user_id, callback_data)

bot_client = BotClient()

