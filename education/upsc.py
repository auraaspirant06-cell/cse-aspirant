"""
CSE Aspirant - UPSC Preparation Module (Hindi & English)
"""
from typing import Dict, Any, List

class UPSCModule:
    def __init__(self):
        self.syllabus = {
            "prelims": {
                "en": "General Studies I (History, Geography, Polity, Economy, Sci-Tech, Ecology) & CSAT (Paper II).",
                "hi": "सामान्य अध्ययन पेपर-1 (इतिहास, भूगोल, राजव्यवस्था, अर्थव्यवस्था, पर्यावरण) एवं सीसैट पेपर-2।"
            },
            "mains_gs1": {
                "en": "Indian Heritage, Culture, History and Geography of the World and Society.",
                "hi": "भारतीय विरासत और संस्कृति, विश्व का इतिहास एवं भूगोल और समाज।"
            },
            "mains_gs2": {
                "en": "Governance, Constitution, Polity, Social Justice and International Relations.",
                "hi": "शासन व्यवस्था, संविधान, राजव्यवस्था, सामाजिक न्याय और अंतर्राष्ट्रीय संबंध।"
            },
            "mains_gs3": {
                "en": "Technology, Economic Development, Bio-diversity, Environment, Security and Disaster Management.",
                "hi": "प्रौद्योगिकी, आर्थिक विकास, जैव विविधता, पर्यावरण, सुरक्षा तथा आपदा प्रबंधन।"
            },
            "mains_gs4": {
                "en": "Ethics, Integrity, and Aptitude.",
                "hi": "नीतिशास्त्र, सत्यनिष्ठा और अभिरुचि।"
            }
        }

    def get_subject_notes(self, subject_key: str, lang: str = "en") -> str:
        lang = lang.lower() if lang.lower() in ("en", "hi") else "en"
        data = self.syllabus.get(subject_key, self.syllabus["prelims"])
        return data.get(lang, data["en"])

    def get_strategy(self, lang: str = "en") -> str:
        if lang == "hi":
            return (
                "🎯 **UPSC तैयारी की सफल रणनीति**:\n"
                "1. **सिलेबस और PYQ**: सबसे पहले पाठ्यक्रम को कंठस्थ करें और पिछले 10 वर्षों के प्रश्न पत्र देखें।\n"
                "2. **NCERT आधार**: कक्षा 6-12 की NCERT का गहन अध्ययन करें।\n"
                "3. **करेंट अफेयर्स**: दैनिक समाचार पत्र विश्लेषण और मासिक पत्रिका पढ़ें।\n"
                "4. **उत्तर लेखन अभ्यास**: प्रतिदिन 2 मुख्य परीक्षा प्रश्नों का उत्तर लिखें।"
            )
        return (
            "🎯 **UPSC Preparation Master Strategy**:\n"
            "1. **Syllabus & PYQ**: Memorize syllabus and dissect last 10 years Prelims/Mains papers.\n"
            "2. **NCERT Foundation**: Master Class 6-12 NCERTs for conceptual bedrock.\n"
            "3. **Current Affairs**: Daily editorial reading and monthly thematic notes.\n"
            "4. **Answer Writing**: Daily 2 Mains questions with diagrams and structured headings."
        )

upsc_module = UPSCModule()
