"""
CSE Aspirant - Unified Health Check Service
"""
from typing import Dict, Any
from core.context import state
from database.connection import db_manager
from music.multi_group import multi_player_manager
from monitoring.sys_info import sys_monitor

class HealthChecker:
    async def run_checks(self) -> Dict[str, Any]:
        sys_data = sys_monitor.get_system_metrics()
        active_streams = multi_player_manager.count_active_players()
        
        db_ok = bool(db_manager.pg_pool or db_manager.is_connected)
        redis_ok = bool(db_manager.redis_client or db_manager.is_connected)

        return {
            "status": "HEALTHY",
            "bot_ready": state.is_ready,
            "database_connected": db_ok,
            "redis_connected": redis_ok,
            "active_music_players": active_streams,
            "system": sys_data
        }

health_checker = HealthChecker()

