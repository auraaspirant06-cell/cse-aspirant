"""
CSE Aspirant - Reply Keyboards
"""
from typing import List, Dict

class ReplyKeyboards:
    @staticmethod
    def main_navigation() -> List[List[str]]:
        return [
            ["🎵 Music", "📚 Academy"],
            ["💻 Programming", "🤖 AI Assistant"],
            ["💎 Premium", "❓ Help"]
        ]

reply_kb = ReplyKeyboards()

