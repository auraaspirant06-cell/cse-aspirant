"""
CSE Aspirant - Audio Stream Recovery & Auto-Reconnect Engine
"""
import asyncio
from core.logger import logger
from error_handling.exceptions import StreamRecoveryError

class StreamRecoveryEngine:
    def __init__(self, max_reconnect_attempts: int = 5, retry_delay: float = 1.5):
        self.max_attempts = max_reconnect_attempts
        self.retry_delay = retry_delay

    async def recover_stream(self, chat_id: int, stream_url: str, resume_position: int = 0) -> bool:
        logger.warning(f"Audio stream interrupted for chat {chat_id}. Attempting auto-recovery...")
        for attempt in range(1, self.max_attempts + 1):
            try:
                import aiohttp

                await asyncio.sleep(self.retry_delay * attempt)
                timeout = aiohttp.ClientTimeout(total=5.0)
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    async with session.get(
                        stream_url,
                        headers={"Range": "bytes=0-1"},
                    ) as response:
                        if response.status not in (200, 206):
                            raise RuntimeError(f"stream returned HTTP {response.status}")
                logger.info(f"Recovery attempt {attempt}/{self.max_attempts} for chat {chat_id} at pos {resume_position}s")
                return True
            except Exception as e:
                logger.error(f"Stream recovery attempt {attempt} failed: {e}")
        
        raise StreamRecoveryError(f"Failed to recover audio stream after {self.max_attempts} attempts.")

recovery_engine = StreamRecoveryEngine()
