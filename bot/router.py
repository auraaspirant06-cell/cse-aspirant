"""
CSE Aspirant - Unified Multi-Prefix Command & Callback Router
"""
import re
from typing import Dict, Any, Optional
from core.constants import SUPPORTED_PREFIXES
from core.logger import logger
from monitoring.metrics import metrics
from moderation.rules import moderation_rules
from error_handling.handlers import format_error_response
import bot.handlers as h
from bot.callbacks.help_cb import help_cb_handler
from bot.callbacks.music_cb import music_cb_handler
from bot.callbacks.payment_cb import payment_cb_handler, promo_cb_handler

class CommandRouter:
    def __init__(self):
        self.prefixes = SUPPORTED_PREFIXES

    def parse_command(self, text: str) -> Optional[Dict[str, str]]:
        if not text:
            return None
        text = text.strip()
        for p in self.prefixes:
            if text.startswith(p):
                parts = text[len(p):].strip().split(maxsplit=1)
                cmd = parts[0].lower().split("@")[0]  # strip bot @username if present
                args = parts[1] if len(parts) > 1 else ""
                return {"command": cmd, "args": args, "prefix": p}
        return None

    async def dispatch_command(
        self,
        chat_id: int,
        user_id: int,
        user_name: str,
        text: str
    ) -> Optional[Dict[str, Any]]:
        # Security & Moderation Inspection
        ok, reason = moderation_rules.check_message(user_id, text)
        if not ok:
            return {"text": f"🛡 {reason}"}

        parsed = self.parse_command(text)
        if not parsed:
            return None

        cmd = parsed["command"]
        args = parsed["args"]
        metrics.increment("commands_total")
        logger.info(f"Dispatching command: '{cmd}' with args '{args}' from user {user_id}")

        try:
            # Basic Commands
            if cmd == "start":
                return await h.handle_start(user_id, user_name, chat_id)
            elif cmd in ("help", "menu"):
                return await h.handle_help()

            # Music Commands
            elif cmd in ("play", "p"):
                return await h.handle_play(chat_id, user_id, user_name, args)
            elif cmd == "pause":
                return await h.handle_pause(chat_id)
            elif cmd == "resume":
                return await h.handle_resume(chat_id)
            elif cmd in ("skip", "next"):
                return await h.handle_skip(chat_id)
            elif cmd in ("previous", "prev"):
                return await h.handle_previous(chat_id)
            elif cmd == "stop":
                return await h.handle_stop(chat_id)
            elif cmd in ("queue", "q"):
                return await h.handle_queue(chat_id)
            elif cmd == "shuffle":
                return await h.handle_shuffle(chat_id)
            elif cmd in ("repeat", "loop"):
                return await h.handle_repeat(chat_id, args)
            elif cmd in ("volume", "vol"):
                return await h.handle_volume(chat_id, args)
            elif cmd == "playlist":
                return await h.handle_playlist(chat_id, args or "study_focus", user_id, user_name)

            # Education Commands
            elif cmd == "education":
                return await h.handle_education(args or "en")
            elif cmd == "upsc":
                return await h.handle_upsc(args or "prelims")
            elif cmd == "cs":
                return await h.handle_cs(args or "os")
            elif cmd == "ncert":
                return await h.handle_ncert(args or "history")
            elif cmd in ("currentaffairs", "ca"):
                return await h.handle_current_affairs()
            elif cmd == "pyq":
                return await h.handle_pyq(args)
            elif cmd == "quiz":
                return await h.handle_quiz()
            elif cmd == "planner":
                return await h.handle_planner(args or "UPSC")

            # Programming Commands
            elif cmd == "programming":
                return await h.handle_programming()
            elif cmd in ("python", "golang", "c", "cpp", "java", "javascript"):
                return await h.handle_lang_course(cmd, args)

            # AI Commands
            elif cmd == "ai":
                return await h.handle_ai_chat(args)
            elif cmd == "ask":
                return await h.handle_ai_ask(args)
            elif cmd == "code":
                return await h.handle_ai_code(args)
            elif cmd == "debug":
                return await h.handle_ai_debug(args)
            elif cmd == "math":
                return await h.handle_ai_math(args)
            elif cmd == "summarize":
                return await h.handle_ai_summarize(args)

            # Premium & Payment
            elif cmd == "premium":
                return await h.handle_premium_status(user_id)
            elif cmd == "verify":
                return await h.handle_verify(user_id, args)
            elif cmd == "pay":
                return await h.handle_pay(user_id, args or "PREMIUM")
            elif cmd == "submit_utr":
                return await h.handle_submit_utr(user_id, args)

            # Promotion
            elif cmd in ("promote", "promo"):
                return await h.handle_promote(user_id, args)

            # Security & Admin
            elif cmd == "audit":
                return await h.handle_audit()
            elif cmd == "warn" and args:
                target_id = int(args.split()[0])
                return await h.handle_warn(chat_id, target_id, user_id)
            elif cmd == "kick" and args:
                target_id = int(args.split()[0])
                return await h.handle_kick(chat_id, target_id, user_id)
            elif cmd == "ban" and args:
                target_id = int(args.split()[0])
                return await h.handle_ban(chat_id, target_id, user_id)

            # Owner Commands
            elif cmd in ("stats", "telemetry"):
                return await h.handle_stats(user_id)
            elif cmd == "set_tier" and len(args.split()) >= 2:
                parts = args.split()
                return await h.handle_set_tier(user_id, int(parts[0]), parts[1])
            elif cmd == "approve_utr" and args:
                return await h.handle_manual_approve_utr(user_id, args.strip())

            return None
        except Exception as e:
            logger.error(f"Error processing command {cmd}: {e}")
            return {"text": f"⚠️ An error occurred while executing `{cmd}`: {e}"}

    async def dispatch_callback(
        self,
        chat_id: int,
        user_id: int,
        callback_data: str
    ) -> Dict[str, Any]:
        logger.info(f"Dispatching callback: '{callback_data}' from user {user_id}")
        
        # Help Menu Callbacks
        if callback_data.startswith("help_"):
            content = help_cb_handler.get_help(callback_data)
            return {"text": content, "alert": False}

        # Music Controls Callbacks
        elif callback_data.startswith("music_"):
            resp = await music_cb_handler.handle(chat_id, callback_data)
            return {"text": resp, "alert": False}

        # Payment Review Callbacks
        elif callback_data.startswith("pay_"):
            resp = await payment_cb_handler.handle_approval(callback_data, user_id)
            return {"text": resp, "alert": True}

        # Promo Review Callbacks
        elif callback_data.startswith("promo_"):
            resp = await promo_cb_handler.handle_review(callback_data, user_id)
            return {"text": resp, "alert": True}

        return {"text": "Action received.", "alert": False}

router = CommandRouter()

