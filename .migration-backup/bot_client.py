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
        self._telegram_app = None
        self._assistant_app = None
        self._voice_client = None

    async def start(self):
        if not config.bot.bot_token:
            raise RuntimeError("BOT_TOKEN must be configured before starting the Telegram client")
        if not config.bot.session_string:
            raise RuntimeError("TELEGRAM_SESSION_STRING is required for voice-chat playback")
        try:
            from pyrogram import Client, filters
            from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
            from pytgcalls import PyTgCalls
            from music.telegram_backend import TelegramVoiceChatBackend
            from music.multi_group import multi_player_manager
        except ImportError as exc:
            raise RuntimeError("Install pyrogram, tgcrypto, and py-tgcalls before starting the bot") from exc

        bot_args = {
            "api_id": config.bot.api_id,
            "api_hash": config.bot.api_hash,
            "bot_token": config.bot.bot_token,
        }
        app = Client("cse_aspirant_bot", **bot_args)
        assistant = Client(
            "cse_aspirant_assistant",
            api_id=config.bot.api_id,
            api_hash=config.bot.api_hash,
            session_string=config.bot.session_string,
        )
        voice_client = PyTgCalls(assistant)

        @app.on_message(filters.text)
        async def on_message(_: Client, message: Message):
            if not message.from_user or not message.chat:
                return
            response = await self.process_update(
                message.chat.id,
                message.from_user.id,
                message.from_user.first_name or "User",
                message.text or "",
            )
            if response and response.get("text"):
                markup = response.get("reply_markup")
                if markup:
                    markup = InlineKeyboardMarkup(
                        [[InlineKeyboardButton(**button) for button in row] for row in markup["inline_keyboard"]]
                    )
                await message.reply_text(response["text"], reply_markup=markup)

        @app.on_callback_query()
        async def on_callback(_: Client, callback: CallbackQuery):
            if not callback.from_user or not callback.message:
                return
            response = await self.process_callback(
                callback.message.chat.id,
                callback.from_user.id,
                callback.data or "",
            )
            await callback.answer(response["text"], show_alert=response.get("alert", False))

        await app.start()
        await assistant.start()
        await voice_client.start()
        multi_player_manager.set_backend_factory(lambda: TelegramVoiceChatBackend(voice_client))
        self._telegram_app = app
        self._assistant_app = assistant
        self._voice_client = voice_client
        self.is_running = True
        state.is_ready = True
        logger.info("CSE ASPIRANT Telegram and voice-chat clients started successfully.")

    async def stop(self):
        self.is_running = False
        state.is_ready = False
        if self._polling_task and not self._polling_task.done():
            self._polling_task.cancel()
        if self._voice_client:
            await self._voice_client.stop()
            self._voice_client = None
        if self._telegram_app:
            await self._telegram_app.stop()
            self._telegram_app = None
        if self._assistant_app:
            await self._assistant_app.stop()
            self._assistant_app = None
        logger.info("CSE ASPIRANT Bot engine gracefully stopped.")

    async def process_update(self, chat_id: int, user_id: int, user_name: str, text: str) -> Optional[dict]:
        return await router.dispatch_command(chat_id, user_id, user_name, text)

    async def process_callback(self, chat_id: int, user_id: int, callback_data: str) -> dict:
        return await router.dispatch_callback(chat_id, user_id, callback_data)

bot_client = BotClient()
