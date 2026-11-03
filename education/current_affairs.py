"""
CSE Aspirant - Daily & Monthly Current Affairs (Hindi & English)
"""
from typing import List, Dict
from datetime import datetime

class CurrentAffairsModule:
    def __init__(self):
        self.digest = [
            {
                "date": "November 2026",
                "title_en": "India's Semiconductor Mission: 2nm Fabrication Milestone",
                "title_hi": "भारत का सेमीकंडक्टर मिशन: 2nm फैब्रिकेशन की ऐतिहासिक उपलब्धि",
                "summary_en": "Critical for GS Paper 3 (Sci-Tech) and CS Aspirants studying micro-architecture.",
                "summary_hi": "जीएस पेपर 3 (विज्ञान एवं प्रौद्योगिकी) और कंप्यूटर आर्किटेक्चर के लिए महत्वपूर्ण।"
            },
            {
                "date": "November 2026",
                "title_en": "Global Climate Adaptation Pact & Renewable Energy Grid",
                "title_hi": "वैश्विक जलवायु अनुकूलन समझौता और नवीकरणीय ऊर्जा ग्रिड",
                "summary_en": "High probability topic for GS Paper 3 Environment and International Conventions.",
                "summary_hi": "जीएस पेपर 3 पर्यावरण एवं अंतर्राष्ट्रीय सम्मेलनों के लिए उच्च प्राथमिकता वाला विषय।"
            }
        ]

    def get_latest(self, lang: str = "en") -> List[Dict[str, str]]:
        lang = "hi" if lang.lower() == "hi" else "en"
        return [
            {
                "date": item["date"],
                "title": item[f"title_{lang}"],
                "summary": item[f"summary_{lang}"]
            }
            for item in self.digest
        ]

current_affairs = CurrentAffairsModule()
