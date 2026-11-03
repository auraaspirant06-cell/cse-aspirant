"""
Unit Tests for Command Router & Multi-Prefix Callback System
"""
import pytest
from bot.router import router

@pytest.mark.parametrize("prefix", ["/", "!", "."])
def test_prefix_parsing(prefix):
    parsed = router.parse_command(f"{prefix}play lofi beats")
    assert parsed is not None
    assert parsed["command"] == "play"
    assert parsed["args"] == "lofi beats"
    assert parsed["prefix"] == prefix

@pytest.mark.asyncio
@pytest.mark.parametrize("prefix", ["/", "!", "."])
async def test_dispatch_start_and_help(prefix):
    res_start = await router.dispatch_command(chat_id=1, user_id=10, user_name="Aspirant", text=f"{prefix}start")
    assert res_start is not None
    assert "Namaste" in res_start["text"]
    assert res_start.get("photo") == "https://i.ytimg.com/vi/9Bk5WgGfkwM/maxresdefault.jpg"
    assert "reply_markup" in res_start

    res_help = await router.dispatch_command(chat_id=1, user_id=10, user_name="Aspirant", text=f"{prefix}help")
    assert res_help is not None
    assert "HELP CENTER" in res_help["text"]

@pytest.mark.asyncio
async def test_help_category_callbacks():
    categories = [
        "help_music",
        "help_education",
        "help_programming",
        "help_ai",
        "help_premium",
        "help_security",
        "help_promotion",
        "help_owner"
    ]
    for cat in categories:
        res = await router.dispatch_callback(chat_id=1, user_id=10, callback_data=cat)
        assert res is not None
        assert len(res["text"]) > 20
        assert "COMMANDS" in res["text"] or "PANEL" in res["text"]

@pytest.mark.asyncio
async def test_music_commands_dispatch():
    res = await router.dispatch_command(chat_id=200, user_id=10, user_name="Dev", text="/play Lofi Coding Beats")
    assert res is not None
    assert "Now Playing" in res["text"]

    pause = await router.dispatch_command(chat_id=200, user_id=10, user_name="Dev", text="!pause")
    assert pause is not None
    assert "paused" in pause["text"]

    resume = await router.dispatch_command(chat_id=200, user_id=10, user_name="Dev", text=".resume")
    assert resume is not None
    assert "resumed" in resume["text"]

