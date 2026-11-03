"""
CSE Aspirant - Database & Cache Connection Manager
"""
from typing import Optional, Any
from core.config import config
from core.logger import logger

class DatabaseManager:
    def __init__(self):
        self.pg_pool: Optional[Any] = None
        self.redis_client: Optional[Any] = None
        self.is_connected: bool = False

    async def connect(self):
        # AsyncPG connect attempt
        try:
            import asyncpg
            self.pg_pool = await asyncpg.create_pool(
                config.db.postgres_url,
                min_size=1,
                max_size=10,
                timeout=5.0
            )
            logger.info("Connected to PostgreSQL successfully.")
        except Exception as e:
            logger.warning(f"PostgreSQL unavailable ({e}). Falling back to in-memory repository.")
            self.pg_pool = None

        # Redis connect attempt
        try:
            import redis.asyncio as aioredis
            self.redis_client = aioredis.from_url(
                config.db.redis_url,
                encoding="utf-8",
                decode_responses=True,
                socket_connect_timeout=2.0
            )
            await self.redis_client.ping()
            logger.info("Connected to Redis successfully.")
        except Exception as e:
            logger.warning(f"Redis unavailable ({e}). Falling back to in-memory cache.")
            self.redis_client = None

        self.is_connected = True

    async def disconnect(self):
        if self.pg_pool:
            await self.pg_pool.close()
        if self.redis_client:
            await self.redis_client.close()
        self.is_connected = False
        logger.info("Database connections closed.")

db_manager = DatabaseManager()
