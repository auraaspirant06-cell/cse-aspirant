"""
CSE Aspirant - API Authentication & Tier Verification
"""
from fastapi import Header, HTTPException, Security, status
from typing import Optional
import secrets
from core.config import config
from database.repository import repo
from database.models import ApiKeyRecord
from premium.limits import quota_manager

async def verify_api_key(x_api_key: Optional[str] = Header(None)) -> ApiKeyRecord:
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing 'X-API-Key' header."
        )

    # Master Owner Key bypass
    if config.services.jwt_secret and secrets.compare_digest(x_api_key, config.services.jwt_secret):
        return ApiKeyRecord(
            key=x_api_key,
            user_id=config.bot.owner_id,
            tier="PRO",
            rate_limit_per_minute=999999
        )

    record = await repo.get_api_key(x_api_key)
    if not record or not record.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or revoked API Key."
        )

    # Bypass limits for owner and sudo users
    if record.user_id == config.bot.owner_id or record.user_id in config.bot.sudo_users:
        record.total_requests += 1
        return record

    # Enforce quota based on key tier
    quota_manager.check_api_quota(record.user_id, record.tier)
    record.total_requests += 1
    return record

