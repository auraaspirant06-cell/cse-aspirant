"""
CSE Aspirant - Automated Moderation Rules Engine
"""
from typing import Tuple, Optional
from security.anti_flood import anti_flood
from security.anti_spam import anti_spam
from security.content_filter import content_moderator
from security.url_scanner import url_scanner

class ModerationRulesEngine:
    def check_message(self, user_id: int, text: str) -> Tuple[bool, Optional[str]]:
        if anti_flood.is_flooding(user_id):
            return False, "Message rejected: Anti-flood limit exceeded."

        if anti_spam.is_spam(user_id, text):
            return False, "Message rejected: Repeated spam detected."

        ok, reason = content_moderator.inspect_text(text)
        if not ok:
            return False, f"Message rejected: {reason}"

        ok, reason = url_scanner.scan_urls(text)
        if not ok:
            return False, f"Message rejected: {reason}"

        return True, None

moderation_rules = ModerationRulesEngine()

