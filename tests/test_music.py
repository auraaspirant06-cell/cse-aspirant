"""
Unit Tests for Music Engine & Player
"""
import pytest
import asyncio
from music.track import Track
from music.queue import MusicQueue
from music.player import GuildPlayer
from music.search import search_engine


class FakeAudioBackend:
    def __init__(self):
        self.events = []

    async def start(self, chat_id, track, volume, position=0):
        self.events.append(("start", chat_id, track.track_id, volume, position))

    async def pause(self, chat_id):
        self.events.append(("pause", chat_id))

    async def resume(self, chat_id):
        self.events.append(("resume", chat_id))

    async def stop(self, chat_id):
        self.events.append(("stop", chat_id))

    async def leave(self, chat_id):
        self.events.append(("leave", chat_id))

    async def set_volume(self, chat_id, volume):
        self.events.append(("volume", chat_id, volume))

    async def seek(self, chat_id, track, volume, position):
        self.events.append(("seek", chat_id, position))

def test_music_queue_operations():
    q = MusicQueue()
    t1 = Track(title="Song 1", uri="http://audio1.mp3", duration=180, requester_id=1, requester_name="Alice")
    t2 = Track(title="Song 2", uri="http://audio2.mp3", duration=210, requester_id=1, requester_name="Alice")

    q.add(t1)
    q.add(t2)
    assert len(q.tracks) == 2

    curr = q.next()
    assert curr.title == "Song 1"
    assert len(q.tracks) == 1

    # Test Previous
    curr2 = q.next()
    assert curr2.title == "Song 2"
    
    prev = q.previous()
    assert prev.title == "Song 1"

def test_repeat_mode():
    q = MusicQueue()
    t1 = Track(title="Loop Track", uri="http://loop.mp3", duration=100, requester_id=1, requester_name="Bob")
    q.add(t1)
    
    q.set_repeat("ONE")
    curr = q.next()
    assert curr.title == "Loop Track"
    
    # Next should still return the same track in repeat ONE
    again = q.next()
    assert again.title == "Loop Track"

@pytest.mark.asyncio
async def test_guild_player_playback():
    backend = FakeAudioBackend()
    player = GuildPlayer(chat_id=1001, backend=backend)
    t = Track(title="Study Beat", uri="http://study.mp3", duration=200, requester_id=42, requester_name="Charlie")
    
    played = await player.play(t)
    assert played.title == "Study Beat"
    assert player.state == "PLAYING"

    # Pause & Resume
    assert await player.pause() is True
    assert player.state == "PAUSED"
    assert await player.resume() is True
    assert player.state == "PLAYING"

    # Volume limits
    vol = player.set_volume(150)
    assert vol == 150
    assert player.set_volume(300) == 200

    # Stop
    await player.stop()
    assert player.state == "STOPPED"
    assert player.queue.current is None
    assert backend.events[0][0] == "start"
    assert ("pause", 1001) in backend.events
    assert ("resume", 1001) in backend.events
    assert ("leave", 1001) in backend.events

@pytest.mark.asyncio
async def test_music_search():
    res = await search_engine.search("https://example.com/audio.mp3", requester_id=1, requester_name="User")
    assert len(res) > 0
    assert res[0].uri == "https://example.com/audio.mp3"


@pytest.mark.asyncio
async def test_seek_calls_audio_backend():
    backend = FakeAudioBackend()
    player = GuildPlayer(chat_id=1002, backend=backend)
    track = Track("Seekable", "https://example.com/seek.ogg", 120, 1, "User")
    await player.play(track)
    assert await player.seek(45) == 45
    assert ("seek", 1002, 45) in backend.events

