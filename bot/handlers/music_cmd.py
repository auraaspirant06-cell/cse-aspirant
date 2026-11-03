"""
CSE Aspirant - Music Commands Handler
"""
from typing import Dict, Any, List
from music.multi_group import multi_player_manager
from music.search import search_engine
from music.playlist import playlist_manager
from bot.keyboards.inline import inline_kb

async def handle_play(chat_id: int, user_id: int, user_name: str, query: str) -> Dict[str, Any]:
    if not query:
        return {"text": "⚠️ Please provide a song name or stream URL! Example: `/play lofi study beats`"}

    tracks = await search_engine.search(query, requester_id=user_id, requester_name=user_name)
    if not tracks:
        return {"text": "❌ No audio found for your query. Try another keyword or URL."}

    player = multi_player_manager.get_player(chat_id)
    track = await player.play(tracks[0])
    
    text = (
        f"🎶 **Now Playing:** [{track.title}]({track.uri})\n"
        f"⏱ Duration: {track.duration}s | 👤 Requested by: {user_name}\n"
        f"🎚 Volume: {player.volume}% | 🔁 Repeat: {player.queue.repeat_mode}"
    )
    return {
        "text": text,
        "reply_markup": {"inline_keyboard": inline_kb.music_player_controls()}
    }

async def handle_pause(chat_id: int) -> Dict[str, Any]:
    player = multi_player_manager.get_player(chat_id)
    ok = await player.pause()
    return {"text": "⏸ Playback paused." if ok else "⚠️ No audio is currently playing."}

async def handle_resume(chat_id: int) -> Dict[str, Any]:
    player = multi_player_manager.get_player(chat_id)
    ok = await player.resume()
    return {"text": "▶ Playback resumed." if ok else "⚠️ Player is not paused."}

async def handle_skip(chat_id: int) -> Dict[str, Any]:
    player = multi_player_manager.get_player(chat_id)
    next_t = await player.skip()
    if next_t:
        return {
            "text": f"⏭ **Skipped!** Now Playing: {next_t.title}",
            "reply_markup": {"inline_keyboard": inline_kb.music_player_controls()}
        }
    return {"text": "⏹ Queue is empty. Playback stopped."}

async def handle_previous(chat_id: int) -> Dict[str, Any]:
    player = multi_player_manager.get_player(chat_id)
    prev_t = await player.previous()
    if prev_t:
        return {
            "text": f"⏮ **Playing Previous:** {prev_t.title}",
            "reply_markup": {"inline_keyboard": inline_kb.music_player_controls()}
        }
    return {"text": "⚠️ No previous track in history."}

async def handle_stop(chat_id: int) -> Dict[str, Any]:
    player = multi_player_manager.get_player(chat_id)
    await player.stop()
    return {"text": "⏹ Audio playback stopped and queue cleared."}

async def handle_queue(chat_id: int) -> Dict[str, Any]:
    player = multi_player_manager.get_player(chat_id)
    tracks = player.queue.tracks
    current = player.queue.current

    if not current and not tracks:
        return {"text": "📭 The music queue is currently empty."}

    lines = ["🎵 **CURRENT MUSIC QUEUE**:\n"]
    if current:
        lines.append(f"▶ **Current:** {current.title} ({current.duration}s)")
    if tracks:
        lines.append("\n**Up Next:**")
        for i, t in enumerate(tracks[:10], start=1):
            lines.append(f"{i}. {t.title} ({t.duration}s)")
        if len(tracks) > 10:
            lines.append(f"\n*...and {len(tracks) - 10} more tracks.*")

    return {"text": "\n".join(lines)}

async def handle_shuffle(chat_id: int) -> Dict[str, Any]:
    player = multi_player_manager.get_player(chat_id)
    player.shuffle()
    return {"text": "🔀 Queue has been shuffled randomly!"}

async def handle_repeat(chat_id: int, mode: str) -> Dict[str, Any]:
    player = multi_player_manager.get_player(chat_id)
    mode = mode.upper() if mode else ("ALL" if player.queue.repeat_mode == "OFF" else "OFF")
    player.set_repeat(mode)
    return {"text": f"🔁 Repeat mode set to: **{mode}**"}

async def handle_volume(chat_id: int, level: str) -> Dict[str, Any]:
    try:
        vol = int(level)
    except Exception:
        vol = 100
    player = multi_player_manager.get_player(chat_id)
    new_vol = player.set_volume(vol)
    return {"text": f"🎚 Volume set to **{new_vol}%**"}

async def handle_playlist(chat_id: int, name: str, user_id: int, user_name: str) -> Dict[str, Any]:
    tracks = playlist_manager.get_tracks(name)
    if not tracks:
        avail = ", ".join(playlist_manager.list_playlists())
        return {"text": f"⚠️ Playlist '{name}' not found. Available: `{avail}`"}

    player = multi_player_manager.get_player(chat_id)
    for t in tracks:
        await player.play(t)
    return {"text": f"📁 Enqueued **{len(tracks)}** tracks from playlist `{name}`!"}

