"""
CSE Aspirant - Async Event Dispatcher
"""
import asyncio
from typing import Callable, Dict, List, Any
from core.logger import logger

class EventBus:
    def __init__(self):
        self._listeners: Dict[str, List[Callable[..., Any]]] = {}

    def subscribe(self, event_name: str, handler: Callable[..., Any]):
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(handler)

    async def emit(self, event_name: str, **kwargs):
        listeners = self._listeners.get(event_name, [])
        for handler in listeners:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(**kwargs)
                else:
                    handler(**kwargs)
            except Exception as e:
                logger.error(f"EventBus error on '{event_name}': {e}")

bus = EventBus()
