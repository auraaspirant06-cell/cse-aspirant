"""
CSE Aspirant - Admin Moderation Commands
"""
from typing import Dict, Any
from moderation.actions import moderation_actions

async def handle_warn(chat_id: int, user_id: int, actor_id: int, reason: str = "Rule violation") -> Dict[str, Any]:
    count = await moderation_actions.warn_user(chat_id, user_id, reason, actor_id)
    return {"text": f"⚠️ User `{user_id}` has been warned (Warning {count}/3). Reason: {reason}"}

async def handle_kick(chat_id: int, user_id: int, actor_id: int) -> Dict[str, Any]:
    async def dummy_kick(c, u): return True
    await moderation_actions.kick_user(chat_id, user_id, actor_id, dummy_kick)
    return {"text": f"👢 User `{user_id}` has been removed from the group."}

async def handle_ban(chat_id: int, user_id: int, actor_id: int) -> Dict[str, Any]:
    async def dummy_ban(c, u): return True
    await moderation_actions.ban_user(chat_id, user_id, actor_id, dummy_ban)
    return {"text": f"🔨 User `{user_id}` has been permanently banned from the group."}

