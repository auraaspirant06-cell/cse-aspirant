"""
Unit Tests for Premium Tiers & Quota Enforcement
"""
import pytest
from premium.tiers import get_tier_policy, TIER_POLICIES
from premium.limits import quota_manager
from error_handling.exceptions import RateLimitExceededError

def test_tier_policies():
    free = get_tier_policy("FREE")
    prem = get_tier_policy("PREMIUM")
    pro = get_tier_policy("PRO")

    assert free.api_rate_limit == 10
    assert prem.api_rate_limit == 100
    assert pro.api_rate_limit == 1000

    assert free.priority_audio is False
    assert prem.priority_audio is True
    assert pro.priority_audio is True

def test_quota_manager_enforcement():
    user_id = 777
    quota_manager._user_usage.clear()

    # Under FREE limit (10 req/min)
    for _ in range(10):
        assert quota_manager.check_api_quota(user_id, "FREE") is True

    # 11th request exceeds quota
    with pytest.raises(RateLimitExceededError):
        quota_manager.check_api_quota(user_id, "FREE")

