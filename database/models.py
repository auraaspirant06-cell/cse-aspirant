"""
CSE Aspirant - Database Data Models
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any

@dataclass
class User:
    user_id: int
    username: Optional[str] = None
    first_name: str = "Aspirant"
    tier: str = "FREE"  # FREE, PREMIUM, PRO
    is_sudo: bool = False
    is_banned: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class Subscription:
    id: str
    user_id: int
    tier: str
    starts_at: datetime
    expires_at: datetime
    is_active: bool = True
    payment_utr: Optional[str] = None

@dataclass
class PaymentRecord:
    utr: str
    user_id: int
    amount: float
    method: str  # UPI, NEFT, CARD
    status: str  # PENDING, APPROVED, REJECTED
    screenshot_url: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    reconciled_at: Optional[datetime] = None
    approved_by: Optional[int] = None

@dataclass
class ApiKeyRecord:
    key: str
    user_id: int
    tier: str
    rate_limit_per_minute: int
    total_requests: int = 0
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class GroupSetting:
    chat_id: int
    title: str = ""
    welcome_enabled: bool = True
    anti_spam: bool = True
    anti_flood: bool = True
    volume: int = 100
    repeat_mode: str = "OFF"  # OFF, ONE, ALL

@dataclass
class PromotionRecord:
    promo_id: str
    user_id: int
    channel_link: str
    status: str = "PENDING"  # PENDING, APPROVED, REJECTED, PUBLISHED
    created_at: datetime = field(default_factory=datetime.utcnow)
    reviewed_by: Optional[int] = None
