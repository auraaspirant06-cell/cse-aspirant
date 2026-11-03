"""
CSE Aspirant - Inline Keyboard Layouts
"""
from typing import List, Dict, Any

class InlineKeyboards:
    @staticmethod
    def help_main_menu() -> List[List[Dict[str, str]]]:
        return [
            [
                {"text": "🎵 MUSIC", "callback_data": "help_music"},
                {"text": "📚 EDUCATION", "callback_data": "help_education"}
            ],
            [
                {"text": "💻 PROGRAMMING", "callback_data": "help_programming"},
                {"text": "🤖 AI ASSISTANT", "callback_data": "help_ai"}
            ],
            [
                {"text": "💎 PREMIUM", "callback_data": "help_premium"},
                {"text": "🔐 SECURITY", "callback_data": "help_security"}
            ],
            [
                {"text": "📢 PROMOTION", "callback_data": "help_promotion"},
                {"text": "👑 OWNER PANEL", "callback_data": "help_owner"}
            ]
        ]

    @staticmethod
    def music_player_controls() -> List[List[Dict[str, str]]]:
        return [
            [
                {"text": "⏮ Prev", "callback_data": "music_prev"},
                {"text": "⏸ Pause", "callback_data": "music_pause"},
                {"text": "▶ Resume", "callback_data": "music_resume"},
                {"text": "⏭ Skip", "callback_data": "music_skip"}
            ],
            [
                {"text": "🔀 Shuffle", "callback_data": "music_shuffle"},
                {"text": "🔁 Repeat", "callback_data": "music_repeat"},
                {"text": "⏹ Stop", "callback_data": "music_stop"}
            ]
        ]

    @staticmethod
    def language_toggle() -> List[List[Dict[str, str]]]:
        return [
            [
                {"text": "🇬🇧 English", "callback_data": "lang_en"},
                {"text": "🇮🇳 हिन्दी", "callback_data": "lang_hi"}
            ]
        ]

    @staticmethod
    def payment_review(utr: str) -> List[List[Dict[str, str]]]:
        return [
            [
                {"text": "✅ Approve Payment", "callback_data": f"pay_approve_{utr}"},
                {"text": "❌ Reject", "callback_data": f"pay_reject_{utr}"}
            ]
        ]

    @staticmethod
    def promo_review(promo_id: str) -> List[List[Dict[str, str]]]:
        return [
            [
                {"text": "✅ Approve Promo", "callback_data": f"promo_approve_{promo_id}"},
                {"text": "❌ Reject", "callback_data": f"promo_reject_{promo_id}"}
            ]
        ]

inline_kb = InlineKeyboards()

