"""
CSE Aspirant - Bridge to High-Performance Go Music Engine
"""
from typing import Dict, Any, Optional
from urllib.parse import quote
from core.config import config
from core.logger import logger
from error_handling.retry import async_retry

class GoEngineError(RuntimeError):
    """Raised when the Go audio engine cannot create a stream."""


class GoEngineBridge:
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or config.services.go_engine_url

    @async_retry(max_retries=2, initial_delay=0.3)
    async def transcode_or_stream(self, stream_url: str, output_format: str = "pcm") -> Dict[str, Any]:
        """Create a real stream session in the Go engine."""
        return await self.open_stream(stream_url, output_format=output_format)

    @async_retry(max_retries=2, initial_delay=0.3)
    async def open_stream(
        self,
        stream_url: str,
        output_format: str = "opus",
        position: int = 0,
    ) -> Dict[str, Any]:
        import aiohttp

        if not stream_url.startswith(("http://", "https://")):
            raise GoEngineError("Only HTTP(S) audio URLs are supported")
        if position < 0:
            raise GoEngineError("Stream position cannot be negative")

        url = f"{self.base_url.rstrip('/')}/api/v1/stream"
        payload = {"url": stream_url, "format": output_format, "position": position}
        headers = {"Authorization": f"Bearer {config.services.go_engine_token}"}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=4.0),
                ) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        if (
                            result.get("status") != "READY"
                            or not result.get("stream_url")
                            or not result.get("stream_id")
                        ):
                            raise GoEngineError("Go engine returned an invalid stream session")
                        return result
                    body = await resp.text()
                    raise GoEngineError(f"Go engine returned HTTP {resp.status}: {body[:200]}")
        except Exception as e:
            logger.warning(f"Go engine stream creation failed: {e}")
            if isinstance(e, GoEngineError):
                raise
            raise GoEngineError("Unable to connect to the Go audio engine") from e

    async def close_stream(self, stream_id: str) -> None:
        import aiohttp

        if not stream_id:
            return
        url = f"{self.base_url.rstrip('/')}/api/v1/stream/{quote(stream_id, safe='')}"
        headers = {"Authorization": f"Bearer {config.services.go_engine_token}"}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.delete(
                    url,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=2.0),
                ) as resp:
                    if resp.status not in (204, 404):
                        raise GoEngineError(f"Go engine returned HTTP {resp.status} while closing stream")
        except GoEngineError:
            raise
        except Exception as exc:
            raise GoEngineError("Unable to close the Go audio stream") from exc

    async def get_engine_health(self) -> Dict[str, Any]:
        import aiohttp

        url = f"{self.base_url.rstrip('/')}/health"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=2.0)) as resp:
                    if resp.status == 200:
                        return await resp.json()
        except Exception:
            return {"status": "degraded", "active_workers": 0, "engine": "go_offline"}

go_bridge = GoEngineBridge()
