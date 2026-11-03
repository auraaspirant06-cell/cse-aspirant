"""
CSE Aspirant - Help Callbacks Handler
"""
from typing import Dict, Any

class HelpCallbackHandler:
    def __init__(self):
        self.help_texts = {
            "help_music": (
                "🎵 **MUSIC ENGINE COMMANDS**\n\n"
                "• `[prefix]play <query/url>` : Play YouTube, direct stream or search\n"
                "• `[prefix]pause` : Pause ongoing stream\n"
                "• `[prefix]resume` : Resume paused track\n"
                "• `[prefix]skip` : Jump to next track in queue\n"
                "• `[prefix]prev` : Play previous track\n"
                "• `[prefix]stop` : Clear queue and stop playback\n"
                "• `[prefix]queue` : Display current queue\n"
                "• `[prefix]shuffle` : Shuffle active queue\n"
                "• `[prefix]repeat <off/one/all>` : Set loop mode\n"
                "• `[prefix]volume <0-200>` : Adjust output volume\n"
                "• `[prefix]playlist` : Load curated study/coding playlists\n\n"
                "Supports prefixes: `/`, `!`, `.`"
            ),
            "help_education": (
                "📚 **EDUCATION & CSE ACADEMY COMMANDS**\n\n"
                "• `[prefix]education` : View Academy summary & modules\n"
                "• `[prefix]upsc <subject>` : Prelims/Mains syllabus & strategies\n"
                "• `[prefix]cs <os/dbms/cn/dsa>` : Core Computer Science notes\n"
                "• `[prefix]ncert <history/polity/geo>` : NCERT foundations\n"
                "• `[prefix]currentaffairs` : Daily & monthly high-yield digest\n"
                "• `[prefix]pyq <subject>` : Previous year questions with model answers\n"
                "• `[prefix]quiz` : Interactive mock tests & quizzes\n"
                "• `[prefix]planner <exam> <hours>` : Automated study timetable\n\n"
                "Dual-Language: Supports English (EN) and Hindi (HI)."
            ),
            "help_programming": (
                "💻 **PROGRAMMING ACADEMY COMMANDS**\n\n"
                "• `[prefix]python` : Python Basic to Advanced with code & quiz\n"
                "• `[prefix]golang` : Go Concurrency, Goroutines & Channels\n"
                "• `[prefix]c` : C Pointers & Memory Management\n"
                "• `[prefix]cpp` : C++ STL, Templates & OOP\n"
                "• `[prefix]java` : Java JVM, Streams & Multithreading\n"
                "• `[prefix]javascript` : JS Event Loop, Promises & Async\n\n"
                "All lessons include Hindi/English explanations, examples, output & quizzes."
            ),
            "help_ai": (
                "🤖 **AI ASSISTANT COMMANDS**\n\n"
                "• `[prefix]ai <query>` : Intelligent conversational chatbot\n"
                "• `[prefix]ask <question>` : Academic Q&A solver\n"
                "• `[prefix]code <problem>` : Algorithm & code solution generator\n"
                "• `[prefix]debug <code>` : Automated code debugger & analyzer\n"
                "• `[prefix]math <equation>` : Step-by-step mathematical proof\n"
                "• `[prefix]summarize <text>` : High-yield notes summarization"
            ),
            "help_premium": (
                "💎 **PREMIUM & SUBSCRIPTION COMMANDS**\n\n"
                "• `[prefix]premium` : View tier benefits (FREE / PREMIUM / PRO)\n"
                "• `[prefix]pay` : Generate payment QR, UPI intent & NEFT details\n"
                "• `[prefix]submit_utr <12_digit_utr>` : Submit UTR for activation\n"
                "• `[prefix]verify` : Social verification (Telegram / Instagram / YouTube)"
            ),
            "help_security": (
                "🔐 **SECURITY & AUDIT COMMANDS**\n\n"
                "• `[prefix]antispam <on/off>` : Toggle anti-spam velocity filter\n"
                "• `[prefix]antiflood <on/off>` : Toggle rate limiter\n"
                "• `[prefix]audit` : View recent administrative actions & logs\n"
                "• Automatic: NSFW filter, copyright matching, suspicious file blocks."
            ),
            "help_promotion": (
                "📢 **PROMOTION COMMANDS**\n\n"
                "• `[prefix]promote <t.me/channel>` : Submit channel for community spotlight\n"
                "• Submissions are strictly verified & approved by owner before broadcast."
            ),
            "help_owner": (
                "👑 **OWNER PANEL COMMANDS**\n\n"
                "• `[prefix]stats` : Real-time CPU, RAM, active players & user counts\n"
                "• `[prefix]broadcast <msg>` : Send rate-limited announcement to all groups\n"
                "• `[prefix]set_tier <user_id> <tier>` : Manually assign user tier\n"
                "• `[prefix]approve_utr <utr>` : Reconcile payment & issue NextGen API keys"
            )
        }

    def get_help(self, category: str) -> str:
        return self.help_texts.get(category, "Select a category from the buttons below.")

help_cb_handler = HelpCallbackHandler()

