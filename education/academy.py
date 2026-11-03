"""
CSE Aspirant Academy - Central Coordinator
"""
from typing import Dict, Any
from education.upsc import upsc_module
from education.cs_core import cs_core
from education.ncert import ncert_module
from education.notes import notes_library
from education.current_affairs import current_affairs
from education.pyq import pyq_repo
from education.quiz import quiz_engine
from education.planner import study_planner

class AcademyCoordinator:
    def get_dashboard_summary(self, lang: str = "en") -> Dict[str, Any]:
        return {
            "upsc_strategy": upsc_module.get_strategy(lang),
            "latest_news": current_affairs.get_latest(lang),
            "active_quizzes": len(quiz_engine.quizzes),
            "curated_books": len(notes_library.library),
            "planner_ready": True
        }

academy = AcademyCoordinator()
