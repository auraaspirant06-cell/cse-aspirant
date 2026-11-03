"""
CSE Aspirant - Verification Captcha for Anti-Raid
"""
import random
from typing import Dict, Any

class WelcomeCaptcha:
    def generate_math_captcha(self, user_id: int) -> Dict[str, Any]:
        a = random.randint(2, 9)
        b = random.randint(1, 9)
        ans = a + b
        return {
            "user_id": user_id,
            "question": f"To enter, please solve: {a} + {b} = ?",
            "expected": ans,
            "options": [ans - 1, ans, ans + 2, ans + 1]
        }

welcome_captcha = WelcomeCaptcha()

