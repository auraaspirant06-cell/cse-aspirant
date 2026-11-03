"""
CSE Aspirant - Python Course (Basic to Advanced)
"""
from typing import Dict, Any

class PythonCourse:
    def get_lesson(self, topic: str = "concurrency", lang: str = "en") -> Dict[str, Any]:
        lang = "hi" if lang.lower() == "hi" else "en"
        return {
            "language": "Python",
            "topic": "AsyncIO & Coroutines" if lang == "en" else "असिंक्रोनस प्रोग्रामिंग और कोरूटीन्स",
            "explanation": (
                "AsyncIO enables non-blocking event-driven concurrency in Python using an event loop."
                if lang == "en" else
                "AsyncIO पायथन में इवेंट लूप की सहायता से नॉन-ब्लॉकिंग कॉनकरेंसी प्रदान करता है।"
            ),
            "code_example": (
                "import asyncio\n\n"
                "async def fetch_data(id: int):\n"
                "    await asyncio.sleep(0.1)\n"
                "    return f'Result {id}'\n\n"
                "async def main():\n"
                "    results = await asyncio.gather(*(fetch_data(i) for i in range(3)))\n"
                "    print(results)\n\n"
                "asyncio.run(main())"
            ),
            "output": "['Result 0', 'Result 1', 'Result 2']",
            "exercise": (
                "Write an async task that downloads 5 URLs concurrently with timeout of 2 seconds."
                if lang == "en" else
                "एक असिंक्रोनस प्रोग्राम लिखें जो 2 सेकंड के टाइमआउट के साथ 5 URLs को समानांतर में लोड करे।"
            ),
            "quiz": {
                "question": "Which keyword is used to pause execution until a coroutine completes?" if lang == "en" else "कोरूटीन पूर्ण होने तक निष्पादन को रोकने के लिए किस कीवर्ड का उपयोग किया जाता है?",
                "options": ["yield", "await", "defer", "pause"],
                "correct_index": 1
            }
        }

python_course = PythonCourse()
