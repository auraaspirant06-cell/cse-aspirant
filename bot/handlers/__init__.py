"""
CSE Aspirant Bot Command Handlers Package
"""
from bot.handlers.start import handle_start
from bot.handlers.help import handle_help
from bot.handlers.music_cmd import (
    handle_play, handle_pause, handle_resume, handle_skip,
    handle_previous, handle_stop, handle_queue, handle_shuffle,
    handle_repeat, handle_volume, handle_seek, handle_playlist
)
from bot.handlers.education_cmd import (
    handle_education, handle_upsc, handle_cs, handle_ncert,
    handle_current_affairs, handle_pyq, handle_quiz, handle_planner
)
from bot.handlers.programming_cmd import handle_programming, handle_lang_course
from bot.handlers.ai_cmd import (
    handle_ai_chat, handle_ai_ask, handle_ai_code,
    handle_ai_debug, handle_ai_math, handle_ai_summarize
)
from bot.handlers.premium_cmd import handle_premium_status, handle_verify
from bot.handlers.payment_cmd import handle_pay, handle_submit_utr
from bot.handlers.promo_cmd import handle_promote
from bot.handlers.security_cmd import handle_audit
from bot.handlers.admin_cmd import handle_warn, handle_kick, handle_ban
from bot.handlers.owner_cmd import handle_stats, handle_set_tier, handle_manual_approve_utr

__all__ = [
    "handle_start", "handle_help",
    "handle_play", "handle_pause", "handle_resume", "handle_skip",
    "handle_previous", "handle_stop", "handle_queue", "handle_shuffle",
    "handle_repeat", "handle_volume", "handle_seek", "handle_playlist",
    "handle_education", "handle_upsc", "handle_cs", "handle_ncert",
    "handle_current_affairs", "handle_pyq", "handle_quiz", "handle_planner",
    "handle_programming", "handle_lang_course",
    "handle_ai_chat", "handle_ai_ask", "handle_ai_code",
    "handle_ai_debug", "handle_ai_math", "handle_ai_summarize",
    "handle_premium_status", "handle_verify",
    "handle_pay", "handle_submit_utr",
    "handle_promote",
    "handle_audit",
    "handle_warn", "handle_kick", "handle_ban",
    "handle_stats", "handle_set_tier", "handle_manual_approve_utr"
]

