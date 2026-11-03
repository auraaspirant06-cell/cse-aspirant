"""
CSE Aspirant - Async Retry Policy with Exponential Backoff
"""
import asyncio
import functools
import random
from typing import Callable, Any, Tuple, Type
from core.logger import logger

def async_retry(
    max_retries: int = 3,
    initial_delay: float = 0.5,
    backoff_factor: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    def decorator(func: Callable[..., Any]):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            delay = initial_delay
            last_err = None
            for attempt in range(1, max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_err = e
                    if attempt == max_retries:
                        logger.error(f"Function {func.__name__} failed after {max_retries} attempts: {e}")
                        raise
                    jitter = random.uniform(0.8, 1.2)
                    sleep_time = delay * jitter
                    logger.warning(
                        f"Attempt {attempt}/{max_retries} failed for {func.__name__}: {e}. Retrying in {sleep_time:.2f}s"
                    )
                    await asyncio.sleep(sleep_time)
                    delay *= backoff_factor
            if last_err:
                raise last_err
        return wrapper
    return decorator
