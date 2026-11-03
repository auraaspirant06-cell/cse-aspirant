"""Focused tests for environment-backed configuration."""
import importlib

import pytest

import core.config as config_module


REQUIRED_VALUES = {
    "BOT_TOKEN": "test-bot-token",
    "TELEGRAM_API_ID": "12345",
    "TELEGRAM_API_HASH": "test-api-hash",
    "TELEGRAM_SESSION_STRING": "test-session",
    "OWNER_ID": "42",
    "DATABASE_URL": "postgresql://user:password@localhost:5432/testdb",
    "REDIS_URL": "redis://localhost:6379/0",
    "GO_ENGINE_URL": "http://localhost:8080",
    "GO_ENGINE_TOKEN": "t" * 32,
    "MASTER_API_KEY": "01234567890123456789012345678901",
    "PAYMENT_UPI_ID": "merchant@example",
    "PAYMENT_MERCHANT_NAME": "Example Merchant",
    "PAYMENT_BANK_NAME": "Example Bank",
    "PAYMENT_ACCOUNT_NAME": "Example Account",
    "PAYMENT_ACCOUNT_NUMBER": "0000000000",
    "PAYMENT_IFSC_CODE": "EXAMPLE00000",
    "PAYMENT_BANK_BRANCH": "Example Branch",
    "PAYMENT_CHECKOUT_URL": "https://payments.example.test",
}


@pytest.fixture
def isolated_config(monkeypatch):
    names = set(REQUIRED_VALUES) | {
        "SUDO_USERS", "API_HOST", "API_PORT", "GO_ENGINE_PUBLIC_URL", "CORS_ORIGINS",
        "JWT_SECRET", "FFMPEG_PATH"
    }
    for name in names:
        monkeypatch.delenv(name, raising=False)
    importlib.reload(config_module)
    yield config_module
    importlib.reload(config_module)


def test_validation_reports_missing_names_without_values(isolated_config):
    with pytest.raises(isolated_config.ConfigurationError) as error:
        isolated_config.validate_config(isolated_config.AppConfig())

    message = str(error.value)
    assert "BOT_TOKEN" in message
    assert "DATABASE_URL" in message
    assert "test-bot-token" not in message


def test_validation_accepts_complete_configuration(isolated_config, monkeypatch):
    for name, value in REQUIRED_VALUES.items():
        monkeypatch.setenv(name, value)
    monkeypatch.setenv("CORS_ORIGINS", "http://localhost:3000, https://example.test")
    importlib.reload(isolated_config)

    isolated_config.validate_config(isolated_config.AppConfig())
    assert isolated_config.config.services.cors_origins == [
        "http://localhost:3000",
        "https://example.test",
    ]


def test_validation_rejects_invalid_port(isolated_config, monkeypatch):
    for name, value in REQUIRED_VALUES.items():
        monkeypatch.setenv(name, value)
    monkeypatch.setenv("API_PORT", "70000")
    importlib.reload(isolated_config)

    with pytest.raises(isolated_config.ConfigurationError) as error:
        isolated_config.validate_config(isolated_config.AppConfig())

    assert "API_PORT" in str(error.value)
