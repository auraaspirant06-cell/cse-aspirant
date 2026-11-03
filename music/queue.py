"""
CSE Aspirant - Music Queue with History, Shuffle, and Repeat
"""
import random
from typing import List, Optional
from music.track import Track
from core.logger import logger

class MusicQueue:
    def __init__(self):
        self._queue: List[Track] = []
        self._history: List[Track] = []
        self._current: Optional[Track] = None
        self.repeat_mode: str = "OFF"  # OFF, ONE, ALL

    @property
    def current(self) -> Optional[Track]:
        return self._current

    @property
    def tracks(self) -> List[Track]:
        return list(self._queue)

    @property
    def history(self) -> List[Track]:
        return list(self._history)

    def add(self, track: Track):
        self._queue.append(track)
        logger.info(f"Added to queue: {track.title} (Duration: {track.duration}s)")

    def next(self) -> Optional[Track]:
        if self.repeat_mode == "ONE" and self._current:
            return self._current
        
        if self._current:
            self._history.append(self._current)
            if self.repeat_mode == "ALL":
                self._queue.append(self._current)

        if not self._queue:
            self._current = None
            return None

        self._current = self._queue.pop(0)
        return self._current

    def previous(self) -> Optional[Track]:
        if not self._history:
            return None
        
        prev_track = self._history.pop()
        if self._current:
            self._queue.insert(0, self._current)
        self._current = prev_track
        return self._current

    def shuffle(self):
        random.shuffle(self._queue)

    def clear(self):
        self._queue.clear()
        self._history.clear()
        self._current = None

    def set_repeat(self, mode: str):
        mode = mode.upper()
        if mode in ("OFF", "ONE", "ALL"):
            self.repeat_mode = mode
