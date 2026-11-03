import sys
import types

import pytest

from music.telegram_backend import TelegramVoiceChatBackend
from music.track import Track


class FakeMediaStream:
    def __init__(self, path):
        self.path = path


class FakeVoiceClient:
    def __init__(self):
        self.events = []

    def play(self, chat_id, media):
        self.events.append(("play", chat_id, media.path))

    def pause(self, chat_id):
        self.events.append(("pause", chat_id))

    def resume(self, chat_id):
        self.events.append(("resume", chat_id))

    def change_volume_call(self, chat_id, volume):
        self.events.append(("volume", chat_id, volume))

    def leave_call(self, chat_id, close=False):
        self.events.append(("leave", chat_id, close))


@pytest.mark.asyncio
async def test_backend_replaces_stream_without_leaving_voice_chat(monkeypatch):
    fake_types = types.ModuleType("pytgcalls.types")
    fake_types.MediaStream = FakeMediaStream
    fake_package = types.ModuleType("pytgcalls")
    fake_package.types = fake_types
    monkeypatch.setitem(sys.modules, "pytgcalls", fake_package)
    monkeypatch.setitem(sys.modules, "pytgcalls.types", fake_types)

    opened = []
    closed = []

    async def open_stream(url, output_format="opus", position=0):
        stream_id = f"stream-{len(opened) + 1}"
        opened.append((url, output_format, position, stream_id))
        return {"stream_id": stream_id, "stream_url": f"http://engine/{stream_id}.ogg"}

    async def close_stream(stream_id):
        closed.append(stream_id)

    from music import telegram_backend
    monkeypatch.setattr(telegram_backend.go_bridge, "open_stream", open_stream)
    monkeypatch.setattr(telegram_backend.go_bridge, "close_stream", close_stream)

    voice = FakeVoiceClient()
    backend = TelegramVoiceChatBackend(voice)
    track = Track("Song", "https://example.com/song.mp3", 120, 1, "User")

    await backend.start(10, track, 100)
    await backend.start(10, track, 100, position=30)

    assert closed == ["stream-1"]
    assert opened[1][2] == 30
    assert [event[0] for event in voice.events] == ["play", "play"]
    assert all(event[0] != "leave" for event in voice.events)

    await backend.stop(10)
    assert closed == ["stream-1", "stream-2"]
    assert all(event[0] != "leave" for event in voice.events)

    await backend.leave(10)
    assert voice.events[-1] == ("leave", 10, False)


@pytest.mark.asyncio
async def test_backend_applies_volume_and_controls(monkeypatch):
    fake_types = types.ModuleType("pytgcalls.types")
    fake_types.MediaStream = FakeMediaStream
    fake_package = types.ModuleType("pytgcalls")
    fake_package.types = fake_types
    monkeypatch.setitem(sys.modules, "pytgcalls", fake_package)
    monkeypatch.setitem(sys.modules, "pytgcalls.types", fake_types)

    async def open_stream(url, output_format="opus", position=0):
        return {"stream_id": "stream-1", "stream_url": "http://engine/stream-1.ogg"}

    async def close_stream(stream_id):
        return None

    from music import telegram_backend
    monkeypatch.setattr(telegram_backend.go_bridge, "open_stream", open_stream)
    monkeypatch.setattr(telegram_backend.go_bridge, "close_stream", close_stream)

    voice = FakeVoiceClient()
    backend = TelegramVoiceChatBackend(voice)
    track = Track("Song", "https://example.com/song.mp3", 120, 1, "User")

    await backend.start(20, track, 70)
    await backend.pause(20)
    await backend.resume(20)

    assert ("volume", 20, 70) in voice.events
    assert ("pause", 20) in voice.events
    assert ("resume", 20) in voice.events
