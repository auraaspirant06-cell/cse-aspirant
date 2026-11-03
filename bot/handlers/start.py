"""
CSE Aspirant - Start Command Handler
"""
from typing import Dict, Any
from core.config import config
from core.constants import START_IMAGE_URL
from bot.keyboards.inline import inline_kb

async def handle_start(user_id: int, user_name: str, chat_id: int) -> Dict[str, Any]:
    photo = config.bot.start_img_url or START_IMAGE_URL
    text = (
        f"👋 **Namaste {user_name}! Welcome to CSE ASPIRANT** 🚀\n\n"
        "Your all-in-one AI-powered Telegram Music Bot & Academic Ecosystem:\n"
        "• 🎵 High-Fidelity Music Engine (Go Powered)\n"
        "• 📚 UPSC & Computer Science Academy (Hindi & English)\n"
        "• 💻 Multi-Language Programming Masterclasses\n"
        "• 🤖 NextGen AI Assistant & Code Debugger\n\n"
        "Click the **Help Menu** button below to explore all commands."
    )
    return {
        "photo": photo,
        "caption": text,
        "text": text,
        "reply_markup": {"inline_keyboard": inline_kb.help_main_menu()}
    }

