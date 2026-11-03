"""
CSE Aspirant - Previous Year Questions & Solutions (UPSC & GATE/CSE)
"""
from typing import List, Dict

class PYQRepository:
    def __init__(self):
        self.pyq_list = [
            {
                "id": "UPSC-2023-GS1",
                "exam": "UPSC Civil Services",
                "subject": "History & Culture",
                "question_en": "Explain the role of geographical factors towards the development of Ancient India.",
                "question_hi": "प्राचीन भारत के विकास में भौगोलिक कारकों की भूमिका की व्याख्या कीजिए।",
                "solution_en": "Himalayas as northern barrier, Indo-Gangetic plains providing agricultural surplus, monsoonal trade routes in the Indian Ocean.",
                "solution_hi": "उत्तरी ढाल के रूप में हिमालय, सिंधु-गंगा के उपजाऊ मैदान, और हिंद महासागर के मानसूनी व्यापार मार्ग।"
            },
            {
                "id": "GATE-CS-OS",
                "exam": "GATE Computer Science",
                "subject": "Operating Systems",
                "question_en": "What are the four necessary conditions for Deadlock to occur?",
                "question_hi": "डेडलॉक उत्पन्न होने के लिए आवश्यक चार शर्तें क्या हैं?",
                "solution_en": "1. Mutual Exclusion, 2. Hold and Wait, 3. No Preemption, 4. Circular Wait (Coffman Conditions).",
                "solution_hi": "1. परस्पर अपवर्जन, 2. होल्ड एंड वेट, 3. नो प्रीएम्पशन, 4. वृत्ताकार प्रतीक्षा (कॉफमैन शर्तें)।"
            }
        ]

    def get_pyqs(self, subject: str = "", lang: str = "en") -> List[Dict[str, str]]:
        lang = "hi" if lang.lower() == "hi" else "en"
        results = []
        for item in self.pyq_list:
            if not subject or subject.lower() in item["subject"].lower() or subject.lower() in item["exam"].lower():
                results.append({
                    "id": item["id"],
                    "exam": item["exam"],
                    "subject": item["subject"],
                    "question": item[f"question_{lang}"],
                    "solution": item[f"solution_{lang}"]
                })
        return results

pyq_repo = PYQRepository()
