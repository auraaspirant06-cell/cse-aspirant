"""
CSE Aspirant - AI Notes & Article Summarizer
"""
from ai.engine import ai_engine

class AINotesSummarizer:
    async def summarize(self, text: str, max_points: int = 5) -> str:
        prompt = f"Summarize the following study material into {max_points} high-yield key revision points:\n\n{text}"
        return await ai_engine.generate_response("Academic Summarization Specialist", prompt)

ai_summarizer = AINotesSummarizer()
