"""
CSE Aspirant - Moderation Actions (Mute, Kick, Ban, Warn)
"""
from typing import Dict, Any
from security.audit import audit_logger
from core.logger import logger

class ModerationActions:
    def __init__(self):
        self._warnings: Dict[int, int] = {}

    async def warn_user(self, chat_id: int, user_id: int, reason: str, actor_id: int) -> int:
        count = self._warnings.get(user_id, 0) + 1
        self._warnings[user_id] = count
        audit_logger.log("USER_WARNED", actor_id, user_id, f"Reason: {reason} | Count: {count}")
        return count

    async def kick_user(self, chat_id: int, user_id: int, actor_id: int, client_kick_fn) -> bool:
        audit_logger.log("USER_KICKED", actor_id, user_id, f"Chat: {chat_id}")
        logger.info(f"Kicking user {user_id} from chat {chat_id}")
        return await client_kick_fn(chat_id, user_id)

    async def ban_user(self, chat_id: int, user_id: int, actor_id: int, client_ban_fn) -> bool:
        audit_logger.log("USER_BANNED", actor_id, user_id, f"Chat: {chat_id}")
        logger.info(f"Banning user {user_id} from chat {chat_id}")
        return await client_ban_fn(chat_id, user_id)

moderation_actions = ModerationActions()

