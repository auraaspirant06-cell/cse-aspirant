"""
CSE Aspirant - Data Repository with In-Memory / PostgreSQL & Redis Support
"""
from typing import Optional, Dict, List
from datetime import datetime, timedelta
import secrets
from database.models import User, Subscription, PaymentRecord, ApiKeyRecord, GroupSetting, PromotionRecord
from database.connection import db_manager
from error_handling.exceptions import PaymentReconciliationError
from core.logger import logger

class Repository:
    def __init__(self):
        self._users: Dict[int, User] = {}
        self._subscriptions: Dict[str, Subscription] = {}
        self._payments: Dict[str, PaymentRecord] = {}  # keyed by UTR
        self._api_keys: Dict[str, ApiKeyRecord] = {}
        self._group_settings: Dict[int, GroupSetting] = {}
        self._promotions: Dict[str, PromotionRecord] = {}
        self._cache: Dict[str, str] = {}

    # User Management
    async def get_or_create_user(self, user_id: int, username: Optional[str] = None, first_name: str = "Aspirant") -> User:
        if user_id not in self._users:
            self._users[user_id] = User(user_id=user_id, username=username, first_name=first_name)
        else:
            if username:
                self._users[user_id].username = username
        return self._users[user_id]

    async def get_user(self, user_id: int) -> Optional[User]:
        return self._users.get(user_id)

    async def update_user_tier(self, user_id: int, tier: str) -> User:
        user = await self.get_or_create_user(user_id)
        user.tier = tier
        user.updated_at = datetime.utcnow()
        return user

    # Payment Management & UTR Submission
    async def submit_payment(self, utr: str, user_id: int, amount: float, method: str, screenshot_url: Optional[str] = None) -> PaymentRecord:
        utr_clean = utr.strip().upper()
        if utr_clean in self._payments:
            raise PaymentReconciliationError(f"Duplicate payment submission! UTR {utr_clean} already registered.")
        
        record = PaymentRecord(
            utr=utr_clean,
            user_id=user_id,
            amount=amount,
            method=method.upper(),
            status="PENDING",
            screenshot_url=screenshot_url
        )
        self._payments[utr_clean] = record
        logger.info(f"Payment recorded: UTR={utr_clean}, user_id={user_id}, amount={amount}")
        return record

    async def get_payment(self, utr: str) -> Optional[PaymentRecord]:
        return self._payments.get(utr.strip().upper())

    async def approve_payment(self, utr: str, approved_by: int) -> PaymentRecord:
        record = await self.get_payment(utr)
        if not record:
            raise PaymentReconciliationError(f"Payment with UTR {utr} not found.")
        if record.status == "APPROVED":
            return record
        
        record.status = "APPROVED"
        record.reconciled_at = datetime.utcnow()
        record.approved_by = approved_by
        
        # Determine tier from amount: e.g. >= 499 -> PRO, >= 199 -> PREMIUM
        tier = "PRO" if record.amount >= 499 else "PREMIUM"
        await self.update_user_tier(record.user_id, tier)

        # Create subscription
        sub_id = secrets.token_hex(8)
        sub = Subscription(
            id=sub_id,
            user_id=record.user_id,
            tier=tier,
            starts_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=30),
            payment_utr=record.utr
        )
        self._subscriptions[sub_id] = sub
        return record

    # API Key Management
    async def generate_api_key(self, user_id: int, tier: str = "FREE") -> ApiKeyRecord:
        key = f"csea_{tier.lower()}_{secrets.token_urlsafe(24)}"
        rate_limits = {"FREE": 10, "PREMIUM": 100, "PRO": 1000}
        record = ApiKeyRecord(
            key=key,
            user_id=user_id,
            tier=tier,
            rate_limit_per_minute=rate_limits.get(tier, 10)
        )
        self._api_keys[key] = record
        return record

    async def get_api_key(self, key: str) -> Optional[ApiKeyRecord]:
        return self._api_keys.get(key)

    async def revoke_api_key(self, key: str) -> bool:
        if key in self._api_keys:
            self._api_keys[key].is_active = False
            return True
        return False

    # Group Settings
    async def get_group_setting(self, chat_id: int) -> GroupSetting:
        if chat_id not in self._group_settings:
            self._group_settings[chat_id] = GroupSetting(chat_id=chat_id)
        return self._group_settings[chat_id]

    async def update_group_setting(self, setting: GroupSetting):
        self._group_settings[setting.chat_id] = setting

    # Promotion Management
    async def create_promotion(self, user_id: int, channel_link: str) -> PromotionRecord:
        promo_id = secrets.token_hex(6)
        promo = PromotionRecord(promo_id=promo_id, user_id=user_id, channel_link=channel_link)
        self._promotions[promo_id] = promo
        return promo

    async def get_promotion(self, promo_id: str) -> Optional[PromotionRecord]:
        return self._promotions.get(promo_id)

    async def update_promotion_status(self, promo_id: str, status: str, reviewed_by: int) -> Optional[PromotionRecord]:
        promo = await self.get_promotion(promo_id)
        if promo:
            promo.status = status
            promo.reviewed_by = reviewed_by
        return promo

    # Cache Operations
    async def set_cache(self, key: str, value: str, expire: int = 300):
        if db_manager.redis_client:
            try:
                await db_manager.redis_client.set(key, value, ex=expire)
                return
            except Exception:
                pass
        self._cache[key] = value

    async def get_cache(self, key: str) -> Optional[str]:
        if db_manager.redis_client:
            try:
                return await db_manager.redis_client.get(key)
            except Exception:
                pass
        return self._cache.get(key)

repo = Repository()
