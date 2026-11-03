"""
CSE Aspirant - Premium & Social Verification Commands
"""
from typing import Dict, Any
from premium.manager import premium_manager
from premium.social_verify import social_verifier
from premium.tiers import TIER_POLICIES

async def handle_premium_status(user_id: int) -> Dict[str, Any]:
    tier = await premium_manager.get_user_tier(user_id)
    policy = await premium_manager.get_user_policy(user_id)
    
    text = (
        f"💎 **CSE ASPIRANT MEMBERSHIP** 💎\n\n"
        f"👤 **Your Current Tier**: `{tier}`\n"
        f"• Max Audio Queue: {policy.max_queue_size} tracks\n"
        f"• Max Stream Duration: {policy.max_duration_seconds // 60} minutes\n"
        f"• API Rate Quota: {policy.api_rate_limit} req/min\n"
        f"• Daily AI Quota: {policy.ai_daily_limit} queries\n\n"
        "Tiers Available:\n"
        "1. 🥉 **FREE**: Basic music & study tools\n"
        "2. 🥈 **PREMIUM (₹199/mo)**: 100 queue, 100 req/min, priority audio\n"
        "3. 🥇 **PRO (₹499/mo)**: Unlimited queue, 1000 req/min, priority AI engine\n\n"
        "Type `/pay` to upgrade your tier."
    )
    return {"text": text}

async def handle_verify(user_id: int, proof_code: str = "") -> Dict[str, Any]:
    res = await social_verifier.verify_instagram_or_fallback(user_id, "user", proof_code)
    if res.get("verified"):
        return {"text": "✅ **Social Verification Verified!** Your account perks have been enabled."}
    return {
        "text": (
            "🛡 **Social Perks Verification**\n\n"
            "Join our Telegram channel & follow our Instagram to unlock bonus features:\n"
            f"{res.get('instruction')}\n\n"
            "After completing, reply with `/verify CSE-IG-<user_id>`"
        )
    }

