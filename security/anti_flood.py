"""
CSE Aspirant - Anti-Flood Sliding Window Rate Limiter
"""
import time
from typing import Dict, List
from collections import defaultdict

class AntiFloodFilter:
    def __init__(self, limit: int = 5, window_seconds: float = 4.0):
        self.limit = limit
        self.window = window_seconds
        self._user_timestamps: Dict[int, List[float]] = defaultdict(list)

    def is_flooding(self, user_id: int) -> bool:
        now = time.time()
        timestamps = self._user_timestamps[user_id]
        
        # Prune old timestamps
        while timestamps and timestamps[0] <= now - self.window:
            timestamps.pop(0)

        timestamps.append(now)
        return len(timestamps) > self.limit

    def reset(self, user_id: int):
        if user_id in self._user_timestamps:
            del self._user_timestamps[user_id]

anti_flood = AntiFloodFilter()

