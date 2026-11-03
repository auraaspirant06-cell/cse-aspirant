"""
CSE Aspirant - Channel & Group Promotion Commands
"""
from typing import Dict, Any
from promotion.manager import promotion_manager
from core.config import config
from bot.keyboards.inline import inline_kb

async def handle_promote(user_id: int, channel_link: str) -> Dict[str, Any]:
    if not channel_link:
        return {
            "text": (
                "📢 **Channel & Group Promotion Submission**\n\n"
                "Please provide your public Telegram group or channel link.\n"
                "Usage: `/promote https://t.me/your_channel` or `/promote @your_channel`\n\n"
                "⚠️ *Submissions are forwarded to the Bot Owner for verification before broadcast.*"
            )
        }

    try:
        promo = await promotion_manager.submit_promotion(user_id, channel_link)
        return {
            "text": (
                f"✅ **Promotion Request Submitted!** (ID: `{promo.promo_id}`)\n\n"
                f"Channel: `{channel_link}`\n"
                "Your request has been forwarded to the bot owner for manual audit."
            ),
            "owner_notify": {
                "owner_id": config.bot.owner_id,
                "text": f"📢 New Promotion Submission (ID: `{promo.promo_id}`):\nUser: `{user_id}`\nChannel: {promo.channel_link}",
                "reply_markup": {"inline_keyboard": inline_kb.promo_review(promo.promo_id)}
            }
        }
    except Exception as e:
        return {"text": f"❌ Error: {str(e)}"}

