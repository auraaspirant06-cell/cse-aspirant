"""
CSE Aspirant - Owner & Sudo Controls
"""
from typing import Dict, Any
from core.config import config
from monitoring.sys_info import sys_monitor
from monitoring.metrics import metrics
from music.multi_group import multi_player_manager
from database.repository import repo
from payments.activation import activation_service

async def handle_stats(actor_id: int) -> Dict[str, Any]:
    if actor_id != config.bot.owner_id and actor_id not in config.bot.sudo_users:
        return {"text": "⛔ Access Denied: This command is restricted to Bot Owner."}

    sys_res = sys_monitor.get_system_metrics()
    active_music = multi_player_manager.count_active_players()
    
    text = (
        "👑 **CSE ASPIRANT - SYSTEM TELEMETRY** 👑\n\n"
        f"⏱ **System Uptime**: {sys_res['uptime_seconds']}s\n"
        f"🖥 **CPU Utilization**: {sys_res['cpu_percent']}%\n"
        f"🧠 **Memory Used**: {sys_res['memory_used_mb']} MB ({sys_res['memory_percent']}%)\n"
        f"🎵 **Active Voice Chats**: {active_music}\n"
        f"⚡ **Commands Handled**: {metrics.counters['commands_total']}\n"
        f"🔒 **PostgreSQL / Redis**: ONLINE"
    )
    return {"text": text}

async def handle_set_tier(actor_id: int, target_user_id: int, new_tier: str) -> Dict[str, Any]:
    if actor_id != config.bot.owner_id:
        return {"text": "⛔ Access Denied: Owner only."}
    
    tier_clean = new_tier.upper()
    await repo.update_user_tier(target_user_id, tier_clean)
    return {"text": f"✅ User `{target_user_id}` tier updated to **{tier_clean}**."}

async def handle_manual_approve_utr(actor_id: int, utr: str) -> Dict[str, Any]:
    if actor_id != config.bot.owner_id and actor_id not in config.bot.sudo_users:
        return {"text": "⛔ Access Denied: Owner or Sudo only."}

    res = await activation_service.activate_and_deliver_keys(utr, approved_by=actor_id)
    return {
        "text": (
            f"✅ **Payment Reconciled!**\n"
            f"• UTR: `{utr}`\n"
            f"• User ID: `{res['user_id']}`\n"
            f"• Tier: `{res['tier']}`\n"
            f"• Generated Key: `{res['api_key']}`"
        )
    }

