"""
CSE Aspirant - Java Programming Course
"""
from typing import Dict, Any

class JavaCourse:
    def get_lesson(self, topic: str = "streams", lang: str = "en") -> Dict[str, Any]:
        lang = "hi" if lang.lower() == "hi" else "en"
        return {
            "language": "Java",
            "topic": "Java Streams & Lambdas" if lang == "en" else "जावा स्ट्रीम्स और लैम्ब्डा एक्सप्रेशन्स",
            "explanation": (
                "Streams API provides a declarative pipeline to process collections of objects with filtering, mapping, and reduction."
                if lang == "en" else
                "जावा स्ट्रीम्स एपीआई ऑब्जेक्ट्स के संग्रह को फिल्टर, मैप और रिड्यूस करने के लिए एक आधुनिक घोषणात्मक पाइपलाइन प्रदान करती है।"
            ),
            "code_example": (
                "import java.util.*;\n"
                "import java.util.stream.*;\n\n"
                "public class StreamDemo {\n"
                "    public static void main(String[] args) {\n"
                "        List<String> names = Arrays.asList(\"Aspirant\", \"CSE\", \"IAS\", \"GATE\");\n"
                "        List<String> filtered = names.stream()\n"
                "            .filter(s -> s.length() <= 4)\n"
                "            .collect(Collectors.toList());\n"
                "        System.out.println(filtered);\n"
                "    }\n"
                "}"
            ),
            "output": "[CSE, IAS, GATE]",
            "exercise": (
                "Create a stream pipeline that sums the squares of even numbers in an array."
                if lang == "en" else
                "एक स्ट्रीम पाइपलाइन बनाएं जो किसी ऐरे में सम संख्याओं के वर्गों का योग करे।"
            ),
            "quiz": {
                "question": "Which method is a terminal operation in Java Streams?" if lang == "en" else "जावा स्ट्रीम में कौन सी विधि एक टर्मिनल ऑपरेशन है?",
                "options": ["filter()", "map()", "collect()", "peek()"],
                "correct_index": 2
            }
        }

java_course = JavaCourse()

