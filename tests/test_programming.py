"""
Unit Tests for Programming Academy Modules
"""
import pytest
from programming.academy import programming_academy

def test_programming_available_languages():
    langs = programming_academy.list_available_languages()
    assert "python" in langs
    assert "golang" in langs
    assert "c" in langs
    assert "cpp" in langs
    assert "java" in langs
    assert "javascript" in langs

@pytest.mark.parametrize("lang", ["python", "golang", "c", "cpp", "java", "javascript"])
def test_programming_lesson_structure(lang):
    lesson = programming_academy.get_lesson(lang, "", lang="en")
    assert "language" in lesson
    assert "explanation" in lesson
    assert "code_example" in lesson
    assert "output" in lesson
    assert "exercise" in lesson
    assert "quiz" in lesson
    assert len(lesson["quiz"]["options"]) >= 2

def test_programming_hindi_support():
    lesson = programming_academy.get_lesson("python", "", lang="hi")
    assert "पायथन" in lesson["explanation"] or "असिंक्रोनस" in lesson["topic"]

