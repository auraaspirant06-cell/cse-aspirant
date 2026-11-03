"""
CSE Aspirant - Programming Commands Handler
"""
from typing import Dict, Any
from programming.academy import programming_academy

async def handle_programming() -> Dict[str, Any]:
    langs = programming_academy.list_available_languages()
    text = (
        "💻 **CSE PROGRAMMING ACADEMY** 💻\n\n"
        "Master industry & competitive programming from scratch to advanced!\n\n"
        "Available Language Tracks:\n"
        + "\n".join(f"• `/{l}` : {l.upper()} Complete Course" for l in langs)
        + "\n\nEvery track includes bilingual explanations, examples, output, exercises & quizzes!"
    )
    return {"text": text}

async def handle_lang_course(lang_code: str, topic: str = "", lang: str = "en") -> Dict[str, Any]:
    lesson = programming_academy.get_lesson(lang_code, topic, lang)
    text = (
        f"🖥 **{lesson['language']} Masterclass** : {lesson['topic']}\n\n"
        f"📖 **Concept**:\n{lesson['explanation']}\n\n"
        f"📝 **Code Example**:\n```\n{lesson['code_example']}\n```\n\n"
        f"📤 **Output**:\n```\n{lesson['output']}\n```\n\n"
        f"🎯 **Hands-On Exercise**:\n{lesson['exercise']}\n\n"
        f"🧠 **Quick Quiz**:\n{lesson['quiz']['question']}\n"
        + "\n".join(f"{i+1}. {opt}" for i, opt in enumerate(lesson['quiz']['options']))
    )
    return {"text": text}

