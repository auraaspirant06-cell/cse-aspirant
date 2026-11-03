"""
CSE Aspirant - C Programming Course
"""
from typing import Dict, Any

class CCourse:
    def get_lesson(self, topic: str = "pointers", lang: str = "en") -> Dict[str, Any]:
        lang = "hi" if lang.lower() == "hi" else "en"
        return {
            "language": "C",
            "topic": "Pointers & Dynamic Memory" if lang == "en" else "पॉइंटर्स और डायनेमिक मेमोरी मैनेजमेंट",
            "explanation": (
                "Pointers store memory addresses of variables, unlocking manual heap memory allocation via malloc and free."
                if lang == "en" else
                "पॉइंटर्स वेरिएबल्स के मेमोरी एड्रेस को स्टोर करते हैं तथा malloc और free द्वारा हीप मेमोरी का सीधा नियंत्रण देते हैं।"
            ),
            "code_example": (
                "#include <stdio.h>\n"
                "#include <stdlib.h>\n\n"
                "int main() {\n"
                "    int *ptr = (int*)malloc(sizeof(int));\n"
                "    *ptr = 42;\n"
                "    printf(\"Value: %d\\n\", *ptr);\n"
                "    free(ptr);\n"
                "    return 0;\n"
                "}"
            ),
            "output": "Value: 42",
            "exercise": (
                "Create a singly linked list node structure and write an insert_head function."
                if lang == "en" else
                "एक सिंगल लिंक्ड लिस्ट नोड स्ट्रक्चर बनाएं और insert_head फंक्शन लिखें।"
            ),
            "quiz": {
                "question": "Which function deallocates memory allocated by malloc()?" if lang == "en" else "malloc() द्वारा आवंटित मेमोरी को मुक्त करने के लिए कौन सा फंक्शन उपयोग होता है?",
                "options": ["delete()", "free()", "dealloc()", "release()"],
                "correct_index": 1
            }
        }

c_course = CCourse()
