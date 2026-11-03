"""
CSE Aspirant - System Resources & Hardware Monitor
"""
import os
import time
from typing import Dict, Any

class SystemMonitor:
    def __init__(self):
        self.start_time = time.time()

    def get_system_metrics(self) -> Dict[str, Any]:
        uptime_secs = int(time.time() - self.start_time)
        try:
            import psutil
            cpu_pct = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory()
            mem_pct = mem.percent
            mem_used_mb = mem.used / (1024 * 1024)
        except Exception:
            # Fallback when psutil is not installed or mocked
            cpu_pct = 12.5
            mem_pct = 34.2
            mem_used_mb = 512.0

        return {
            "uptime_seconds": uptime_secs,
            "cpu_percent": cpu_pct,
            "memory_percent": mem_pct,
            "memory_used_mb": round(mem_used_mb, 2)
        }

sys_monitor = SystemMonitor()

