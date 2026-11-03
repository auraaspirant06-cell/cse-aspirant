"""
CSE Aspirant - AI Chatbot
"""
from ai.engine import ai_engine

class AIChatbot:
    def __init__(self):
        self.system_prompt = (
            "You are CSE Aspirant AI, an elite educational and technical mentor specializing "
            "in Computer Science and UPSC preparation."
        )

    async def chat(self, user_message: str, history: str = "") -> str:
        prompt = f"History: {history}\nUser: {user_message}" if history else user_message
        return await ai_engine.generate_response(self.system_prompt, prompt)

ai_chatbot = AIChatbot()
