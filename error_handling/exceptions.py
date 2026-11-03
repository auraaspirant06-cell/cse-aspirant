"""
CSE Aspirant - Unified Exception Hierarchy
"""

class CSEAspirantException(Exception):
    """Base exception for all CSE Aspirant bot errors."""
    def __init__(self, message: str, code: str = "INTERNAL_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)

class MusicPlayerError(CSEAspirantException):
    """Raised when an error occurs during audio streaming or playback."""
    def __init__(self, message: str, track_id: str = ""):
        self.track_id = track_id
        super().__init__(message, code="MUSIC_PLAYER_ERROR")

class StreamRecoveryError(MusicPlayerError):
    """Raised when an audio stream cannot be recovered."""
    pass

class DatabaseError(CSEAspirantException):
    """Raised on relational or key-value database failures."""
    pass

class APIError(CSEAspirantException):
    """Raised when an external or internal API call fails."""
    def __init__(self, message: str, status_code: int = 500):
        self.status_code = status_code
        super().__init__(message, code=f"API_ERROR_{status_code}")

class RateLimitExceededError(CSEAspirantException):
    """Raised when a user or group exceeds quota."""
    def __init__(self, retry_after: int = 30):
        self.retry_after = retry_after
        super().__init__(f"Rate limit exceeded. Retry in {retry_after}s", code="RATE_LIMITED")

class SecurityViolationError(CSEAspirantException):
    """Raised when anti-spam, toxic content, or bad URLs are detected."""
    pass

class PaymentReconciliationError(CSEAspirantException):
    """Raised during payment UTR validation or duplicate submission."""
    pass
