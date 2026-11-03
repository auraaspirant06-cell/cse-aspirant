"""
CSE Aspirant - Security & Audit Commands
"""
from typing import Dict, Any
from security.audit import audit_logger

async def handle_audit() -> Dict[str, Any]:
    logs = audit_logger.get_logs(10)
    if not logs:
        return {"text": "🛡 **Audit Log**: No recent security incidents or moderation events."}

    lines = ["🛡 **RECENT AUDIT LOG ENTRIES**:\n"]
    for l in logs:
        lines.append(f"• `{l['timestamp'][11:19]}` [{l['action']}] Actor: `{l['actor_id']}` -> Details: {l['details']}")
    return {"text": "\n".join(lines)}

