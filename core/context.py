"""
CSE Aspirant - Global Execution Context
"""
from typing import Optional, Any
from dataclasses import dataclass, field
import time

@dataclass
class AppState:
    boot_time: float = field(default_factory=time.time)
    active_guilds: int = 0
    total_commands_executed: int = 0
    redis_client: Optional[Any] = None
    db_pool: Optional[Any] = None
    is_ready: bool = False

state = AppState()
