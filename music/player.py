"""
CSE Aspirant - Guild Audio Player
"""
import asyncio
from typing import Optional, Dict, Any
from core.constants import STATE_IDLE, STATE_PLAYING, STATE_PAUSED, STATE_STOPPED
from music.backend import AudioBackend, UnconfiguredAudioBackend
from music.queue import MusicQueue
from music.track import Track
from music.recovery import recovery_engine
from core.logger import logger

class GuildPlayer:
    def __init__(self, chat_id: int, backend: Optional[AudioBackend] = None):
        self.chat_id = chat_id
        self.backend = backend or UnconfiguredAudioBackend()
        self.queue = MusicQueue()
        self.state: str = STATE_IDLE
        self.volume: int = 100
        self.current_position: int = 0
        self._playback_task: Optional[asyncio.Task] = None
        self._lock = asyncio.Lock()

    async def play(self, track: Track) -> Track:
        async with self._lock:
            self.queue.add(track)
            if self.state in (STATE_PLAYING, STATE_PAUSED):
                return track
            return await self._play_next()

    async def _play_next(self) -> Optional[Track]:
        track = self.queue.next()
        if not track:
            self.state = STATE_IDLE
            self.current_position = 0
            logger.info(f"Queue finished for chat {self.chat_id}. Player is IDLE.")
            return None

        try:
            await self.backend.start(self.chat_id, track, self.volume, self.current_position)
        except Exception:
            self.state = STATE_IDLE
            raise

        self.state = STATE_PLAYING
        self.current_position = 0
        logger.info(f"Now playing in chat {self.chat_id}: {track.title}")
        return track

    async def pause(self) -> bool:
        async with self._lock:
            if self.state != STATE_PLAYING:
                return False
            await self.backend.pause(self.chat_id)
            self.state = STATE_PAUSED
            logger.info(f"Playback paused in chat {self.chat_id}")
            return True

    async def resume(self) -> bool:
        async with self._lock:
            if self.state != STATE_PAUSED:
                return False
            await self.backend.resume(self.chat_id)
            self.state = STATE_PLAYING
            logger.info(f"Playback resumed in chat {self.chat_id}")
            return True

    async def skip(self) -> Optional[Track]:
        async with self._lock:
            logger.info(f"Skipping track in chat {self.chat_id}")
            await self.backend.stop(self.chat_id)
            track = self.queue.next(force=True)
            if not track:
                self.state = STATE_IDLE
                self.current_position = 0
                return None
            await self.backend.start(self.chat_id, track, self.volume)
            self.state = STATE_PLAYING
            self.current_position = 0
            return track

    async def previous(self) -> Optional[Track]:
        async with self._lock:
            prev = self.queue.previous()
            if not prev:
                return None
            await self.backend.start(self.chat_id, prev, self.volume)
            self.state = STATE_PLAYING
            self.current_position = 0
            logger.info(f"Playing previous track in chat {self.chat_id}: {prev.title}")
            return prev

    async def stop(self):
        async with self._lock:
            await self.backend.leave(self.chat_id)
            if self._playback_task and not self._playback_task.done():
                self._playback_task.cancel()
            self.state = STATE_STOPPED
            self.queue.clear()
            self.current_position = 0
            logger.info(f"Player stopped in chat {self.chat_id}")

    def set_volume(self, vol: int) -> int:
        self.volume = max(0, min(200, vol))
        logger.info(f"Volume in chat {self.chat_id} set to {self.volume}%")
        return self.volume

    async def set_volume_live(self, vol: int) -> int:
        async with self._lock:
            new_volume = self.set_volume(vol)
            await self.backend.set_volume(self.chat_id, new_volume)
            return new_volume

    async def seek(self, position: int) -> int:
        async with self._lock:
            if not self.queue.current:
                raise ValueError("No track is currently playing")
            if position < 0 or (self.queue.current.duration and position >= self.queue.current.duration):
                raise ValueError("Seek position is outside the track duration")
            await self.backend.seek(
                self.chat_id,
                self.queue.current,
                self.volume,
                position,
            )
            self.current_position = position
            self.state = STATE_PLAYING
            return position

    def set_repeat(self, mode: str):
        self.queue.set_repeat(mode)

    def shuffle(self):
        self.queue.shuffle()

    async def recover(self) -> bool:
        if self.queue.current:
            async with self._lock:
                recovered = await recovery_engine.recover_stream(
                    self.chat_id,
                    self.queue.current.uri,
                    self.current_position
                )
                if recovered:
                    await self.backend.start(
                        self.chat_id,
                        self.queue.current,
                        self.volume,
                        self.current_position,
                    )
                    self.state = STATE_PLAYING
                return recovered
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
