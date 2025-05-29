import asyncio

from core.bot.buttons import btn
from telegram import KeyboardButton, ReplyKeyboardMarkup

_MENU_CACHED = {}
_LOCK = asyncio.Lock()


async def set_menu() -> ReplyKeyboardMarkup:
    """Set keyboard menu."""
    global _MENU_CACHED

    if btn.FAQ not in _MENU_CACHED:
        async with _LOCK:
            _MENU_CACHED[btn.FAQ] = ReplyKeyboardMarkup([[KeyboardButton(btn.FAQ)]], resize_keyboard=True)
    return _MENU_CACHED[btn.FAQ]
