"""
Unit Tests for Music Engine & Player
"""
import pytest
import asyncio
from music.track import Track
from music.queue import MusicQueue
from music.player import GuildPlayer
from music.search import search_engine

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
    player = GuildPlayer(chat_id=1001)
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

@pytest.mark.asyncio
async def test_music_search():
    res = await search_engine.search("UPSC Motivation", requester_id=1, requester_name="User")
    assert len(res) > 0
    assert "UPSC" in res[0].title

