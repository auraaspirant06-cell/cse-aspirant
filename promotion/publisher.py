"""
CSE Aspirant - Promotion Publisher
"""
from typing import Dict, Any, List
from database.repository import repo
from core.logger import logger
from error_handling.exceptions import CSEAspirantException

class PromotionPublisher:
    async def publish_promotion(self, promo_id: str, broadcast_callback) -> Dict[str, Any]:
        promo = await repo.get_promotion(promo_id)
        if not promo or promo.status != "APPROVED":
            raise CSEAspirantException("Promotion is not approved by the owner and cannot be published.")

        msg = (
            "🌟 **CSE ASPIRANT COMMUNITY SPOTLIGHT** 🌟\n\n"
            "Check out this verified channel partner:\n"
            f"👉 {promo.channel_link}\n\n"
            "Join to accelerate your exam and programming mastery!"
        )
        
        delivered = await broadcast_callback(msg)
        promo.status = "PUBLISHED"
        logger.info(f"Published promotion {promo_id} across groups.")
        return {"promo_id": promo_id, "status": "PUBLISHED", "recipients": delivered}

promotion_publisher = PromotionPublisher()

