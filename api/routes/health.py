"""
CSE Aspirant - API Health & Metrics Endpoints
"""
from fastapi import APIRouter, Response
from monitoring.health import health_checker
from monitoring.metrics import metrics

router = APIRouter(tags=["Health & Monitoring"])

@router.get("/health")
async def get_health():
    return await health_checker.run_checks()

@router.get("/metrics")
async def get_prometheus_metrics():
    return Response(content=metrics.to_prometheus(), media_type="text/plain")

