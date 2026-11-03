"""
CSE Aspirant - Welcome Message Generator
"""
from typing import Dict, Any
from core.config import config
from core.constants import START_IMAGE_URL

class WelcomeGreeter:
    def format_welcome_message(self, user_name: str, chat_title: str) -> str:
        return (
            f"👋 **Welcome, {user_name}, to {chat_title}!**\n\n"
            "🚀 **CSE ASPIRANT - Academy & Music Hub**\n"
            "• Use `/play <song>` for high-definition study music.\n"
            "• Use `/education` to explore UPSC & Computer Science modules.\n"
            "• Use `/programming` for dual-language programming courses.\n"
            "• Use `/help` to view all features and settings.\n\n"
            "⚡ *Study Hard. Play Smart. Succeed!*"
        )

    def get_welcome_payload(self, user_name: str, chat_title: str) -> Dict[str, Any]:
        text = self.format_welcome_message(user_name, chat_title)
        return {
            "photo": config.bot.start_img_url or START_IMAGE_URL,
            "caption": text,
            "text": text
        }

welcome_greeter = WelcomeGreeter()

