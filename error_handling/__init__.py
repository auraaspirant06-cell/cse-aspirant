"""
CSE Aspirant Error Handling Module
"""
from error_handling.exceptions import (
    CSEAspirantException,
    MusicPlayerError,
    StreamRecoveryError,
    DatabaseError,
    APIError,
    RateLimitExceededError,
    SecurityViolationError,
    PaymentReconciliationError
)
from error_handling.retry import async_retry
from error_handling.circuit_breaker import CircuitBreaker, CircuitBreakerOpenException
from error_handling.handlers import format_error_response, handle_bot_error

__all__ = [
    "CSEAspirantException",
    "MusicPlayerError",
    "StreamRecoveryError",
    "DatabaseError",
    "APIError",
    "RateLimitExceededError",
    "SecurityViolationError",
    "PaymentReconciliationError",
    "async_retry",
    "CircuitBreaker",
    "CircuitBreakerOpenException",
    "format_error_response",
    "handle_bot_error"
]
