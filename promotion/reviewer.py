"""
CSE Aspirant - Promotion Owner Review Handler
"""
from typing import Dict, Any, Optional
from database.repository import repo
from database.models import PromotionRecord
from core.logger import logger

class PromotionReviewer:
    def format_review_message(self, promo: PromotionRecord) -> str:
        return (
            "📢 **NEW CHANNEL PROMOTION REQUEST**\n\n"
            f"🆔 **Promo ID**: `{promo.promo_id}`\n"
            f"👤 **Requester ID**: `{promo.user_id}`\n"
            f"🔗 **Channel/Group**: {promo.channel_link}\n\n"
            "Only owner-approved promotions will be broadcasted."
        )

    async def review(self, promo_id: str, action: str, owner_id: int) -> Optional[PromotionRecord]:
        status = "APPROVED" if action.upper() == "APPROVE" else "REJECTED"
        logger.info(f"Owner {owner_id} marked promotion {promo_id} as {status}")
        return await repo.update_promotion_status(promo_id, status, reviewed_by=owner_id)

promotion_reviewer = PromotionReviewer()

