"""
CSE Aspirant - Circuit Breaker Pattern for External Services
"""
import time
from typing import Callable, Any
from core.logger import logger

class CircuitBreakerOpenException(Exception):
    pass

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 30.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = 0.0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def record_success(self):
        self.failure_count = 0
        self.state = "CLOSED"

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            logger.error(f"Circuit Breaker tripped to OPEN state! Threshold: {self.failure_threshold}")

    def allow_request(self) -> bool:
        if self.state == "CLOSED":
            return True
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
                return True
            return False
        return True  # HALF_OPEN allows one trial request

    async def call(self, func: Callable, *args, **kwargs) -> Any:
        if not self.allow_request():
            raise CircuitBreakerOpenException("Circuit breaker is OPEN. Upstream call rejected.")
        try:
            res = await func(*args, **kwargs)
            self.record_success()
            return res
        except Exception as e:
            self.record_failure()
            raise e
