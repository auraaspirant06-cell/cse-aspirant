"""
CSE Aspirant - API Key Management Routes
"""
from fastapi import APIRouter, Depends, HTTPException
from api.schemas import ApiKeyCreateRequest, ApiKeyRevokeRequest, BaseResponse
from api.auth import verify_api_key
from database.repository import repo
from database.models import ApiKeyRecord
from core.config import config

router = APIRouter(prefix="/api/v1/keys", tags=["API Keys"])

@router.post("/generate", response_model=BaseResponse)
async def generate_key(req: ApiKeyCreateRequest, auth_key: ApiKeyRecord = Depends(verify_api_key)):
    if auth_key.user_id != config.bot.owner_id and auth_key.user_id not in config.bot.sudo_users:
        raise HTTPException(status_code=403, detail="Only the owner or sudo users may generate API keys.")
    if req.tier.upper() not in {"FREE", "PREMIUM", "PRO"}:
        raise HTTPException(status_code=400, detail="Invalid API key tier.")
    new_record = await repo.generate_api_key(req.user_id, req.tier.upper())
    return BaseResponse(
        message="API Key generated successfully.",
        data={
            "key": new_record.key,
            "tier": new_record.tier,
            "rate_limit_per_minute": new_record.rate_limit_per_minute
        }
    )

@router.post("/revoke", response_model=BaseResponse)
async def revoke_key(req: ApiKeyRevokeRequest, auth_key: ApiKeyRecord = Depends(verify_api_key)):
    if auth_key.user_id != config.bot.owner_id and auth_key.user_id not in config.bot.sudo_users:
        raise HTTPException(status_code=403, detail="Only the owner or sudo users may revoke API keys.")
    revoked = await repo.revoke_api_key(req.key)
    if not revoked:
        raise HTTPException(status_code=404, detail="API Key not found.")
    return BaseResponse(message="API Key has been revoked.")

