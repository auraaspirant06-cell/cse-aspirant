"""
CSE Aspirant - Interactive Quiz & Mock Test Engine
"""
from typing import List, Dict, Any, Optional

class QuizEngine:
    def __init__(self):
        self.quizzes: List[Dict[str, Any]] = [
            {
                "id": "q1",
                "category": "UPSC Polity",
                "question_en": "Which Article of the Indian Constitution deals with the Right to Constitutional Remedies?",
                "question_hi": "भारतीय संविधान का कौन सा अनुच्छेद 'संवैधानिक उपचारों के अधिकार' से संबंधित है?",
                "options": ["Article 21", "Article 32", "Article 44", "Article 370"],
                "correct_index": 1,
                "explanation_en": "Article 32 is termed the 'Heart and Soul of the Constitution' by Dr. B.R. Ambedkar.",
                "explanation_hi": "डॉ. बी.आर. अंबेडकर ने अनुच्छेद 32 को 'संविधान का हृदय और आत्मा' कहा था।"
            },
            {
                "id": "q2",
                "category": "Computer Science",
                "question_en": "What is the worst-case time complexity of QuickSort?",
                "question_hi": "क्विकसॉर्ट (QuickSort) की सबसे खराब समय जटिलता (Worst-case time complexity) क्या है?",
                "options": ["O(N log N)", "O(N)", "O(N^2)", "O(log N)"],
                "correct_index": 2,
                "explanation_en": "When pivot selection is unbalanced (e.g. already sorted list with last element as pivot), QuickSort degenerates to O(N^2).",
                "explanation_hi": "जब पिवट का चयन असंतुलित होता है, तब क्विकसॉर्ट O(N^2) जटिलता में बदल जाता है।"
            }
        ]

    def get_quiz(self, quiz_id: Optional[str] = None) -> Dict[str, Any]:
        if quiz_id:
            for q in self.quizzes:
                if q["id"] == quiz_id:
                    return q
        return self.quizzes[0]

    def verify_answer(self, quiz_id: str, selected_index: int, lang: str = "en") -> Dict[str, Any]:
        lang = "hi" if lang.lower() == "hi" else "en"
        quiz = self.get_quiz(quiz_id)
        is_correct = (quiz["correct_index"] == selected_index)
        return {
            "quiz_id": quiz_id,
            "is_correct": is_correct,
            "correct_option": quiz["options"][quiz["correct_index"]],
            "explanation": quiz[f"explanation_{lang}"]
        }

quiz_engine = QuizEngine()
