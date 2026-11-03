"""
CSE Aspirant - Help Command Handler
"""
from typing import Dict, Any
from bot.keyboards.inline import inline_kb

async def handle_help() -> Dict[str, Any]:
    text = (
        "🧭 **CSE ASPIRANT - HELP CENTER** 🧭\n\n"
        "Select any category below to view detailed command lists, usages, and options.\n\n"
        "Supported Command Prefixes:\n"
        "• `/command`\n"
        "• `!command`\n"
        "• `.command`"
    )
    return {
        "text": text,
        "reply_markup": {"inline_keyboard": inline_kb.help_main_menu()}
    }

