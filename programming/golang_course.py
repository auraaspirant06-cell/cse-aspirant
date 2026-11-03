"""
CSE Aspirant - Golang Course (Basic to Advanced)
"""
from typing import Dict, Any

class GolangCourse:
    def get_lesson(self, topic: str = "concurrency", lang: str = "en") -> Dict[str, Any]:
        lang = "hi" if lang.lower() == "hi" else "en"
        return {
            "language": "Golang",
            "topic": "Goroutines & Channels" if lang == "en" else "गोरूटीन्स और चैनल्स",
            "explanation": (
                "Go provides lightweight execution threads managed by the Go runtime, communicating via typed channels."
                if lang == "en" else
                "Go रनटाइम द्वारा प्रबंधित हल्के निष्पादन थ्रेड्स (गोरूटीन्स) प्रदान करता है जो चैनल्स के माध्यम से संवाद करते हैं।"
            ),
            "code_example": (
                "package main\n\n"
                "import (\n\t\"fmt\"\n)\n\n"
                "func main() {\n"
                "\tch := make(chan string)\n"
                "\tgo func() { ch <- \"Hello CSE Aspirant!\" }()\n"
                "\tmsg := <-ch\n"
                "\tfmt.Println(msg)\n"
                "}"
            ),
            "output": "Hello CSE Aspirant!",
            "exercise": (
                "Implement a worker pool with 4 workers processing an audio ring buffer."
                if lang == "en" else
                "ऑडियो रिंग बफर को प्रोसेस करने के लिए 4 वर्कर्स का एक वर्कर पूल बनाएं।"
            ),
            "quiz": {
                "question": "Which operator is used to send data into a channel?" if lang == "en" else "चैनल में डेटा भेजने के लिए किस ऑपरेटर का उपयोग किया जाता है?",
                "options": ["<-", "->", ":=", "=>"],
                "correct_index": 0
            }
        }

golang_course = GolangCourse()
