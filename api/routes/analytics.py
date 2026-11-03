"""
CSE Aspirant - Analytics & Metrics Endpoints
"""
from fastapi import APIRouter, Depends
from api.schemas import BaseResponse
from api.auth import verify_api_key
from database.models import ApiKeyRecord
from monitoring.metrics import metrics
from monitoring.sys_info import sys_monitor
from music.multi_group import multi_player_manager

router = APIRouter(prefix="/api/v1/analytics", tags=["Analytics"])

@router.get("/overview", response_model=BaseResponse)
async def get_analytics_overview(auth: ApiKeyRecord = Depends(verify_api_key)):
    return BaseResponse(
        data={
            "counters": metrics.counters,
            "active_audio_players": multi_player_manager.count_active_players(),
            "system_resources": sys_monitor.get_system_metrics()
        }
    )

