"""
CSE Aspirant - Subscription Activation & API Key Delivery
"""
from typing import Dict, Any
from database.repository import repo
from database.models import PaymentRecord, ApiKeyRecord
from core.logger import logger

class ActivationService:
    async def activate_and_deliver_keys(self, utr: str, approved_by: int) -> Dict[str, Any]:
        record = await repo.approve_payment(utr, approved_by=approved_by)
        tier = "PRO" if record.amount >= 499 else "PREMIUM"
        
        # Generate official NextGen API Key for the user
        api_record: ApiKeyRecord = await repo.generate_api_key(record.user_id, tier=tier)
        
        logger.info(f"Subscription activated for user {record.user_id}: Tier={tier}, Key={api_record.key}")
        return {
            "user_id": record.user_id,
            "tier": tier,
            "api_key": api_record.key,
            "rate_limit": api_record.rate_limit_per_minute,
            "status": "ACTIVE"
        }

activation_service = ActivationService()

