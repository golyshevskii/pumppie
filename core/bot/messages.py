"""
Messages for the Telegram bot.

This module contains all text content used in the bot,
organized by context and language.
"""

from enum import Enum, auto


class Language(Enum):
    """Available languages."""

    RU = auto()
    EN = auto()


# Default language for the bot
DEFAULT_LANGUAGE = Language.RU


class Messages:
    """Container for all messages used in the bot."""

    # Command responses
    COMMAND_START = {
        Language.RU: "Привет! Я твой персональный помощник. Чем могу помочь?",
        Language.EN: "Hello! I'm your personal assistant. How can I help you?",
    }

    COMMAND_HELP = {
        Language.RU: "Доступные команды:\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать это сообщение\n"
        "/faq - Часто задаваемые вопросы",
        Language.EN: "Available commands:\n"
        "/start - Start working with the bot\n"
        "/help - Show this message\n"
        "/faq - Frequently asked questions",
    }

    # Button texts
    BUTTON_FAQ = {Language.RU: "FAQ", Language.EN: "FAQ"}

    BUTTON_CONFIRM = {Language.RU: "Подтвердить", Language.EN: "Confirm"}

    BUTTON_CANCEL = {Language.RU: "Отменить", Language.EN: "Cancel"}

    BUTTON_BACK = {Language.RU: "Назад", Language.EN: "Back"}

    # Notifications and responses
    PROCESSING_REQUEST = {Language.RU: "Обрабатываю ваш запрос...", Language.EN: "Processing your request..."}

    REQUEST_CONFIRMED = {Language.RU: "Запрос подтвержден!", Language.EN: "Request confirmed!"}

    REQUEST_CANCELLED = {Language.RU: "Запрос отменен.", Language.EN: "Request cancelled."}

    # Error messages
    ERROR_GENERAL = {
        Language.RU: "Произошла ошибка. Пожалуйста, попробуйте еще раз позже.",
        Language.EN: "An error occurred. Please try again later.",
    }

    ERROR_NOT_UNDERSTOOD = {
        Language.RU: "Извините, я не понял ваш запрос. Можете уточнить?",
        Language.EN: "Sorry, I didn't understand your request. Can you clarify?",
    }


def get_message(message_key: dict[Language, str], lang: Language = DEFAULT_LANGUAGE) -> str:
    """
    Get message in the specified language.

    Args:
        message_key: Dictionary with language keys and message texts
        lang: Language to get the message in

    Returns:
        Message text in the specified language
    """
    return message_key.get(lang, message_key.get(DEFAULT_LANGUAGE, "Message not found"))


# Aliases for easier access
msg = Messages()
get = get_message
