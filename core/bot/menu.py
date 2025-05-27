from core.bot.messages import get, msg
from telegram import KeyboardButton, ReplyKeyboardMarkup


async def set_menu(only_faq=False):
    """Set keyboard menu."""
    if only_faq:
        keyboard = [[KeyboardButton(get(msg.BUTTON_FAQ))]]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    keyboard = []
    keyboard.append([KeyboardButton(get(msg.BUTTON_FAQ))])
    confirm_cancel_row = [KeyboardButton(get(msg.BUTTON_CONFIRM)), KeyboardButton(get(msg.BUTTON_CANCEL))]
    keyboard.append(confirm_cancel_row)

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
