"""
CSE Aspirant - Bridge to High-Performance Go Music Engine
"""
from typing import Dict, Any, Optional
import aiohttp
from core.config import config
from core.logger import logger
from error_handling.retry import async_retry

class GoEngineBridge:
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or config.services.go_engine_url

    @async_retry(max_retries=2, initial_delay=0.3)
    async def transcode_or_stream(self, stream_url: str, output_format: str = "pcm") -> Dict[str, Any]:
        """Calls Go engine to transcode or buffer high-bitrate audio."""
        url = f"{self.base_url}/api/v1/stream"
        payload = {"url": stream_url, "format": output_format}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=4.0)) as resp:
                    if resp.status == 200:
                        return await resp.json()
        except Exception as e:
            logger.warning(f"Go engine connection skipped ({e}). Falling back to native async stream.")
        
        return {
            "status": "fallback",
            "stream_url": stream_url,
            "engine": "internal_async"
        }

    async def get_engine_health(self) -> Dict[str, Any]:
        url = f"{self.base_url}/health"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=2.0)) as resp:
                    if resp.status == 200:
                        return await resp.json()
        except Exception:
            pass
        return {"status": "degraded", "active_workers": 0, "engine": "go_offline"}

go_bridge = GoEngineBridge()
