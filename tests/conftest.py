"""
CSE Aspirant - Test Configuration & Fixtures
"""
import pytest
import sys
import os

os.environ.setdefault("MASTER_API_KEY", "test-master-api-key")

# Ensure the root CSE-Aspirant directory is in sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from database.repository import repo

@pytest.fixture(autouse=True)
def reset_in_memory_state():
    """Cleans in-memory caches and tables between tests."""
    repo._users.clear()
    repo._subscriptions.clear()
    repo._payments.clear()
    repo._api_keys.clear()
    repo._group_settings.clear()
    repo._promotions.clear()
    repo._cache.clear()
    yield

