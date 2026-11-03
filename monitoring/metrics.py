"""
CSE Aspirant - Application Metrics & Prometheus Exporter
"""
from typing import Dict, Any

class MetricsCollector:
    def __init__(self):
        self.counters = {
            "commands_total": 0,
            "music_tracks_played": 0,
            "ai_queries_total": 0,
            "api_requests_total": 0,
            "errors_total": 0
        }

    def increment(self, metric: str, amount: int = 1):
        if metric in self.counters:
            self.counters[metric] += amount

    def to_prometheus(self) -> str:
        lines = []
        for k, v in self.counters.items():
            lines.append(f"# TYPE cse_aspirant_{k} counter")
            lines.append(f"cse_aspirant_{k} {v}")
        return "\n".join(lines) + "\n"

metrics = MetricsCollector()

