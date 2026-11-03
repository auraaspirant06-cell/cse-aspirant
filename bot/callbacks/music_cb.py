"""
CSE Aspirant - Music Inline Callback Handler
"""
from typing import Dict, Any
from music.multi_group import multi_player_manager
from music.backend import AudioBackendError

class MusicCallbackHandler:
    async def handle(self, chat_id: int, action: str) -> str:
        player = multi_player_manager.get_player(chat_id)
        try:
            if action == "music_pause":
                ok = await player.pause()
                return "⏸ Playback paused." if ok else "Already paused or idle."
            elif action == "music_resume":
                ok = await player.resume()
                return "▶ Playback resumed." if ok else "Not paused."
            elif action == "music_skip":
                next_t = await player.skip()
                return f"⏭ Now Playing: {next_t.title}" if next_t else "⏹ Queue finished."
            elif action == "music_prev":
                prev_t = await player.previous()
                return f"⏮ Now Playing: {prev_t.title}" if prev_t else "No previous track."
            elif action == "music_shuffle":
                player.shuffle()
                return "🔀 Queue shuffled!"
            elif action == "music_repeat":
                new_mode = "ALL" if player.queue.repeat_mode == "OFF" else ("ONE" if player.queue.repeat_mode == "ALL" else "OFF")
                player.set_repeat(new_mode)
                return f"🔁 Repeat mode set to: {new_mode}"
            elif action == "music_stop":
                await player.stop()
                return "⏹ Playback stopped & queue cleared."
        except AudioBackendError as exc:
            return f"⚠️ Audio control failed: {exc}"
        return "Unknown music action."

music_cb_handler = MusicCallbackHandler()

