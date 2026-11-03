"""
Unit Tests for Education & CSE Academy Modules
"""
import pytest
from education.upsc import upsc_module
from education.cs_core import cs_core
from education.ncert import ncert_module
from education.current_affairs import current_affairs
from education.pyq import pyq_repo
from education.quiz import quiz_engine
from education.planner import study_planner

def test_upsc_bilingual_notes():
    en_notes = upsc_module.get_subject_notes("prelims", "en")
    hi_notes = upsc_module.get_subject_notes("prelims", "hi")
    assert "General Studies" in en_notes
    assert "सामान्य अध्ययन" in hi_notes

def test_cs_core_overview():
    os_info = cs_core.get_subject_overview("os", "en")
    assert "Operating Systems" in os_info
    assert "Deadlocks" in os_info

def test_ncert_foundation():
    hist = ncert_module.get_summary("history", "en")
    assert "Ancient India" in hist

def test_current_affairs():
    ca = current_affairs.get_latest("en")
    assert len(ca) >= 2
    assert "Semiconductor" in ca[0]["title"] or "Climate" in ca[1]["title"]

def test_pyq_repository():
    pyqs = pyq_repo.get_pyqs("Operating Systems", "en")
    assert len(pyqs) >= 1
    assert "Deadlock" in pyqs[0]["question"]

def test_quiz_engine():
    q = quiz_engine.get_quiz("q1")
    assert q["id"] == "q1"
    
    # Verify correct answer
    res_correct = quiz_engine.verify_answer("q1", selected_index=1, lang="en")
    assert res_correct["is_correct"] is True
    assert "Article 32" in res_correct["correct_option"]

    # Verify wrong answer
    res_wrong = quiz_engine.verify_answer("q1", selected_index=0, lang="en")
    assert res_wrong["is_correct"] is False

def test_study_planner():
    plan = study_planner.generate_daily_schedule(target_exam="UPSC", hours_available=10, lang="en")
    assert plan["target_exam"] == "UPSC"
    assert len(plan["sessions"]) >= 4

