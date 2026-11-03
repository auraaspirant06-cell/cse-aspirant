"""Audio backend contracts used by the per-chat music player."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from music.track import Track


class AudioBackendError(RuntimeError):
    """Raised when an audio backend cannot start or control playback."""


class AudioBackend(Protocol):
    async def start(self, chat_id: int, track: Track, volume: int, position: int = 0) -> None:
        """Start or replace playback for a Telegram chat."""

    async def pause(self, chat_id: int) -> None:
        """Pause playback for a Telegram chat."""

    async def resume(self, chat_id: int) -> None:
        """Resume playback for a Telegram chat."""

    async def stop(self, chat_id: int) -> None:
        """Stop the current media without leaving the voice chat."""

    async def leave(self, chat_id: int) -> None:
        """Stop playback and leave the Telegram voice chat."""

    async def set_volume(self, chat_id: int, volume: int) -> None:
        """Apply a volume percentage to the active stream."""

    async def seek(self, chat_id: int, track: Track, volume: int, position: int) -> None:
        """Restart the active stream from a position in seconds."""


@dataclass
class UnconfiguredAudioBackend:
    """Explicit failure backend; prevents false successful playback responses."""

    reason: str = "Telegram voice-chat audio backend is not configured"

    async def start(self, chat_id: int, track: Track, volume: int, position: int = 0) -> None:
        raise AudioBackendError(self.reason)

    async def pause(self, chat_id: int) -> None:
        raise AudioBackendError(self.reason)

    async def resume(self, chat_id: int) -> None:
        raise AudioBackendError(self.reason)

    async def stop(self, chat_id: int) -> None:
        return None

    async def leave(self, chat_id: int) -> None:
        return None

    async def set_volume(self, chat_id: int, volume: int) -> None:
        raise AudioBackendError(self.reason)

    async def seek(self, chat_id: int, track: Track, volume: int, position: int) -> None:
        raise AudioBackendError(self.reason)
