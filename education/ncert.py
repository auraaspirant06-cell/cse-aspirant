"""
CSE Aspirant - NCERT Foundation Summaries (Hindi & English)
"""
from typing import Dict, Any

class NCERTModule:
    def __init__(self):
        self.ncert_data = {
            "history": {
                "en": "Ancient India (R.S. Sharma), Medieval India (Satish Chandra), Modern India (Bipan Chandra) & Themes in Indian History I-III.",
                "hi": "प्राचीन भारत (आर. एस. शर्मा), मध्यकालीन भारत (सतीश चंद्र), आधुनिक भारत (बिपिन चंद्र) एवं भारतीय इतिहास के कुछ विषय (भाग 1-3)।"
            },
            "polity": {
                "en": "Class 11: Indian Constitution at Work & Political Theory; Class 12: Politics in India since Independence.",
                "hi": "कक्षा 11: भारत का संविधान - सिद्धांत और व्यवहार; कक्षा 12: स्वतंत्र भारत में राजनीति।"
            },
            "geography": {
                "en": "Class 11: Fundamentals of Physical Geography & India: Physical Environment; Class 12: Fundamentals of Human Geography.",
                "hi": "कक्षा 11: भौतिक भूगोल के मूल सिद्धांत व भारत: भौतिक पर्यावरण; कक्षा 12: मानव भूगोल के मूल सिद्धांत।"
            },
            "economics": {
                "en": "Class 11: Indian Economic Development; Class 12: Introductory Macroeconomics.",
                "hi": "कक्षा 11: भारतीय अर्थव्यवस्था का विकास; कक्षा 12: समष्टि अर्थशास्त्र - एक परिचय।"
            }
        }

    def get_summary(self, subject: str, lang: str = "en") -> str:
        lang = "hi" if lang.lower() == "hi" else "en"
        data = self.ncert_data.get(subject.lower(), self.ncert_data["history"])
        return data.get(lang, data["en"])

ncert_module = NCERTModule()
