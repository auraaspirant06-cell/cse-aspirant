"""
CSE Aspirant - Anti-Spam Velocity & Duplicate Detector
"""
from typing import Dict
import hashlib

class AntiSpamDetector:
    def __init__(self):
        self._last_messages: Dict[int, str] = {}
        self._spam_counts: Dict[int, int] = {}

    def is_spam(self, user_id: int, message_text: str) -> bool:
        if not message_text:
            return False
        
        msg_hash = hashlib.md5(message_text.strip().encode("utf-8")).hexdigest()
        last_hash = self._last_messages.get(user_id)
        
        if last_hash == msg_hash:
            self._spam_counts[user_id] = self._spam_counts.get(user_id, 0) + 1
            if self._spam_counts[user_id] >= 3:
                return True
        else:
            self._spam_counts[user_id] = 0
            self._last_messages[user_id] = msg_hash

        return False

anti_spam = AntiSpamDetector()

