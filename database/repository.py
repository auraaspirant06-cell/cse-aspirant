"""
CSE Aspirant - Data Repository with In-Memory / PostgreSQL & Redis Support
"""
from typing import Any, Optional, Dict, List
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

    @property
    def _persistent(self) -> bool:
        return db_manager.pg_pool is not None

    @property
    def _pool(self) -> Any:
        return db_manager.pg_pool

    @staticmethod
    def _user_from_row(row: Any) -> User:
        return User(
            user_id=row["user_id"],
            username=row["username"],
            first_name=row["first_name"],
            tier=row["tier"],
            is_sudo=row["is_sudo"],
            is_banned=row["is_banned"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    @staticmethod
    def _payment_from_row(row: Any) -> PaymentRecord:
        return PaymentRecord(
            utr=row["utr"],
            user_id=row["user_id"],
            amount=float(row["amount"]),
            method=row["method"],
            status=row["status"],
            screenshot_url=row["screenshot_url"],
            created_at=row["created_at"],
            reconciled_at=row["reconciled_at"],
            approved_by=row["approved_by"],
        )

    @staticmethod
    def _api_key_from_row(row: Any) -> ApiKeyRecord:
        return ApiKeyRecord(
            key=row["key"],
            user_id=row["user_id"],
            tier=row["tier"],
            rate_limit_per_minute=row["rate_limit_per_minute"],
            total_requests=row["total_requests"],
            is_active=row["is_active"],
            created_at=row["created_at"],
        )

    # User Management
    async def get_or_create_user(self, user_id: int, username: Optional[str] = None, first_name: str = "Aspirant") -> User:
        if self._persistent:
            async with self._pool.acquire() as conn:
                row = await conn.fetchrow(
                    """
                    INSERT INTO users (user_id, username, first_name)
                    VALUES ($1, $2, $3)
                    ON CONFLICT (user_id) DO UPDATE
                    SET username = COALESCE(EXCLUDED.username, users.username),
                        first_name = CASE WHEN $3 = 'Aspirant' THEN users.first_name ELSE EXCLUDED.first_name END,
                        updated_at = CURRENT_TIMESTAMP
                    RETURNING user_id, username, first_name, tier, is_sudo, is_banned,
                              created_at, updated_at
                    """,
                    user_id,
                    username,
                    first_name,
                )
            return self._user_from_row(row)
        if user_id not in self._users:
            self._users[user_id] = User(user_id=user_id, username=username, first_name=first_name)
        else:
            if username:
                self._users[user_id].username = username
        return self._users[user_id]

    async def get_user(self, user_id: int) -> Optional[User]:
        if self._persistent:
            async with self._pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT user_id, username, first_name, tier, is_sudo, is_banned, created_at, updated_at FROM users WHERE user_id = $1",
                    user_id,
                )
            return self._user_from_row(row) if row else None
        return self._users.get(user_id)

    async def update_user_tier(self, user_id: int, tier: str) -> User:
        if self._persistent:
            await self.get_or_create_user(user_id)
            async with self._pool.acquire() as conn:
                row = await conn.fetchrow(
                    "UPDATE users SET tier = $2, updated_at = CURRENT_TIMESTAMP WHERE user_id = $1 RETURNING user_id, username, first_name, tier, is_sudo, is_banned, created_at, updated_at",
                    user_id,
                    tier.upper(),
                )
            return self._user_from_row(row)
        user = await self.get_or_create_user(user_id)
        user.tier = tier
        user.updated_at = datetime.utcnow()
        return user

    # Payment Management & UTR Submission
    async def submit_payment(self, utr: str, user_id: int, amount: float, method: str, screenshot_url: Optional[str] = None) -> PaymentRecord:
        utr_clean = utr.strip().upper()
        if self._persistent:
            await self.get_or_create_user(user_id)
            async with self._pool.acquire() as conn:
                existing = await conn.fetchrow("SELECT utr FROM payments WHERE utr = $1", utr_clean)
                if existing:
                    raise PaymentReconciliationError(f"Duplicate payment submission! UTR {utr_clean} already registered.")
                row = await conn.fetchrow(
                    """
                    INSERT INTO payments (utr, user_id, amount, method, status, screenshot_url)
                    VALUES ($1, $2, $3, $4, 'PENDING', $5)
                    RETURNING utr, user_id, amount, method, status, screenshot_url,
                              created_at, reconciled_at, approved_by
                    """,
                    utr_clean,
                    user_id,
                    amount,
                    method.upper(),
                    screenshot_url,
                )
            return self._payment_from_row(row)
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
        if self._persistent:
            async with self._pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT utr, user_id, amount, method, status, screenshot_url, created_at, reconciled_at, approved_by FROM payments WHERE utr = $1",
                    utr.strip().upper(),
                )
            return self._payment_from_row(row) if row else None
        return self._payments.get(utr.strip().upper())

    async def approve_payment(self, utr: str, approved_by: int) -> PaymentRecord:
        if self._persistent:
            async with self._pool.acquire() as conn:
                async with conn.transaction():
                    row = await conn.fetchrow(
                        "SELECT utr, user_id, amount, method, status, screenshot_url, created_at, reconciled_at, approved_by FROM payments WHERE utr = $1 FOR UPDATE",
                        utr.strip().upper(),
                    )
                    if not row:
                        raise PaymentReconciliationError(f"Payment with UTR {utr} not found.")
                    if row["status"] == "APPROVED":
                        return self._payment_from_row(row)
                    tier = "PRO" if float(row["amount"]) >= 499 else "PREMIUM"
                    await conn.execute(
                        "INSERT INTO users (user_id) VALUES ($1) ON CONFLICT (user_id) DO UPDATE SET tier = $2, updated_at = CURRENT_TIMESTAMP",
                        row["user_id"],
                        tier,
                    )
                    await conn.execute(
                        "UPDATE users SET tier = $2, updated_at = CURRENT_TIMESTAMP WHERE user_id = $1",
                        row["user_id"],
                        tier,
                    )
                    await conn.execute(
                        "UPDATE payments SET status = 'APPROVED', reconciled_at = CURRENT_TIMESTAMP, approved_by = $2 WHERE utr = $1",
                        row["utr"],
                        approved_by,
                    )
                    await conn.execute(
                        "INSERT INTO subscriptions (id, user_id, tier, starts_at, expires_at, payment_utr) VALUES ($1, $2, $3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '30 days', $4)",
                        secrets.token_hex(8),
                        row["user_id"],
                        tier,
                        row["utr"],
                    )
                    row = await conn.fetchrow(
                        "SELECT utr, user_id, amount, method, status, screenshot_url, created_at, reconciled_at, approved_by FROM payments WHERE utr = $1",
                        row["utr"],
                    )
            return self._payment_from_row(row)
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

    async def reject_payment(self, utr: str, rejected_by: int) -> bool:
        if self._persistent:
            async with self._pool.acquire() as conn:
                result = await conn.execute(
                    "UPDATE payments SET status = 'REJECTED', reconciled_at = CURRENT_TIMESTAMP, approved_by = $2 WHERE utr = $1 AND status = 'PENDING'",
                    utr.strip().upper(),
                    rejected_by,
                )
            if int(result.split()[-1]) == 0:
                existing = await self.get_payment(utr)
                if not existing:
                    raise PaymentReconciliationError(f"Payment with UTR {utr} not found.")
                if existing.status == "APPROVED":
                    raise PaymentReconciliationError("An approved payment cannot be rejected.")
                return False
            return True
        record = await self.get_payment(utr)
        if not record:
            raise PaymentReconciliationError(f"Payment with UTR {utr} not found.")
        if record.status == "APPROVED":
            raise PaymentReconciliationError("An approved payment cannot be rejected.")
        record.status = "REJECTED"
        record.reconciled_at = datetime.utcnow()
        record.approved_by = rejected_by
        return True

    # API Key Management
    async def generate_api_key(self, user_id: int, tier: str = "FREE") -> ApiKeyRecord:
        key = f"csea_{tier.lower()}_{secrets.token_urlsafe(24)}"
        rate_limits = {"FREE": 10, "PREMIUM": 100, "PRO": 1000}
        if self._persistent:
            await self.get_or_create_user(user_id)
            async with self._pool.acquire() as conn:
                row = await conn.fetchrow(
                    "INSERT INTO api_keys (key, user_id, tier, rate_limit_per_minute) VALUES ($1, $2, $3, $4) RETURNING key, user_id, tier, rate_limit_per_minute, total_requests, is_active, created_at",
                    key,
                    user_id,
                    tier.upper(),
                    rate_limits.get(tier.upper(), 10),
                )
            return self._api_key_from_row(row)
        record = ApiKeyRecord(
            key=key,
            user_id=user_id,
            tier=tier,
            rate_limit_per_minute=rate_limits.get(tier, 10)
        )
        self._api_keys[key] = record
        return record

    async def get_api_key(self, key: str) -> Optional[ApiKeyRecord]:
        if self._persistent:
            async with self._pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT key, user_id, tier, rate_limit_per_minute, total_requests, is_active, created_at FROM api_keys WHERE key = $1",
                    key,
                )
            return self._api_key_from_row(row) if row else None
        return self._api_keys.get(key)

    async def revoke_api_key(self, key: str) -> bool:
        if self._persistent:
            async with self._pool.acquire() as conn:
                result = await conn.execute("UPDATE api_keys SET is_active = FALSE WHERE key = $1 AND is_active", key)
            return int(result.split()[-1]) > 0
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
