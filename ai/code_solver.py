"""
CSE Aspirant - AI Code Solver & Debugger
"""
from typing import Dict, Any
from ai.engine import ai_engine

class AICodeSolver:
    async def solve(self, problem: str, language: str = "python") -> Dict[str, Any]:
        system = f"Expert programmer solving technical problems in {language} with optimal complexity."
        explanation = await ai_engine.generate_response(system, f"Solve in {language}: {problem}")
        return {
            "language": language,
            "problem": problem,
            "solution": explanation,
            "status": "success"
        }

    async def debug(self, code: str, language: str = "python", error_log: str = "") -> Dict[str, Any]:
        prompt = f"Fix this {language} code:\n```{language}\n{code}\n```\nError: {error_log}"
        debugged = await ai_engine.generate_response("Expert Software Debugger", prompt)
        return {
            "original_code": code,
            "language": language,
            "analysis": debugged
        }

ai_code_solver = AICodeSolver()
