"""
CSE Aspirant - C++ Programming Course
"""
from typing import Dict, Any

class CPPCourse:
    def get_lesson(self, topic: str = "stl", lang: str = "en") -> Dict[str, Any]:
        lang = "hi" if lang.lower() == "hi" else "en"
        return {
            "language": "C++",
            "topic": "Standard Template Library (STL)" if lang == "en" else "स्टैंडर्ड टेम्पलेट लाइब्रेरी (STL)",
            "explanation": (
                "STL provides powerful template classes for algorithms, containers (vectors, maps), and iterators."
                if lang == "en" else
                "STL कंटेनर्स (वेक्टर, मैप), एल्गोरिदम और इटरेटर्स के लिए शक्तिशाली जेनेरिक कक्षाएं प्रदान करता है।"
            ),
            "code_example": (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <algorithm>\n\n"
                "int main() {\n"
                "    std::vector<int> nums = {4, 1, 8, 3};\n"
                "    std::sort(nums.begin(), nums.end());\n"
                "    for (int n : nums) std::cout << n << \" \";\n"
                "    return 0;\n"
                "}"
            ),
            "output": "1 3 4 8",
            "exercise": (
                "Implement a frequency counter of words using std::unordered_map."
                if lang == "en" else
                "std::unordered_map का उपयोग करके शब्दों की आवृत्ति गिनने वाला प्रोग्राम लिखें।"
            ),
            "quiz": {
                "question": "What is the average time complexity of lookup in std::unordered_map?" if lang == "en" else "std::unordered_map में लुकअप की औसत समय जटिलता क्या है?",
                "options": ["O(1)", "O(log N)", "O(N)", "O(N log N)"],
                "correct_index": 0
            }
        }

cpp_course = CPPCourse()
