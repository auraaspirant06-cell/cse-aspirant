"""
CSE Aspirant - Multi-Group Music Player Manager
"""
from typing import Dict, List, Optional
from music.player import GuildPlayer
from core.logger import logger

class MultiGroupManager:
    def __init__(self):
        self._players: Dict[int, GuildPlayer] = {}

    def get_player(self, chat_id: int) -> GuildPlayer:
        if chat_id not in self._players:
            logger.info(f"Instantiating new GuildPlayer for chat {chat_id}")
            self._players[chat_id] = GuildPlayer(chat_id)
        return self._players[chat_id]

    def remove_player(self, chat_id: int):
        if chat_id in self._players:
            del self._players[chat_id]

    def list_active_players(self) -> List[int]:
        return [cid for cid, p in self._players.items() if p.state != "STOPPED" and p.queue.current]

    def count_active_players(self) -> int:
        return len(self.list_active_players())

multi_player_manager = MultiGroupManager()
