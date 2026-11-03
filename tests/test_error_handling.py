"""
Unit Tests for Error Handling, Circuit Breakers & Retry Policies
"""
import pytest
import asyncio
from error_handling.exceptions import CSEAspirantException, MusicPlayerError, DatabaseError
from error_handling.retry import async_retry
from error_handling.circuit_breaker import CircuitBreaker, CircuitBreakerOpenException

def test_exception_hierarchy():
    e = MusicPlayerError("Stream dropped", track_id="track1")
    assert isinstance(e, CSEAspirantException)
    assert e.code == "MUSIC_PLAYER_ERROR"
    assert e.track_id == "track1"

@pytest.mark.asyncio
async def test_retry_policy():
    attempts = 0

    @async_retry(max_retries=3, initial_delay=0.01)
    async def flaky_call():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ConnectionError("Temporary glitch")
        return "SUCCESS"

    res = await flaky_call()
    assert res == "SUCCESS"
    assert attempts == 3

@pytest.mark.asyncio
async def test_circuit_breaker():
    cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0.1)

    async def faulty_remote():
        raise TimeoutError("Remote server offline")

    # 1st failure
    with pytest.raises(TimeoutError):
        await cb.call(faulty_remote)
    assert cb.state == "CLOSED"

    # 2nd failure -> Tripped
    with pytest.raises(TimeoutError):
        await cb.call(faulty_remote)
    assert cb.state == "OPEN"

    # Subsequent request is immediately rejected without calling target
    with pytest.raises(CircuitBreakerOpenException):
        await cb.call(faulty_remote)

