"""
CSE Aspirant - Protected Mass Broadcaster
"""
import asyncio
from typing import List, Dict, Any, Callable
from core.logger import logger

class SafeBroadcaster:
    def __init__(self, rate_delay: float = 0.05):
        self.rate_delay = rate_delay

    async def broadcast_message(
        self,
        targets: List[int],
        message: str,
        send_fn: Callable[[int, str], Any],
        pin: bool = False
    ) -> Dict[str, int]:
        success_count = 0
        failure_count = 0
        
        for target in targets:
            try:
                await send_fn(target, message)
                success_count += 1
                await asyncio.sleep(self.rate_delay)
            except Exception as e:
                logger.warning(f"Broadcast failed for {target}: {e}")
                failure_count += 1

        logger.info(f"Broadcast complete. Success: {success_count}, Failed: {failure_count}")
        return {
            "total": len(targets),
            "successful": success_count,
            "failed": failure_count
        }

broadcaster = SafeBroadcaster()

