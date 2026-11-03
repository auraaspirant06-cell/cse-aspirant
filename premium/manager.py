"""
CSE Aspirant - Premium Membership Manager
"""
from typing import Optional
from database.repository import repo
from premium.tiers import get_tier_policy, TierPolicy

class PremiumManager:
    async def get_user_tier(self, user_id: int) -> str:
        user = await repo.get_user(user_id)
        return user.tier if user else "FREE"

    async def get_user_policy(self, user_id: int) -> TierPolicy:
        tier = await self.get_user_tier(user_id)
        return get_tier_policy(tier)

    async def upgrade_user(self, user_id: int, new_tier: str):
        await repo.update_user_tier(user_id, new_tier)

premium_manager = PremiumManager()

