"""
CSE Aspirant - AI Commands Handler
"""
from typing import Dict, Any
from ai.chatbot import ai_chatbot
from ai.assistant import ai_assistant
from ai.code_solver import ai_code_solver
from ai.math_solver import ai_math_solver
from ai.summarizer import ai_summarizer

async def handle_ai_chat(prompt: str) -> Dict[str, Any]:
    if not prompt:
        return {"text": "🤖 Please ask something! Example: `/ai What is the CAP theorem?`"}
    ans = await ai_chatbot.chat(prompt)
    return {"text": ans}

async def handle_ai_ask(question: str) -> Dict[str, Any]:
    if not question:
        return {"text": "❓ Please provide your question! Example: `/ask Difference between TCP and UDP`"}
    ans = await ai_assistant.answer_question(question)
    return {"text": ans}

async def handle_ai_code(problem: str, language: str = "python") -> Dict[str, Any]:
    if not problem:
        return {"text": "💻 Example: `/code reverse a linked list`"}
    res = await ai_code_solver.solve(problem, language)
    return {"text": res["solution"]}

async def handle_ai_debug(code: str) -> Dict[str, Any]:
    if not code:
        return {"text": "🛠 Please provide code to debug! Example: `/debug print(x)`"}
    res = await ai_code_solver.debug(code)
    return {"text": res["analysis"]}

async def handle_ai_math(problem: str) -> Dict[str, Any]:
    if not problem:
        return {"text": "🧮 Example: `/math integrate x^2 dx from 0 to 3`"}
    res = await ai_math_solver.solve(problem)
    return {"text": res["steps"]}

async def handle_ai_summarize(text: str) -> Dict[str, Any]:
    if not text:
        return {"text": "📄 Example: `/summarize <insert notes or text>`"}
    summary = await ai_summarizer.summarize(text)
    return {"text": f"📋 **Summary Key Takeaways**:\n\n{summary}"}

