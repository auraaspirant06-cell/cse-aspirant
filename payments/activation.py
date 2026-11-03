"""
CSE Aspirant - Subscription Activation & API Key Delivery
"""
from typing import Dict, Any
from database.repository import repo
from database.models import PaymentRecord, ApiKeyRecord
from core.logger import logger

class ActivationService:
    async def activate_and_deliver_keys(self, utr: str, approved_by: int) -> Dict[str, Any]:
        existing = await repo.get_payment(utr)
        if existing and existing.status == "APPROVED":
            tier = "PRO" if existing.amount >= 499 else "PREMIUM"
            return {
                "user_id": existing.user_id,
                "tier": tier,
                "api_key": None,
                "rate_limit": 0,
                "status": "ALREADY_ACTIVE",
            }
        record = await repo.approve_payment(utr, approved_by=approved_by)
        tier = "PRO" if record.amount >= 499 else "PREMIUM"
        
        # Generate official NextGen API Key for the user
        api_record: ApiKeyRecord = await repo.generate_api_key(record.user_id, tier=tier)
        
        logger.info("Subscription activated for user %s: Tier=%s", record.user_id, tier)
        return {
            "user_id": record.user_id,
            "tier": tier,
            "api_key": api_record.key,
            "rate_limit": api_record.rate_limit_per_minute,
            "status": "ACTIVE"
        }

    async def reject_payment(self, utr: str, rejected_by: int) -> bool:
        return await repo.reject_payment(utr, rejected_by=rejected_by)

activation_service = ActivationService()

