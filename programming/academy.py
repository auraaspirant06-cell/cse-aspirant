"""
CSE Aspirant - Central Programming Academy
"""
from typing import Dict, Any, List
from programming.python_course import python_course
from programming.golang_course import golang_course
from programming.c_course import c_course
from programming.cpp_course import cpp_course
from programming.java_course import java_course
from programming.js_course import js_course

class ProgrammingAcademy:
    def __init__(self):
        self.courses = {
            "python": python_course,
            "golang": golang_course,
            "c": c_course,
            "cpp": cpp_course,
            "java": java_course,
            "javascript": js_course
        }

    def get_lesson(self, language: str, topic: str = "", lang: str = "en") -> Dict[str, Any]:
        course = self.courses.get(language.lower())
        if not course:
            return python_course.get_lesson(topic, lang)
        return course.get_lesson(topic, lang)

    def list_available_languages(self) -> List[str]:
        return list(self.courses.keys())

programming_academy = ProgrammingAcademy()

