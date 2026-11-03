"""PyTgCalls audio backend for real Telegram group voice chats."""
from __future__ import annotations

import inspect
from typing import Any

from core.logger import logger
from music.audio_bridge import GoEngineError, go_bridge
from music.backend import AudioBackendError
from music.track import Track


async def _maybe_await(value: Any) -> Any:
    if inspect.isawaitable(value):
        return await value
    return value


class TelegramVoiceChatBackend:
    """Adapt a running PyTgCalls client to the music player contract.

    PyTgCalls must be created with a user session that can join group calls.
    A bot token alone is not sufficient for Telegram voice-chat playback.
    """

    def __init__(self, voice_client: Any):
        self.voice_client = voice_client
        self._active_streams: dict[int, str] = {}
        self._stream_sessions: dict[int, str] = {}
        self._stream_tracks: dict[int, int] = {}

    async def _media_stream(self, chat_id: int, track: Track, position: int = 0) -> Any:
        try:
            from pytgcalls.types import MediaStream
        except ImportError as exc:
            raise AudioBackendError(
                "pytgcalls is required for Telegram voice-chat playback"
            ) from exc

        try:
            stream = await go_bridge.open_stream(track.uri, output_format="opus", position=position)
        except GoEngineError as exc:
            raise AudioBackendError(str(exc)) from exc
        self._active_streams[track.track_id] = stream["stream_url"]
        self._stream_sessions[chat_id] = stream["stream_id"]
        self._stream_tracks[chat_id] = track.track_id
        return MediaStream(stream["stream_url"])

    async def _close_stream(self, chat_id: int) -> None:
        stream_id = self._stream_sessions.pop(chat_id, None)
        track_id = self._stream_tracks.pop(chat_id, None)
        if track_id:
            self._active_streams.pop(track_id, None)
        if stream_id:
            try:
                await go_bridge.close_stream(stream_id)
            except GoEngineError as exc:
                logger.warning("Unable to close Go stream %s: %s", stream_id, exc)

    async def start(self, chat_id: int, track: Track, volume: int, position: int = 0) -> None:
        await self._close_stream(chat_id)
        media = await self._media_stream(chat_id, track, position)
        try:
            await _maybe_await(self.voice_client.play(chat_id, media))
            if volume != 100:
                await self.set_volume(chat_id, volume)
        except Exception as exc:
            await self._close_stream(chat_id)
            try:
                await _maybe_await(self.voice_client.leave_call(chat_id, close=False))
            except Exception:
                logger.warning("Unable to clean up failed voice playback in chat %s", chat_id)
            raise AudioBackendError(f"Unable to start Telegram voice chat: {exc}") from exc
        logger.info("Started Telegram voice playback in chat %s", chat_id)

    async def pause(self, chat_id: int) -> None:
        try:
            await _maybe_await(self.voice_client.pause(chat_id))
        except Exception as exc:
            raise AudioBackendError(f"Unable to pause Telegram voice chat: {exc}") from exc

    async def resume(self, chat_id: int) -> None:
        try:
            await _maybe_await(self.voice_client.resume(chat_id))
        except Exception as exc:
            raise AudioBackendError(f"Unable to resume Telegram voice chat: {exc}") from exc

    async def stop(self, chat_id: int) -> None:
        await self._close_stream(chat_id)

    async def leave(self, chat_id: int) -> None:
        await self._close_stream(chat_id)
        try:
            await _maybe_await(self.voice_client.leave_call(chat_id, close=False))
        except Exception as exc:
            raise AudioBackendError(f"Unable to leave Telegram voice chat: {exc}") from exc

    async def set_volume(self, chat_id: int, volume: int) -> None:
        change_volume = getattr(self.voice_client, "change_volume_call", None)
        if change_volume is None:
            raise AudioBackendError("Installed PyTgCalls version has no volume control")
        try:
            await _maybe_await(change_volume(chat_id, volume))
        except Exception as exc:
            raise AudioBackendError(f"Unable to set Telegram volume: {exc}") from exc

    async def seek(self, chat_id: int, track: Track, volume: int, position: int) -> None:
        await self.stop(chat_id)
        await self.start(chat_id, track, volume, position)
