"""
CSE Aspirant - Custom & Academy Playlists
"""
from typing import Dict, List, Optional
from music.track import Track
import uuid

class PlaylistManager:
    def __init__(self):
        self._playlists: Dict[str, List[Track]] = {}
        self._initialize_academy_playlists()

    def _initialize_academy_playlists(self):
        self._playlists["study_focus"] = [
            Track("Lofi Study Beats", "https://stream.cse-aspirant.org/audio/lofi-study.mp3", 180, 0, "CSE Aspirant"),
            Track("Ambient Alpha Waves", "https://stream.cse-aspirant.org/audio/alpha-waves.mp3", 600, 0, "CSE Aspirant"),
        ]
        self._playlists["upsc_motivation"] = [
            Track("UPSC Aspirant Theme", "https://stream.cse-aspirant.org/audio/upsc-motivation.mp3", 240, 0, "CSE Aspirant"),
        ]
        self._playlists["coding_flow"] = [
            Track("Synthwave Hacker Beats", "https://stream.cse-aspirant.org/audio/coding-synthwave.mp3", 310, 0, "CSE Aspirant"),
        ]

    def create_playlist(self, name: str) -> str:
        pl_id = name.lower().replace(" ", "_")
        if pl_id not in self._playlists:
            self._playlists[pl_id] = []
        return pl_id

    def add_track(self, playlist_id: str, track: Track):
        if playlist_id in self._playlists:
            self._playlists[playlist_id].append(track)

    def get_tracks(self, playlist_id: str) -> List[Track]:
        return self._playlists.get(playlist_id, [])

    def list_playlists(self) -> List[str]:
        return list(self._playlists.keys())

playlist_manager = PlaylistManager()
