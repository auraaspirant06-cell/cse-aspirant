"""
CSE Aspirant - Content Moderation & Copyright Filter
"""
import re
from typing import Tuple, Optional

class ContentModerator:
    # Toxic, abusive, and explicit patterns
    ABUSE_KEYWORDS = {
        "nude", "porn", "xxx", "nsfw", "sex", "scam", "crypto pump", "free nitro",
        "casino", "betting", "hack tool", "malware", "telegram leaked"
    }

    COPYRIGHT_PATTERNS = [
        re.compile(r"copyrighted material reserved", re.IGNORECASE),
        re.compile(r"dmca infringement sample", re.IGNORECASE)
    ]

    def inspect_text(self, text: str) -> Tuple[bool, Optional[str]]:
        if not text:
            return True, None
        
        lower = text.lower()
        for word in self.ABUSE_KEYWORDS:
            if word in lower:
                return False, f"Prohibited or explicit content detected ('{word}')"

        for pat in self.COPYRIGHT_PATTERNS:
            if pat.search(text):
                return False, "Copyright violation detected"

        return True, None

content_moderator = ContentModerator()

