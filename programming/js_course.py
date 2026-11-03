"""
CSE Aspirant - JavaScript Programming Course
"""
from typing import Dict, Any

class JavaScriptCourse:
    def get_lesson(self, topic: str = "event_loop", lang: str = "en") -> Dict[str, Any]:
        lang = "hi" if lang.lower() == "hi" else "en"
        return {
            "language": "JavaScript",
            "topic": "Event Loop & Promises" if lang == "en" else "इवेंट लूप और प्रॉमिस",
            "explanation": (
                "JavaScript runtime features a single-threaded non-blocking event loop orchestrating the call stack, microtask queue, and macrotask queue."
                if lang == "en" else
                "जावास्क्रिप्ट सिंगल-थ्रेडेड नॉन-ब्लॉकिंग इवेंट लूप का उपयोग करती है जो कॉल स्टैक, माइक्रो-टास्क और मैक्रो-टास्क क्यू को प्रबंधित करता है।"
            ),
            "code_example": (
                "console.log('1: Start');\n\n"
                "setTimeout(() => console.log('2: Macrotask (Timer)'), 0);\n\n"
                "Promise.resolve().then(() => console.log('3: Microtask (Promise)'));\n\n"
                "console.log('4: End');"
            ),
            "output": "1: Start\n4: End\n3: Microtask (Promise)\n2: Macrotask (Timer)",
            "exercise": (
                "Write an async function with Promise.allSettled() handling multiple API calls safely."
                if lang == "en" else
                "एक असिंक्रोनस फंक्शन लिखें जो कई एपीआई कॉल्स को Promise.allSettled() के जरिए सुरक्षित रूप से संभाले।"
            ),
            "quiz": {
                "question": "Which queue has higher priority in JavaScript event loop?" if lang == "en" else "जावास्क्रिप्ट इवेंट लूप में किस कतार को उच्च प्राथमिकता मिलती है?",
                "options": ["Macrotask Queue", "Microtask Queue", "Timer Queue", "I/O Polling Queue"],
                "correct_index": 1
            }
        }

js_course = JavaScriptCourse()

