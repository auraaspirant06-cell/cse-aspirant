"""
CSE Aspirant - Promotion Request Manager
"""
import re
from typing import Optional
from database.repository import repo
from database.models import PromotionRecord
from error_handling.exceptions import CSEAspirantException

class PromotionManager:
    LINK_REGEX = re.compile(r"^(https?://)?(t\.me|telegram\.me)/([a-zA-Z0-9_]{4,32})|@([a-zA-Z0-9_]{4,32})$")

    def validate_link(self, link: str) -> bool:
        return bool(self.LINK_REGEX.match(link.strip()))

    async def submit_promotion(self, user_id: int, channel_link: str) -> PromotionRecord:
        clean_link = channel_link.strip()
        if not self.validate_link(clean_link):
            raise CSEAspirantException(
                "Invalid Telegram link! Please provide a valid link (e.g. https://t.me/yourchannel or @yourchannel)."
            )
        return await repo.create_promotion(user_id, clean_link)

promotion_manager = PromotionManager()

