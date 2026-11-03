"""CSE Aspirant environment-backed configuration."""
import os
from dataclasses import dataclass, field
from typing import List
from urllib.parse import urlparse


class ConfigurationError(RuntimeError):
    """Raised when required application configuration is missing or invalid."""


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def _int_env(name: str, default: int = 0) -> int:
    value = _env(name, str(default))
    try:
        return int(value)
    except ValueError as exc:
        raise ConfigurationError(f"{name} must be an integer") from exc


def _csv_env(name: str) -> List[str]:
    return [item.strip() for item in _env(name).split(",") if item.strip()]


def _int_list_env(name: str) -> List[int]:
    try:
        return [int(item) for item in _csv_env(name)]
    except ValueError as exc:
        raise ConfigurationError(f"{name} must contain comma-separated integers") from exc

@dataclass
class BotConfig:
    bot_token: str = field(default_factory=lambda: _env("BOT_TOKEN"))
    api_id: int = field(default_factory=lambda: _int_env("TELEGRAM_API_ID"))
    api_hash: str = field(default_factory=lambda: _env("TELEGRAM_API_HASH"))
    session_string: str = field(default_factory=lambda: _env("TELEGRAM_SESSION_STRING"))
    owner_id: int = field(default_factory=lambda: _int_env("OWNER_ID"))
    sudo_users: List[int] = field(default_factory=lambda: _int_list_env("SUDO_USERS"))
    prefixes: List[str] = field(default_factory=lambda: ["/", "!", "."])
    start_img_url: str = field(default_factory=lambda: _env(
        "START_IMG_URL",
        "https://i.ytimg.com/vi/9Bk5WgGfkwM/maxresdefault.jpg",
    ))

@dataclass
class DatabaseConfig:
    postgres_url: str = field(default_factory=lambda: _env("DATABASE_URL"))
    redis_url: str = field(default_factory=lambda: _env("REDIS_URL"))

@dataclass
class ServiceConfig:
    api_host: str = field(default_factory=lambda: _env("API_HOST", "0.0.0.0"))
    api_port: int = field(default_factory=lambda: _int_env("API_PORT", 8000))
    go_engine_url: str = field(default_factory=lambda: _env("GO_ENGINE_URL"))
    go_engine_token: str = field(default_factory=lambda: _env("GO_ENGINE_TOKEN"))
    jwt_secret: str = field(default_factory=lambda: _env("JWT_SECRET"))
    master_api_key: str = field(default_factory=lambda: _env("MASTER_API_KEY"))
    ai_provider: str = field(default_factory=lambda: _env("AI_PROVIDER", "local"))
    ai_api_key: str = field(default_factory=lambda: _env("AI_API_KEY"))
    cors_origins: List[str] = field(default_factory=lambda: _csv_env("CORS_ORIGINS"))


@dataclass
class PaymentConfig:
    upi_id: str = field(default_factory=lambda: _env("PAYMENT_UPI_ID"))
    merchant_name: str = field(default_factory=lambda: _env("PAYMENT_MERCHANT_NAME"))
    bank_name: str = field(default_factory=lambda: _env("PAYMENT_BANK_NAME"))
    account_name: str = field(default_factory=lambda: _env("PAYMENT_ACCOUNT_NAME"))
    account_number: str = field(default_factory=lambda: _env("PAYMENT_ACCOUNT_NUMBER"))
    ifsc_code: str = field(default_factory=lambda: _env("PAYMENT_IFSC_CODE"))
    bank_branch: str = field(default_factory=lambda: _env("PAYMENT_BANK_BRANCH"))
    checkout_url: str = field(default_factory=lambda: _env("PAYMENT_CHECKOUT_URL"))

@dataclass
class AppConfig:
    bot: BotConfig = field(default_factory=BotConfig)
    db: DatabaseConfig = field(default_factory=DatabaseConfig)
    services: ServiceConfig = field(default_factory=ServiceConfig)
    payment: PaymentConfig = field(default_factory=PaymentConfig)


def _valid_url(value: str, schemes: tuple[str, ...]) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in schemes and bool(parsed.netloc)


def validate_config(app_config: AppConfig = None) -> None:
    """Validate production startup configuration without exposing secret values."""
    app_config = app_config or config
    missing = []
    invalid = []

    required_values = {
        "BOT_TOKEN": app_config.bot.bot_token,
        "TELEGRAM_API_HASH": app_config.bot.api_hash,
        "TELEGRAM_SESSION_STRING": app_config.bot.session_string,
        "DATABASE_URL": app_config.db.postgres_url,
        "REDIS_URL": app_config.db.redis_url,
        "GO_ENGINE_URL": app_config.services.go_engine_url,
        "GO_ENGINE_TOKEN": app_config.services.go_engine_token,
        "MASTER_API_KEY": app_config.services.master_api_key,
        "PAYMENT_UPI_ID": app_config.payment.upi_id,
        "PAYMENT_MERCHANT_NAME": app_config.payment.merchant_name,
        "PAYMENT_BANK_NAME": app_config.payment.bank_name,
        "PAYMENT_ACCOUNT_NAME": app_config.payment.account_name,
        "PAYMENT_ACCOUNT_NUMBER": app_config.payment.account_number,
        "PAYMENT_IFSC_CODE": app_config.payment.ifsc_code,
        "PAYMENT_BANK_BRANCH": app_config.payment.bank_branch,
        "PAYMENT_CHECKOUT_URL": app_config.payment.checkout_url,
    }
    missing.extend(name for name, value in required_values.items() if not value)

    if app_config.bot.api_id <= 0:
        invalid.append("TELEGRAM_API_ID")
    if app_config.bot.owner_id <= 0:
        invalid.append("OWNER_ID")
    if not (1 <= app_config.services.api_port <= 65535):
        invalid.append("API_PORT")
    if not _valid_url(app_config.db.postgres_url, ("postgresql", "postgres")):
        invalid.append("DATABASE_URL")
    if not _valid_url(app_config.db.redis_url, ("redis", "rediss")):
        invalid.append("REDIS_URL")
    if not _valid_url(app_config.services.go_engine_url, ("http", "https")):
        invalid.append("GO_ENGINE_URL")
    if not _valid_url(app_config.payment.checkout_url, ("http", "https")):
        invalid.append("PAYMENT_CHECKOUT_URL")
    if len(app_config.services.master_api_key) < 32:
        invalid.append("MASTER_API_KEY")

    if missing or invalid:
        problems = []
        if missing:
            problems.append("missing: " + ", ".join(sorted(set(missing))))
        if invalid:
            problems.append("invalid: " + ", ".join(sorted(set(invalid))))
        raise ConfigurationError("Invalid application configuration (" + "; ".join(problems) + ")")

config = AppConfig()
