"""
CSE Aspirant - Usage Limits and Quota Enforcement
"""
from typing import Any, Dict
import time
from premium.tiers import get_tier_policy
from error_handling.exceptions import RateLimitExceededError

class QuotaManager:
    def __init__(self):
        self._user_usage: Dict[int, Dict[str, Any]] = {}

    def check_api_quota(self, user_id: int, tier: str) -> bool:
        policy = get_tier_policy(tier)
        now = time.time()
        record = self._user_usage.setdefault(user_id, {"minute_window": now, "req_count": 0})
        
        if now - record["minute_window"] > 60:
            record["minute_window"] = now
            record["req_count"] = 0
            
        if record["req_count"] >= policy.api_rate_limit:
            raise RateLimitExceededError(retry_after=int(60 - (now - record["minute_window"])))
            
        record["req_count"] += 1
        return True

quota_manager = QuotaManager()

