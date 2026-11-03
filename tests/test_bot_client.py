import sys
import types
from types import SimpleNamespace

import pytest

from bot.client import BotClient


class FakeClient:
    instances = []

    def __init__(self, name, **kwargs):
        self.name = name
        self.kwargs = kwargs
        self.handlers = []
        self.started = False
        self.stopped = False
        FakeClient.instances.append(self)

    def on_message(self, filter_value):
        def register(handler):
            self.handlers.append(("message", filter_value, handler))
            return handler

        return register

    def on_callback_query(self):
        def register(handler):
            self.handlers.append(("callback", handler))
            return handler

        return register

    async def start(self):
        self.started = True

    async def stop(self):
        self.stopped = True


class FakeVoiceClient:
    instances = []
    fail_on_start = False

    def __init__(self, assistant):
        self.assistant = assistant
        self.started = False
        self.stopped = False
        FakeVoiceClient.instances.append(self)

    async def start(self):
        if self.fail_on_start:
            raise RuntimeError("voice startup failed")
        self.started = True

    async def stop(self):
        self.stopped = True


@pytest.mark.asyncio
async def test_start_uses_separate_hydrogram_bot_and_assistant_clients(monkeypatch):
    FakeClient.instances.clear()
    FakeVoiceClient.instances.clear()

    hydrogram = types.ModuleType("hydrogram")
    hydrogram.Client = FakeClient
    hydrogram.filters = SimpleNamespace(text=object())
    hydrogram_types = types.ModuleType("hydrogram.types")
    hydrogram_types.CallbackQuery = object
    hydrogram_types.InlineKeyboardButton = object
    hydrogram_types.InlineKeyboardMarkup = object
    hydrogram_types.Message = object
    hydrogram.types = hydrogram_types

    pytgcalls = types.ModuleType("pytgcalls")
    pytgcalls.PyTgCalls = FakeVoiceClient
    monkeypatch.setitem(sys.modules, "hydrogram", hydrogram)
    monkeypatch.setitem(sys.modules, "hydrogram.types", hydrogram_types)
    monkeypatch.setitem(sys.modules, "pytgcalls", pytgcalls)

    import bot.client as client_module

    monkeypatch.setattr(
        client_module,
        "config",
        SimpleNamespace(
            bot=SimpleNamespace(
                bot_token="test-bot-token",
                api_id=12345,
                api_hash="test-api-hash",
                session_string="test-assistant-session",
            )
        ),
    )

    client = BotClient()
    await client.start()

    bot, assistant = FakeClient.instances
    assert bot.kwargs == {
        "api_id": 12345,
        "api_hash": "test-api-hash",
        "bot_token": "test-bot-token",
    }
    assert assistant.kwargs == {
        "api_id": 12345,
        "api_hash": "test-api-hash",
        "session_string": "test-assistant-session",
    }
    assert {handler[0] for handler in bot.handlers} == {"message", "callback"}
    assert FakeVoiceClient.instances[0].assistant is assistant
    assert bot.started and assistant.started and FakeVoiceClient.instances[0].started

    await client.stop()

    assert bot.stopped and assistant.stopped and FakeVoiceClient.instances[0].stopped


@pytest.mark.asyncio
async def test_start_cleans_up_clients_when_voice_start_fails(monkeypatch):
    FakeClient.instances.clear()
    FakeVoiceClient.instances.clear()
    FakeVoiceClient.fail_on_start = True

    hydrogram = types.ModuleType("hydrogram")
    hydrogram.Client = FakeClient
    hydrogram.filters = SimpleNamespace(text=object())
    hydrogram_types = types.ModuleType("hydrogram.types")
    hydrogram_types.CallbackQuery = object
    hydrogram_types.InlineKeyboardButton = object
    hydrogram_types.InlineKeyboardMarkup = object
    hydrogram_types.Message = object
    hydrogram.types = hydrogram_types
    pytgcalls = types.ModuleType("pytgcalls")
    pytgcalls.PyTgCalls = FakeVoiceClient
    monkeypatch.setitem(sys.modules, "hydrogram", hydrogram)
    monkeypatch.setitem(sys.modules, "hydrogram.types", hydrogram_types)
    monkeypatch.setitem(sys.modules, "pytgcalls", pytgcalls)

    import bot.client as client_module

    monkeypatch.setattr(
        client_module,
        "config",
        SimpleNamespace(
            bot=SimpleNamespace(
                bot_token="test-bot-token",
                api_id=12345,
                api_hash="test-api-hash",
                session_string="test-assistant-session",
            )
        ),
    )

    with pytest.raises(RuntimeError, match="voice startup failed"):
        await BotClient().start()

    bot, assistant = FakeClient.instances
    assert bot.stopped and assistant.stopped
    assert not FakeVoiceClient.instances[0].stopped
    FakeVoiceClient.fail_on_start = False
