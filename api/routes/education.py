"""
CSE Aspirant - Education & Academy API Endpoints
"""
from fastapi import APIRouter, Query
from api.schemas import BaseResponse
from education.academy import academy
from education.upsc import upsc_module
from education.cs_core import cs_core
from education.quiz import quiz_engine
from education.planner import study_planner

router = APIRouter(prefix="/api/v1/education", tags=["Academy"])

@router.get("/summary", response_model=BaseResponse)
async def get_academy_summary(lang: str = Query("en", regex="^(en|hi)$")):
    return BaseResponse(data=academy.get_dashboard_summary(lang))

@router.get("/upsc/strategy", response_model=BaseResponse)
async def get_upsc_strategy(lang: str = Query("en", regex="^(en|hi)$")):
    return BaseResponse(data={"strategy": upsc_module.get_strategy(lang)})

@router.get("/cs/{subject}", response_model=BaseResponse)
async def get_cs_subject(subject: str, lang: str = Query("en", regex="^(en|hi)$")):
    return BaseResponse(data={"overview": cs_core.get_subject_overview(subject, lang)})

@router.get("/quiz/random", response_model=BaseResponse)
async def get_quiz():
    return BaseResponse(data=quiz_engine.get_quiz())

@router.get("/planner", response_model=BaseResponse)
async def get_planner(exam: str = "UPSC", hours: int = 8, lang: str = "en"):
    return BaseResponse(data=study_planner.generate_daily_schedule(exam, hours, lang))

