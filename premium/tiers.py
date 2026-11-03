"""
CSE Aspirant - Premium Tier Definitions & Capabilities
"""
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class TierPolicy:
    name: str
    max_queue_size: int
    max_duration_seconds: int
    api_rate_limit: int  # requests per minute
    ai_daily_limit: int
    priority_audio: bool
    can_use_soundfx: bool

TIER_POLICIES: Dict[str, TierPolicy] = {
    "FREE": TierPolicy(
        name="FREE",
        max_queue_size=15,
        max_duration_seconds=600,
        api_rate_limit=10,
        ai_daily_limit=20,
        priority_audio=False,
        can_use_soundfx=False
    ),
    "PREMIUM": TierPolicy(
        name="PREMIUM",
        max_queue_size=100,
        max_duration_seconds=3600,
        api_rate_limit=100,
        ai_daily_limit=200,
        priority_audio=True,
        can_use_soundfx=True
    ),
    "PRO": TierPolicy(
        name="PRO",
        max_queue_size=500,
        max_duration_seconds=14400,
        api_rate_limit=1000,
        ai_daily_limit=10000,
        priority_audio=True,
        can_use_soundfx=True
    )
}

def get_tier_policy(tier: str) -> TierPolicy:
    return TIER_POLICIES.get(tier.upper(), TIER_POLICIES["FREE"])

