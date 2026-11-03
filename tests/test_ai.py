"""
Unit Tests for AI System Modules
"""
import pytest
from ai.chatbot import ai_chatbot
from ai.code_solver import ai_code_solver
from ai.math_solver import ai_math_solver
from ai.summarizer import ai_summarizer
from ai.assistant import ai_assistant

@pytest.mark.asyncio
async def test_ai_chatbot_response():
    resp = await ai_chatbot.chat("What is an Operating System?")
    assert len(resp) > 0
    assert "CSE Aspirant AI" in resp or "Operating System" in resp

@pytest.mark.asyncio
async def test_ai_code_solver():
    res = await ai_code_solver.solve("Sort an array in ascending order", "python")
    assert res["status"] == "success"
    assert "def solve_problem" in res["solution"]

@pytest.mark.asyncio
async def test_ai_math_solver():
    res = await ai_math_solver.solve("integrate x dx")
    assert res["verified"] is True
    assert "Mathematical Solution" in res["steps"]

@pytest.mark.asyncio
async def test_ai_summarizer():
    summary = await ai_summarizer.summarize("Long notes about Indian Polity and Preamble.")
    assert len(summary) > 0

@pytest.mark.asyncio
async def test_ai_resource_finder():
    resources = await ai_assistant.find_resources("Database Normalization")
    assert len(resources) >= 2
    assert "link" in resources[0]

