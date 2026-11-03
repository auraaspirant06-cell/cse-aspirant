"""
CSE Aspirant - Guild Audio Player
"""
import asyncio
from typing import Optional, Dict, Any
from core.constants import STATE_IDLE, STATE_PLAYING, STATE_PAUSED, STATE_STOPPED
from music.queue import MusicQueue
from music.track import Track
from music.recovery import recovery_engine
from core.logger import logger

class GuildPlayer:
    def __init__(self, chat_id: int):
        self.chat_id = chat_id
        self.queue = MusicQueue()
        self.state: str = STATE_IDLE
        self.volume: int = 100
        self.current_position: int = 0
        self._playback_task: Optional[asyncio.Task] = None

    async def play(self, track: Track) -> Track:
        self.queue.add(track)
        if self.state != STATE_PLAYING:
            return await self._play_next()
        return track

    async def _play_next(self) -> Optional[Track]:
        track = self.queue.next()
        if not track:
            self.state = STATE_IDLE
            self.current_position = 0
            logger.info(f"Queue finished for chat {self.chat_id}. Player is IDLE.")
            return None

        self.state = STATE_PLAYING
        self.current_position = 0
        logger.info(f"Now playing in chat {self.chat_id}: {track.title}")
        return track

    async def pause(self) -> bool:
        if self.state == STATE_PLAYING:
            self.state = STATE_PAUSED
            logger.info(f"Playback paused in chat {self.chat_id}")
            return True
        return False

    async def resume(self) -> bool:
        if self.state == STATE_PAUSED:
            self.state = STATE_PLAYING
            logger.info(f"Playback resumed in chat {self.chat_id}")
            return True
        return False

    async def skip(self) -> Optional[Track]:
        logger.info(f"Skipping track in chat {self.chat_id}")
        return await self._play_next()

    async def previous(self) -> Optional[Track]:
        prev = self.queue.previous()
        if prev:
            self.state = STATE_PLAYING
            self.current_position = 0
            logger.info(f"Playing previous track in chat {self.chat_id}: {prev.title}")
            return prev
        return None

    async def stop(self):
        self.state = STATE_STOPPED
        self.queue.clear()
        self.current_position = 0
        logger.info(f"Player stopped in chat {self.chat_id}")

    def set_volume(self, vol: int) -> int:
        self.volume = max(0, min(200, vol))
        logger.info(f"Volume in chat {self.chat_id} set to {self.volume}%")
        return self.volume

    def set_repeat(self, mode: str):
        self.queue.set_repeat(mode)

    def shuffle(self):
        self.queue.shuffle()

    async def recover(self) -> bool:
        if self.queue.current:
            return await recovery_engine.recover_stream(
                self.chat_id, 
                self.queue.current.uri, 
                self.current_position
            )
        return False

    def get_status(self) -> Dict[str, Any]:
        return {
            "chat_id": self.chat_id,
            "state": self.state,
            "volume": self.volume,
            "repeat_mode": self.queue.repeat_mode,
            "current_track": self.queue.current.to_dict() if self.queue.current else None,
            "queue_length": len(self.queue.tracks)
        }
