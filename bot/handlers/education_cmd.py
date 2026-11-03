"""
CSE Aspirant - Education Commands Handler
"""
from typing import Dict, Any
from education.academy import academy
from education.upsc import upsc_module
from education.cs_core import cs_core
from education.ncert import ncert_module
from education.current_affairs import current_affairs
from education.pyq import pyq_repo
from education.quiz import quiz_engine
from education.planner import study_planner

async def handle_education(lang: str = "en") -> Dict[str, Any]:
    summary = academy.get_dashboard_summary(lang)
    text = (
        "📚 **CSE ASPIRANT ACADEMY** 📚\n\n"
        f"{summary['upsc_strategy']}\n\n"
        f"📖 Available Quizzes: {summary['active_quizzes']} | Curated Books: {summary['curated_books']}\n\n"
        "Commands:\n"
        "• `/upsc <prelims/mains_gs1..4>`\n"
        "• `/cs <os/dbms/cn/dsa>`\n"
        "• `/ncert <history/polity/geo/economics>`\n"
        "• `/currentaffairs`\n"
        "• `/pyq <subject>`\n"
        "• `/quiz`\n"
        "• `/planner`"
    )
    return {"text": text}

async def handle_upsc(subject: str = "prelims", lang: str = "en") -> Dict[str, Any]:
    notes = upsc_module.get_subject_notes(subject, lang)
    return {"text": f"🏛 **UPSC Module ({subject.upper()})**:\n\n{notes}"}

async def handle_cs(subject: str = "os", lang: str = "en") -> Dict[str, Any]:
    overview = cs_core.get_subject_overview(subject, lang)
    return {"text": overview}

async def handle_ncert(subject: str = "history", lang: str = "en") -> Dict[str, Any]:
    summary = ncert_module.get_summary(subject, lang)
    return {"text": f"📘 **NCERT Foundation ({subject.title()})**:\n\n{summary}"}

async def handle_current_affairs(lang: str = "en") -> Dict[str, Any]:
    items = current_affairs.get_latest(lang)
    lines = ["📰 **HIGH-YIELD CURRENT AFFAIRS DIGEST**:\n"]
    for it in items:
        lines.append(f"• **{it['title']}**\n  {it['summary']}\n")
    return {"text": "\n".join(lines)}

async def handle_pyq(subject: str = "", lang: str = "en") -> Dict[str, Any]:
    items = pyq_repo.get_pyqs(subject, lang)
    if not items:
        return {"text": "No previous year questions found for this topic."}
    q = items[0]
    return {
        "text": (
            f"📝 **Previous Year Question ({q['exam']} - {q['subject']})**\n\n"
            f"❓ **Q**: {q['question']}\n\n"
            f"💡 **Model Answer**: {q['solution']}"
        )
    }

async def handle_quiz() -> Dict[str, Any]:
    q = quiz_engine.get_quiz()
    options_str = "\n".join(f"{i+1}. {opt}" for i, opt in enumerate(q["options"]))
    return {
        "text": (
            f"🧠 **Daily Mock Quiz ({q['category']})**\n\n"
            f"{q['question_en']}\n\n"
            f"{options_str}\n\n"
            f"Answer: Option {q['correct_index'] + 1}\n"
            f"Explanation: {q['explanation_en']}"
        )
    }

async def handle_planner(exam: str = "UPSC", hours: str = "8", lang: str = "en") -> Dict[str, Any]:
    try:
        h = int(hours)
    except Exception:
        h = 8
    plan = study_planner.generate_daily_schedule(exam, h, lang)
    lines = [f"📅 **Daily Study Blueprint ({plan['target_exam']})** | {plan['total_hours']} Hours:\n"]
    for s in plan["sessions"]:
        lines.append(f"⏰ `{s['time']}` : {s['task']}")
    lines.append(f"\n💡 *Rule: {plan['pomodoro_guideline']}*")
    return {"text": "\n".join(lines)}

