"""
CSE Aspirant - Multi-Group Music Player Manager
"""
from typing import Callable, Dict, List, Optional
from music.player import GuildPlayer
from core.logger import logger

class MultiGroupManager:
    def __init__(self, backend_factory: Optional[Callable[[], object]] = None):
        self._players: Dict[int, GuildPlayer] = {}
        self._backend_factory = backend_factory

    def set_backend_factory(self, backend_factory: Callable[[], object]) -> None:
        self._backend_factory = backend_factory

    def get_player(self, chat_id: int) -> GuildPlayer:
        if chat_id not in self._players:
            logger.info(f"Instantiating new GuildPlayer for chat {chat_id}")
            backend = self._backend_factory() if self._backend_factory else None
            self._players[chat_id] = GuildPlayer(chat_id, backend=backend)
        return self._players[chat_id]

    def remove_player(self, chat_id: int):
        if chat_id in self._players:
            del self._players[chat_id]

    def list_active_players(self) -> List[int]:
        return [cid for cid, p in self._players.items() if p.state != "STOPPED" and p.queue.current]

    def count_active_players(self) -> int:
        return len(self.list_active_players())

multi_player_manager = MultiGroupManager()
