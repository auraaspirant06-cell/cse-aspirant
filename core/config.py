"""
CSE Aspirant - Core Configuration Module
"""
import os
from dataclasses import dataclass, field
from typing import List

@dataclass
class BotConfig:
    bot_token: str = os.getenv("BOT_TOKEN", "MOCK_BOT_TOKEN_CSE_ASPIRANT")
    api_id: int = int(os.getenv("TELEGRAM_API_ID", "1234567"))
    api_hash: str = os.getenv("TELEGRAM_API_HASH", "mock_telegram_api_hash_cse")
    owner_id: int = int(os.getenv("OWNER_ID", "987654321"))
    sudo_users: List[int] = field(default_factory=lambda: [
        int(x.strip()) for x in os.getenv("SUDO_USERS", "987654321").split(",") if x.strip()
    ])
    prefixes: List[str] = field(default_factory=lambda: ["/", "!", "."])
    start_img_url: str = os.getenv("START_IMG_URL", "https://i.ytimg.com/vi/9Bk5WgGfkwM/maxresdefault.jpg")

@dataclass
class DatabaseConfig:
    postgres_url: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:postgres@localhost:5432/cse_aspirant"
    )
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

@dataclass
class ServiceConfig:
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    go_engine_url: str = os.getenv("GO_ENGINE_URL", "http://localhost:8080")
    jwt_secret: str = os.getenv("JWT_SECRET", "super-secret-cse-aspirant-key-2026")
    ai_provider: str = os.getenv("AI_PROVIDER", "hybrid")

@dataclass
class AppConfig:
    bot: BotConfig = field(default_factory=BotConfig)
    db: DatabaseConfig = field(default_factory=DatabaseConfig)
    services: ServiceConfig = field(default_factory=ServiceConfig)

config = AppConfig()
