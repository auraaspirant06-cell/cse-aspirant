"""
CSE Aspirant - Admin Audit Logger
"""
from typing import Dict, Any, List
from datetime import datetime
from core.logger import logger

class AuditLogger:
    def __init__(self):
        self._logs: List[Dict[str, Any]] = []

    def log(self, action: str, actor_id: int, target_id: int = 0, details: str = ""):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "actor_id": actor_id,
            "target_id": target_id,
            "details": details
        }
        self._logs.append(entry)
        logger.info(f"AUDIT LOG: {entry}")

    def get_logs(self, limit: int = 20) -> List[Dict[str, Any]]:
        return self._logs[-limit:]

audit_logger = AuditLogger()

